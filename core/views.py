from django.shortcuts import render
from django.conf import settings

def home(request):
    return render(
        request=request, 
        template_name='home.html',
        context={
            "debug": settings.DEBUG
            }
        )