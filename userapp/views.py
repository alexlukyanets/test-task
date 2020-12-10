from django.http import JsonResponse
from django.utils.datastructures import MultiValueDictKeyError
from rest_framework.authtoken.models import Token
from .models import User
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate


@csrf_exempt
def signup(request):
    if request.method == 'POST':
        try:
            user = User.objects.create_user(request.POST['username'],
                                            password=request.POST['password'])
            user.save()
            token = Token.objects.create(user=user)
            return JsonResponse({'token': str(token)}, status=201)
        except IntegrityError:
            return JsonResponse(({'error': 'That username has already been taken. Please choose a new username'}),
                                status=401)
        except MultiValueDictKeyError:
            return JsonResponse(({'error': 'Please user json data in request body'}), status=401)

    else:
        return JsonResponse(({'error': 'Use POST method for authorization'}), status=401)


@csrf_exempt
def login(request):
    if request.method == 'POST':
        try:
            user = authenticate(request, username=request.POST['username'],
                                password=request.POST['password'])
            if user is None:
                return JsonResponse(({'error': 'Check username or password'}),
                                    status=401)
            else:
                token = Token.objects.get(user=user)
                return JsonResponse({'token': str(token)}, status=200)
        except MultiValueDictKeyError:
            return JsonResponse(({'error': 'Please user json data in request body'}), status=401)
    else:
        return JsonResponse(({'error': 'Use POST method for login'}),
                            status=401)
