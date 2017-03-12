import json
import jwt

from account.authentication import (
  validate_outlook_token_header, validate_outlook_token_lifetime, validate_outlook_token_audience,
  validate_outlook_token_version, vaildate_outlook_token_signature_and_get_unique_identifier
)
from account.models import User, OutlookUser
from account.utils import base64_decode, get_user_jwt_token, get_user_from_jwt_value
from customer.models import Customer
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.exceptions import APIException
from rest_framework.response import Response
from rest_framework.exceptions import APIException


class OutlookAuth(APIView):
  """
  PATH - /auth/outlook
  """

  permission_classes = (permissions.AllowAny,)

  def post(self, request, format=None):
    if not request.data or 'token' not in request.data or 'email' not in request.data:
      return Response('Credentials not provided', status=status.HTTP_400_BAD_REQUEST)

    raw_token = request.data['token']
    email = request.data['email']

    """
    Steps:
    1. Verify the token and user
    2. Create new token manually and pass back
    """
    token_parts = raw_token.split('.')
    if len(token_parts) != 3:
      return Response('Invalid token', status=status.HTTP_400_BAD_REQUEST)

    encoded_header = token_parts[0]
    encoded_payload = token_parts[1]
    signature = token_parts[2]


    decoded_header = json.loads(base64_decode(encoded_header))
    decoded_payload = json.loads(base64_decode(encoded_payload))

    validate_outlook_token_header(decoded_header)
    validate_outlook_token_lifetime(decoded_payload)
    validate_outlook_token_audience(decoded_payload)
    validate_outlook_token_version(decoded_payload)
    unique_identifier = vaildate_outlook_token_signature_and_get_unique_identifier(raw_token, decoded_payload)

    """
    Once the unique is obtained. Create User and Outlook User instances
    """
    try:
      outlook_user = OutlookUser.objects.get(unique_identifier=unique_identifier)
      user = outlook_user.user
      customer = user.customer_profile
    except OutlookUser.DoesNotExist:
      # Register the Outlook user
      user = User.objects.create_user(email)
      outlook_user = OutlookUser(unique_identifier=unique_identifier, user=user)
      outlook_user.save()
      customer = Customer(user=user)
      customer.save()
    except:
      raise APIException('Failed to get user')

    jwt_token = get_user_jwt_token(user)

    return Response({'token': jwt_token, 'id': customer.id}, status.HTTP_200_OK)


class AuthLogin(APIView):
  """
  PATH: /auth/login
  """

  permission_classes = (permissions.AllowAny,)

  def post(self, request):
    if not request.data or 'token' not in request.data:
      return Response('Token not provided', status=status.HTTP_400_BAD_REQUEST)

    jwt_token = request.data['token']
    user = get_user_from_jwt_value(jwt_token)
    customer = user.customer_profile

    return Response({'token': jwt_token, 'id': customer.id}, status.HTTP_200_OK)
