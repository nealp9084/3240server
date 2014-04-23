from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json

from users.models import User
from tokens.models import Token

def index(request):
  if request.method == 'GET':
    param_secret = request.GET['token']

    # get the current user via the access token
    current_user = Token.get_current_user(param_secret)
    if not current_user:
      return HttpResponseForbidden()

    if current_user.is_admin:
      objs = [x.to_dict() for x in list(Token.objects.all())]
      json_data = json.dumps(objs)
      return HttpResponse(json_data)
    else:
      return HttpResponseForbidden()
  else:
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def login(request):
  if request.method == 'POST':
    param_name = request.POST['name']
    param_password = request.POST['password']

    # get the current user via the access token
    user = User.lookup(param_name, param_password)
    if not user:
      return HttpResponseForbidden()

    token = Token.create(user)
    token.save()

    json_data = json.dumps({'success': True, 'token': token.secret})
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def logout(request):
  if request.method == 'POST':
    param_token = request.POST['token']

    token = Token.objects.filter(secret=param_token).first()
    if not token:
      return HttpResponseForbidden()

    token.delete()

    json_data = json.dumps({'success': True})
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['POST'])
