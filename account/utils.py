import base64
import jwt

from rest_framework import exceptions
from rest_framework_jwt.authentication import JSONWebTokenAuthentication
from rest_framework_jwt.settings import api_settings

jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
jwt_decode_handler = api_settings.JWT_DECODE_HANDLER

def base64_decode(encoded_string):
  """Decode base64, padding being optional.

  :param data: Base64 data as an ASCII byte string
  :returns: The decoded byte string.

  """
  missing_padding = len(encoded_string) % 4
  if missing_padding != 0:
      encoded_string += '=' * (4 - missing_padding)
  return base64.b64decode(encoded_string)

def get_user_jwt_token(user):
  """
  Get the JWT payload for the user and
  Create the response object with the JWT payload.
  """
  payload = jwt_payload_handler(user)
  token = jwt_encode_handler(payload)
  
  return token

def get_user_from_jwt_value(jwt_value):
  try:
    payload = jwt_decode_handler(jwt_value)
  except jwt.ExpiredSignature:
    msg = 'Signature has expired.'
    raise exceptions.AuthenticationFailed(msg)
  except jwt.DecodeError:
    msg = 'Error decoding signature.'
    raise exceptions.AuthenticationFailed(msg)

  return JSONWebTokenAuthentication().authenticate_credentials(payload)