import json
import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions, status

class BetaList(APIView):
  """
  Add to beta waitlsit.

  """
  permission_classes = (permissions.AllowAny,)

  def get(self, request, format=None):
    """
    Return a list of all users.
    """
    return Response('GET not allowed')

  def post(self, request, format=None):
    if not request.data or 'email' not in request.data:
      return Response('Email not provided', status=status.HTTP_400_BAD_REQUEST)

    email = request.data['email']
    api_key = 'b6d356617303648da8431084847bc905-us15'
    beta_list_id = '85fad0375a'
    headers = {'Authorization': 'apikey ' + api_key}
    url = 'https://us15.api.mailchimp.com/3.0/lists/' + beta_list_id + '/members/'

    params = {
      'email_address': email,
      'status': 'subscribed',
    }

    r = requests.post(url, auth=('apikey', api_key), data=json.dumps(params))

    if r.status_code == requests.codes.ok:
      return Response('Email subscribed', status=status.HTTP_200_OK)
    else:
      r.raise_for_status()