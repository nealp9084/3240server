from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json
import dateutil.parser

from sync.models import File, History
from users.models import User

def index(request):
  if request.method == 'GET':
    # very unsecure, access token pls
    current_user_id = request.GET['current_user']
    current_user = get_object_or_404(User, id=current_user_id)

    if current_user.is_admin:
      objs = [x.to_dict() for x in list(File.objects.all())]
    else:
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
    param_local_path = request.POST['local_path']
    param_last_modified = request.POST['last_modified']
    param_file_data = request.POST['file_data']

    current_user = get_object_or_404(User, id=current_user_id)

    # check if the file already exists
    if File.objects.filter(owner=current_user, local_path=param_local_path):
      error_data = {'code': 200, 'message': 'file already exists'}
      json_data = json.dumps({'success': False, 'error': error_data})
      return HttpResponse(json_data)

    # is the timestamp valid?
    try:
      last_modified = dateutil.parser.parse(param_last_modified)
    except:
      return HttpResponseBadRequest()

    # create and save the file record to the database
    file = File.create(param_local_path, last_modified, param_file_data,
                       current_user)
    file.save()

    # update metadata and log this transaction
    current_user.bytes_transferred += file.size
    current_user.save()
    History.log_creation(current_user, file)

    json_data = json.dumps({'success': True, 'file_id': file.id})
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['POST'])

@csrf_exempt
def update_file(request, file_id):
  # Updates the file on the server.
  if request.method == 'POST':
    param_current_user_id = request.POST['current_user']
    param_last_modified = request.POST['last_modified']
    # param_local_path = request.POST['local_path']
    param_file_data = request.POST['file_data']

    file = get_object_or_404(File, id=file_id)
    current_user = get_object_or_404(User, id=param_current_user_id)

    # workaround for possibly-faulty client code
    if 'local_path' in request.POST:
      param_local_path = request.POST['local_path']
    else:
      param_local_path = file.local_path

    # does the current user have the right to update this file?
    if not (current_user.is_admin or current_user == file.owner):
      return HttpResponseForbidden()

    # is the timestamp valid?
    try:
      user_timestamp = dateutil.parser.parse(param_last_modified)
    except:
      return HttpResponseBadRequest()

    # determine which direction we have to sync:
    # no direction, OR
    # client -> server, OR
    # server -> client
    sync_code = file.is_sync_needed(user_timestamp)
    
    # Conditions based off of sync code.
    if sync_code == 0:
      error_data = {'code': 210, 'message': 'file is already up-to-date'}
      json_data = json.dumps({'success': False, 'error': error_data})
      return HttpResponse(json_data) 
    else:
      if sync_code == 1:
        # Update file on server side.
        file.sync(user_timestamp, param_file_data, param_local_path)
        file.save()

        current_user.bytes_transferred += file.size
        current_user.save()
        History.log_update(current_user, file)

        json_data = json.dumps({'success': True})
        return HttpResponse(json_data)
      else:
        # Replace file on client side.
        error_data = {'code': 212,
                      'message': 'the file you sent is older than the one on the server'}
        json_data = json.dumps({'success': False, 'error': error_data})
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
      current_user.bytes_transferred += file.size
      current_user.save()
      History.log_retrieval(current_user, file)

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

      History.log_deletion(current_user, file)
      current_user.save()

      json_data = json.dumps({'success': True})
      return HttpResponse(json_data)
    else:
      return HttpResponseForbidden()
  else:
    return HttpResponseNotAllowed(['DELETE'])
