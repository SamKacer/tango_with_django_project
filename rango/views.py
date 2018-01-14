from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse('Howdy yall! This is from Rango. <br/> <a href="/rango/about/"> about </a>')

def about(request):
    return HttpResponse('Rango says here is the about page. <br/> <a href="/rango/"> index </a>')
    