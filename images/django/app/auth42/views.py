from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, logout as auth_logout

# Create your views here.
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from urllib.parse import quote
import os
import requests

client_id = os.environ['CLIENT_ID']
client_secret = os.environ['CLIENT_SECRET']

def login_as(request, username):
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        user = User.objects.create_user(username=username)
        user.save()
    auth_login(request, user)

def login_view(request):
    if 'mock' in request.GET:
        username = request.GET['mock']
        # TODO: validate username
        login_as(request, username)
        return redirect(reverse("home"))

    if request.get_host() == '127.0.0.1:8000':
        # for local development
        redirect_url = 'http://' + request.get_host() + reverse('login')
    else:
        # force https proxy (nginx/ngrok) instead of request.scheme
        redirect_url = 'https://' + request.get_host() + reverse('login')

    if 'code' in request.GET:
        postdata = {
            'grant_type': 'authorization_code',
            'client_id': client_id,
            'client_secret': client_secret,
            'code': request.GET['code'],
            'redirect_uri': redirect_url,
        }
        try:
            response = requests.post('https://api.intra.42.fr/oauth/token', json=postdata)
            data = response.json()
            if 'error_description' in data:
                # expired secret, please regenerate
                return redirect(reverse('home') + '?' + request.GET.urlencode())
            access_token = data['access_token']
            response = requests.get('https://api.intra.42.fr/v2/me?access_token=' + access_token)
            data = response.json()
            if 'error_description' in data:
                # expired code, please relogin
                return redirect(reverse('home') + '?' + request.GET.urlencode())
            username = data['login']
            login_as(request, username)
            return redirect(reverse("home"))
        except Exception as e:
            return HttpResponse(e)
    
    if 'error_description' in request.GET:
        # user cancels auth
        return redirect(reverse('home') + '?' + request.GET.urlencode())

    auth_url = (
        'https://api.intra.42.fr/oauth/authorize'
        '?client_id=' + client_id +
        '&redirect_uri=' + quote(redirect_url, safe='') +
        '&response_type=code')
    return redirect(auth_url)

def logout_view(request):
    auth_logout(request)
    return redirect(reverse('home'))
