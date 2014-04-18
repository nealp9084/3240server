from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from users.models import User
from tokens.models import Token
import json


# TODO: horribly unsecure
def index(request):
  if request.method == 'GET':
    objs = [x.to_dict() for x in list(Token.objects.all())]
    json_data = json.dumps(objs)
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['GET'])


@csrf_exempt
def login(request):
  if request.method == 'POST':
    param_name = request.POST['name']
    param_password = request.POST['password']

    user = User.objects.get(name=param_name, password=param_password)

    if user:
      token = Token.create(user)
      token.save()

      json_data = json.dumps({'success': True, 'token': token.secret})
      return HttpResponse(json_data)
    else:
      return HttpResponseForbidden()
  else:
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def logout(request):
  if request.method == 'POST':
    param_token = request.POST['token']
    token = get_object_or_404(Token, secret=param_token)

    token.delete()

    json_data = json.dumps({'success': True})
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['POST'])
