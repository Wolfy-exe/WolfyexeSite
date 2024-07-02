from django.http import JsonResponse
from django.shortcuts import render
from .twitchAPI import get_valid_token, search_user
from .orbfy import orbfy
from dotenv import load_dotenv
import requests,os

def home(request):
    return render(request=request, template_name='streamer_orb/home.html', context={'test':"Home Page"})

def search_streamer(request):
    username = request.POST.get('username')
    errors = []
    # Validate the input
    if not username and len(username) < 26:
        return JsonResponse({'error': 'Valid username is required'})
    channels = search_user(username)
    if channels == None:
        return JsonResponse({'error': 'Error: Could not find channels with that username'})
    # If there are errors, return them
    return JsonResponse({'success': 'Search query successful', 'channels': channels, 'count': len(channels)})

def get_image(request):
    username = request.POST.get('username')
    speed = request.POST.get('speed')
    size = request.POST.get('size')
    errors = []
    # Validate the input
    if not username:
        errors.append('Username is required')
    
    try:
        speed = int(speed)
        if speed < 5 or speed > 60:
            errors.append('Speed must be between 5 and 60')
        else:
            speed = 65-speed
    except (TypeError, ValueError):
        errors.append('Speed must be a number')
    
    try:
        size = int(size)
        if size < 20 or size > 300:
            errors.append('Size must be between 20 and 300')
    except (TypeError, ValueError):
        errors.append('Size must be a number')

    # If there are errors, return them
    if errors:
        return JsonResponse({'errors': errors})

    # Get the profile image
    try:
        access_token = get_valid_token()
    except Exception as e:
        return JsonResponse({'error': 'Error: Could not get token'})
    
    load_dotenv()
    if not load_dotenv():
        return JsonResponse({'error': 'Error: Could not load variables'})
    try:
        user_url = 'https://api.twitch.tv/helix/users?login='+str(username)
        user_headers = {
            'Client-Id': os.getenv('TWITCH_CLIENT_ID'),
            'Authorization': 'Bearer '+access_token,
        }
        user_response = requests.get(user_url, headers=user_headers)
        user_data = user_response.json()
        if 'data' in user_data and len(user_data['data']) > 0:
            profile_image_url = user_data['data'][0]['profile_image_url']
            orbfy(profile_image_url, "media/orbs/", username, frame_count=speed, img_size=size)
            return JsonResponse({'success': 'Orb created successfully', 'url': f'/media/orbs/{username}ORB.gif'})
        else:
            print(user_response.json())
            return JsonResponse({'error': 'User not found, please check the username you entered'})
    except Exception as e:
        print(e)
        return JsonResponse({'error': 'Error: Could not get user data'})