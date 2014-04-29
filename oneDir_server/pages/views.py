from django.shortcuts import render
from django.http import HttpResponse

def index(request):
  with open('pages/templates/index.html') as f:
    return HttpResponse(f.read())

def get_client(request):
  with open('pages/templates/get_client.html') as f:
    return HttpResponse(f.read())

def create_user(request):
  with open('pages/templates/create_user.html') as f:
    return HttpResponse(f.read())

def admin_show_users(request):
  with open('pages/templates/admin_show_users.html') as f:
    return HttpResponse(f.read())

def change_password(request):
  with open('pages/templates/change_password.html') as f:
    return HttpResponse(f.read())

def admin_change_password(request):
  with open('pages/templates/admin_change_password.html') as f:
    return HttpResponse(f.read())

def delete_user(request):
  with open('pages/templates/delete_user.html') as f:
    return HttpResponse(f.read())

def admin_delete_user(request):
  with open('pages/templates/admin_delete_user.html') as f:
    return HttpResponse(f.read())

def show_history(request):
  with open('pages/templates/show_history.html') as f:
    return HttpResponse(f.read())

def admin_show_history(request):
  with open('pages/templates/admin_show_history.html') as f:
    return HttpResponse(f.read())

def show_files(request):
  with open('pages/templates/show_files.html') as f:
    return HttpResponse(f.read())

def admin_show_files(request):
  with open('pages/templates/admin_show_files.html') as f:
    return HttpResponse(f.read())
