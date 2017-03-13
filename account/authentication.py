from account.utils import base64_decode
from cryptography.x509 import load_pem_x509_certificate
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta
from django.conf import settings
import hashlib
import jwt
import json
import pytz
from pytz import utc
import requests
from rest_framework.exceptions import APIException
from utils.dates import utcnow
import base64


def validate_outlook_token_header(header):
  if 'typ' not in header:
    raise APIException('Missing typ from header')

  if header['typ'] != 'JWT':
    raise APIException('Not a JWT')

  if 'alg' not in header:
    raise APIException('Missing alg from header')

  if header['alg'] != 'RS256':
    raise APIException('Wrong alg')

  if 'x5t' not in header:
    raise APIException('Missing signature from header')


def validate_outlook_token_lifetime(payload):
  if 'nbf' not in payload:
    raise APIException('Missing valid from date')

  if 'exp' not in payload:
    raise APIException('Missing valid to date')

  valid_from_epoch = payload['nbf']
  valid_until_epoch = payload['exp']

  valid_from_datetime = datetime.utcfromtimestamp(valid_from_epoch).replace(tzinfo=utc)
  valid_until_datetime = datetime.utcfromtimestamp(valid_until_epoch).replace(tzinfo=utc)

  # 5 miinute padding to accomodate time difference b/t server & client
  padding = timedelta(minutes=5)

  if valid_from_datetime - utcnow() > padding:
    raise APIException('Token not yet valid')

  if utcnow() - valid_until_datetime > padding:
    raise APIException('Token expired')


def validate_outlook_token_audience(payload):
  if 'aud' not in payload:
    raise APIException('Missing audience in payload')

  if payload['aud'] != settings.OUTLOOK_AUDIENCE:
    msg = 'Wrong audience: ' + payload['aud'] + 'should be ' + settings.OUTLOOK_AUDIENCE
    raise APIException(msg)


def validate_outlook_token_version(payload):
  app_context = json.loads(payload['appctx'])

  if 'msexchuid' not in app_context:
    raise APIException('Missing unique identifier')

  if app_context['version'] != 'ExIdTok.V1':  # Version for Exchange 2013
    raise APIException('Wrong version')

  if 'amurl' not in app_context:
    raise APIException('Missing metadata location')


def get_metadata_document(auth_metadata_endpoint):
  document = requests.get(auth_metadata_endpoint).json()

  if not document:
    raise APIException('No authentication metadata found')

  return document


def get_signing_certificate(auth_metadata_endpoint):
  document = get_metadata_document(auth_metadata_endpoint)

  if bool(document) and len(document['keys']):
    signing_key = document['keys'][0]

    if signing_key and signing_key['keyvalue']:
      cert_value = signing_key['keyvalue']['value']

      #  Need to convert to proper pem format with the BEGIN and END tags, and each line having 64 characters
      cert_value_splits = '\r\n'.join(cert_value[i:min(i+64, len(cert_value))] for i in range(0, len(cert_value), 64))
      x509_cert = '-----BEGIN CERTIFICATE-----\n'+cert_value_splits+'\n-----END CERTIFICATE-----'  # this is so sketch...
      
      return x509_cert.encode()

  raise APIException('The metadata document does not contain a signing certificate')


def vaildate_outlook_token_signature_and_get_unique_identifier(raw_token, payload):
  app_context = json.loads(payload['appctx'])
  auth_metadata_endpoint = app_context['amurl']

  cert_str = get_signing_certificate(auth_metadata_endpoint)
  cert_obj = load_pem_x509_certificate(cert_str, default_backend())
  public_key = cert_obj.public_key()
  try:
    verified_payload = jwt.decode(raw_token, public_key, algorithms=['RS256'], audience=settings.OUTLOOK_AUDIENCE)
    verified_app_context = json.loads(verified_payload['appctx'])
  except:
    APIException('Cannot verify Outlook token')

  #  has Exchange ID and auth metadata endpoint
  payload_app_context_bytes = (verified_app_context['msexchuid'] + verified_app_context['amurl']).encode()
  unique_identifier = hashlib.sha256(payload_app_context_bytes).hexdigest()
  return unique_identifier
