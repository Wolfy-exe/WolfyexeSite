from django.http import JsonResponse
from django.shortcuts import render
from .tokenhandler import get_valid_token
from dotenv import load_dotenv
import requests,os

def home(request):
    return render(request=request, template_name='streamer_orb/home.html', context={'test':"Home Page"})

def get_image(request):
    access_token = get_valid_token()
    load_dotenv()
    username = request.POST.get('username')
    user_url = 'https://api.twitch.tv/helix/users?login='+str(username)
    user_headers = {
        'Client-Id': os.getenv('TWITCH_CLIENT_ID'),
        'Authorization': 'Bearer '+access_token,
    }

    user_response = requests.get(user_url, headers=user_headers)
    user_data = user_response.json()
    if 'data' in user_data and len(user_data['data']) > 0:
        profile_image_url = user_data['data'][0]['profile_image_url']
        return JsonResponse({'profile_image_url': profile_image_url})
    else:
        print(user_response.json())
        return JsonResponse({'error': 'No user data found'})