from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from sync.models import File
from users.models import User

def index(request):
  if request.method == 'GET':
    # very unsecure, access token pls
    current_user = request.GET['current_user']
    objs = [x.to_dict() for x in list(File.objects.all().filter(owner=current_user))]
    json_data = json.dumps(objs)
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def create_server_file(request):
  # Put something in the db.
  if request.method == 'POST':
    # very unsecure, access token pls
    current_user_id = request.POST['current_user']
    current_user = get_object_or_404(User, id=current_user_id)
    param_local_path = request.POST['local_path']
    param_last_modified = request.POST['last_modified']
    param_file_data = request.POST['file_data']
    
    f = File(local_path=param_local_path,last_modified=param_last_modified,
      file_data=param_file_data,owner=current_user)
    f.save()

    current_user.last_activity = timezone.now()
    current_user.save()

    # Move file from client to user directory on server.
    # File name should be timestamp

    json_data = json.dumps({'success': True, 'file_id': f.id})
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def update_file(request, file_id):
  # Updates the file on the server.
  if request.method == 'POST':
    current_user_id = request.POST['current_user']
    file = get_object_or_404(File, id=file_id)
    current_user = get_object_or_404(User, id=current_user_id)
    param_last_modified = request.POST['last_modified']
    t = file.is_sync_needed(param_last_modified)
    
    # Conditions based off of sync code.
    if t == 0:
      json_data = json.dumps({'success': False, 'file_id': file.id, 'code' : t})
      return HttpResponse(json_data) 
    else:
      param_local_path = request.POST['local_path']
      param_file_data = request.POST['file_data']
      param_owner = request.POST['owner']
      if t == 1:
        # Update file on server side.
        file.sync(param_last_modified, param_file_data)
        file.save()
        current_user.last_activity = timezone.now()
        current_user.save()
        json_data = json.dumps({'success': True, 'file_id': file.id, 'code' : t})
        return HttpResponse(json_data)
      else: # t == 2
        # Replace file on client side.
        json_data = json.dumps({'success': True, 'file_id': file.id, 'code' : t, 'file_info' : {'file_data' : file.file_data, 'file_timestamp' : file.last_modified}})
        return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['POST'])

def serve_file(request, file_id):
  # Serves the file to the client.
  if request.method == 'GET':
    current_user_id = request.GET['current_user']
    file = get_object_or_404(File, id=file_id)
    current_user = get_object_or_404(User, id=current_user_id)

    if current_user.is_admin or file.owner == current_user:
      return HttpResponse(str(file.file_data))
    else:
      return HttpResponseForbidden()
  else:
    return HttpResponseNotAllowed(['GET'])

@csrf_exempt
def delete_file(request, file_id):
  # Deletes the file from the server.
  if request.method == 'DELETE':
    current_user_id = request.GET['current_user']
    file = get_object_or_404(File, id=file_id)
    current_user = get_object_or_404(User, id=current_user_id)

    if current_user.is_admin or file.owner == current_user:
      file.delete()
      current_user.last_activity = timezone.now()
      current_user.save()
      json_data = {'success': True}
      return HttpResponse(json.dumps(json_data))
    else:
      return HttpResponseForbidden()
  else:
    return HttpResponseNotAllowed(['DELETE'])
