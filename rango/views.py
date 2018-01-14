from django.shortcuts import render
from django.http import HttpResponse

def index(request):
	return HttpResponse("Howdy yall! This is from Rango.")

def about(request):
    return HttpResponse('Rango says here is the about page.')