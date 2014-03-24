from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
import json

from sync.models import File

def index(request):
  if request.method == 'GET':
    objs = [x.to_dict() for x in list(File.objects.all())]
    json_data = json.dumps(objs)
    return HttpResponse(json_data)
  else:
    return HttpResponseNotAllowed(['GET'])

def create_server_file(request):
  # Put something in the db.
  if request.method == 'POST':
    param_local_path = request.POST['local_path']
    param_last_modified = request.POST['last_modified']
    param_server_path = request.POST['server_path']
    param_owner = request.POST['owner']
    
    f = File(local_path=param_local_path,last_modified=param_last_modified, \
      server_path=param_server_path,owner=param_owner)
    f.save()
    
    # If user directory doesn't exist:
    #   Create User Directory
    # Move file from client to user directory on server.
    # File name should be timestamp

    json_data = json.dumps({'success': True, 'file_id': f.id})
    return HttpResponse(json_data)   
  else:
    return HttpResponseNotAllowed(['POST'])

def update_file(request, file_id):
  # Updates the file on the server.
  if request.method == 'POST':
    file = get_object_or_404(File, id=file_id)
    param_last_modified = request.POST['last_modified']
    t = file.is_sync_needed(param_last_modified)
    
    # Conditions based off of sync code.
    if(t == 0):
      json_data = json.dumps({'success': False, 'file_id': f.id, 'code' : t})
      return HttpResponse(json_data) 
    else:
      param_local_path = request.POST['local_path']
      param_server_path = request.POST['server_path']
      param_owner = request.POST['owner']
      if(t == 1):
        # Replace file on server side.
        
          f = File(local_path=param_local_path,last_modified=param_last_modified, \
          server_path=param_server_path,owner=param_owner)
        f.save()     
        json_data = json.dumps({'success': True, 'file_id': f.id, 'code' : t})
        return HttpResponse(json_data)
      else: # t == 2
        # Replace file on client side.

        f = File(local_path=param_local_path,last_modified=param_last_modified, \
          server_path=param_server_path,owner=param_owner)
        f.save() 
        json_data = json.dumps({'success': True, 'file_id': f.id, 'code' : t})
        return HttpResponse(json_data) 

def serve_file(request, file_id):
  # Serves the file to the client.
  if request.method == 'GET':
    # If file exists: get_object_or_404()
    #   Send
  else
    return HttpResponseNotAllowed(['GET'])
