from django.shortcuts import render

# Create your views here.

def homepage(request):
    return render(request, 'tips/homepage.html')

def other(request):
    return render(request, 'tips/other.html')
