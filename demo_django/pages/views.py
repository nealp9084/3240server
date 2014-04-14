from django.shortcuts import render
from django.http import HttpResponse

def create_user(request):
  with open('pages/templates/create_user.html') as f:
    return HttpResponse(f.read())

def get_client(request):
  with open('pages/templates/get_client.html') as f:
    return HttpResponse(f.read())

def change_password(request):
  with open('pages/templates/change_password.html') as f:
    return HttpResponse(f.read())

def delete_user(request):
  with open('pages/templates/delete_user.html') as f:
    return HttpResponse(f.read())

def show_history(request):
  with open('pages/templates/show_history.html') as f:
    return HttpResponse(f.read())
