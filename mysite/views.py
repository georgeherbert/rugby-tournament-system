# render used to return HTML responses
from django.shortcuts import render

# Provides user with site homepage
def index(request):
    return render(request, "index.html")
