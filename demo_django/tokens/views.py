from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json

from users.models import User
from tokens.models import Token

# TODO: horribly unsecure
def index(request):
  if request.method == 'GET':
    objs = [x.to_dict() for x in list(Token.objects.all())]
    json_data = json.dumps(objs)
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['GET'])

# TODO: what happens when you submit invalid creds?
# DoesNotExist of ObjectDoesNotExist
@csrf_exempt
def login(request):
  if request.method == 'POST':
    param_name = request.POST['name']
    param_password = request.POST['password']

    try:
      user = User.objects.get(name=param_name, password=param_password)
    except ObjectDoesNotExist:
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

    try:
      token = Token.get(secret=param_token)
    except ObjectDoesNotExist:
      return HttpResponseForbidden()

    token.delete()

    json_data = json.dumps({'success': True})
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['POST'])
