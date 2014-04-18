from django.shortcuts import get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ObjectDoesNotExist
import json

from users.models import User
from tokens.models import Token

# Create your views here.
def index(request):
  # TODO: this leaks password
  if request.method == 'GET':
    objs = [x.to_dict() for x in list(User.objects.all())]
    json_data = json.dumps(objs)
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['GET'])

def detail(request, user_id):
  if request.method == 'GET':
    user = get_object_or_404(User, id=user_id)
    json_data = json.dumps(user.to_dict())
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def create(request):
  if request.method == 'POST':
    param_name = request.POST['name']
    param_password = request.POST['password']

    # check if a user exists with the given username
    if User.objects.filter(name=param_name):
      error_data = {'code': 100, 'message': 'username is taken'}
      json_data = json.dumps({'success': False, 'error': error_data})
      return HttpResponse(json_data)

    # create and save a regular user
    user = User.create(param_name, param_password)
    token = Token.create(user)
    token.save()
    user.save()

    # indicate success
    json_data = json.dumps({'success': True, 'user_id': user.id, 'token' : token.secret})
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def delete(request, user_id):
  if request.method == 'DELETE':
    param_secret = request.GET['token']

    target_user = get_object_or_404(User, id=user_id)

    try:
      current_user_token = Token.objects.find(secret=param_secret)
      current_user = current_user_token.user
    except ObjectDoesNotExist:
      return HttpResponseForbidden()

    if current_user.is_admin or current_user == target_user:
      target_user.delete()
      # Once an object is deleted in this manner, all objects with the former as a field are also
      # automatically deleted.
      # In this way, we know that the auth token is automatically removed.

      json_data = json.dumps({'success': True})
      return HttpResponse(json_data)
    else:
      return HttpResponseForbidden()
  else:
    return HttpResponseNotAllowed(['DELETE'])

@csrf_exempt
def change_password(request, user_id):
  if request.method == 'POST':
    param_secret = request.POST['token']
    new_password = request.POST['new_password']

    target_user = get_object_or_404(User, id=user_id)

    try:
      current_user_token = Token.objects.find(secret=param_secret)
      current_user = current_user_token.user
    except ObjectDoesNotExist:
      return HttpResponseForbidden()

    if current_user.is_admin or current_user == target_user:
      target_user.password = new_password
      target_user.save()
      json_data = json.dumps({'success': True})
      return HttpResponse(json_data)
    else:
      return HttpResponseForbidden()
  else:
    return HttpResponseNotAllowed(['POST'])
