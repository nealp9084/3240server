from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from users.models import User
from sync.models import File

# Create your views here.
def index(request):
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
      error_data = {'code': '100', 'message': 'username is taken'}
      json_data = json.dumps({'success': False, 'error': error_data})
      return HttpResponse(json_data)

    # create and save a regular user
    u = User(name=param_name, password=param_password,
             is_admin=False, last_activity=timezone.now())
    u.save()
    # Create the key

    # indicate success
    json_data = json.dumps({'success': True})
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def delete(request, user_id):
  if request.method == 'DELETE':
    current_user_id = request.GET['current_user']
    user = get_object_or_404(User, id=user_id)
    current_user = get_object_or_404(User, id=current_user_id)

    if current_user.is_admin or user == current_user:
      user.delete()
      # optionally delete the user's files
      if 'delete_files' in request.GET and request.GET['delete_files']:
        File.objects.filter(owner=current_user).delete()

      json_data = json.dumps({'success': True})
      return HttpResponse(json_data)
    else:
      return HttpResponseForbidden()
  else:
    return HttpResponseNotAllowed(['DELETE'])

@csrf_exempt
def change_password(request, user_id):
  if request.method == 'POST':
    current_user_id = request.POST['current_user']
    new_password = request.POST['new_password']
    target_user = get_object_or_404(User, id=user_id)
    current_user = get_object_or_404(User, id=current_user_id)

    if current_user.is_admin or current_user == target_user:
      target_user.password = new_password
      target_user.save()
      json_data = json.dumps({'success': True})
      return HttpResponse(json_data)
    else:
      return HttpResponseForbidden()
  else:
    return HttpResponseNotAllowed(['POST'])
