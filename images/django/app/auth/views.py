from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

from django.shortcuts import redirect
import os
import requests
from django.http import JsonResponse

def redirect_oauth(request):
    code = request.GET.get('code', '')
    if code:
        url = 'https://api.intra.42.fr/oauth/token'
        postdata = {
            'grant_type': 'authorization_code',
            'client_id': 'u-s4t2ud-888abf99e7a96317ce8952769a0be4b4c4a092bed5f52d27b85ae3b989536a15',
            'client_secret': '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',
            'code': code,
            'redirect_uri': 'https://localhost/auth',
            }
        response = requests.post(url, json=postdata)
        data = response.json()
        if data.get('access_token') is None:
            # "error": "invalid_grant",
            # "error_description": "The provided authorization grant is invalid, expired, revoked, does not match the redirection URI used in the authorization request, or was issued to another client."
            return JsonResponse(data)

        # "access_token": "559ee583ed4cd618cccc96920e9f282b23eaf0a258e80a531e88570b519ed65d",
        # "token_type": "bearer",
        # "expires_in": 7200,
        # "refresh_token": "bf44e4c3d672a3adf02bd7aeb32b549abe76cbd150b2c6979a83c0f8061c083d",
        # "scope": "public",
        # "created_at": 1701843554,
        # "secret_valid_until": 1704207237
        response = requests.get('https://api.intra.42.fr/v2/me?access_token=' + data['access_token'])
        data = response.json()
        if data.get('login') is None:
            return HttpResponse('login not found')
        request.session['login'] = data['login']
        # return JsonResponse(data)
        return redirect("me")
    else:
        error = request.GET.get('error', '')
        if error:
            # ?error=access_denied&error_description=The+resource+owner+or+authorization+server+denied+the+request.
            return redirect("/")
        else:
            return redirect(os.environ.get('OAUTH_URL'))

def receive_oauth_code(request):
    return redirect(os.environ.get('OAUTH_URL'))

def logout(request):
    request.session.flush()
    return redirect("/")

def me(request):
    return render(request, 'me.html', {'login': request.session.get('login')})
    return HttpResponse(request.session.get('login'))