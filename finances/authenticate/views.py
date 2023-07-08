from django.shortcuts import render, redirect
import json 
from django.http import JsonResponse, HttpResponse
from django.contrib.auth.models import User
from django.contrib import auth
from validate_email import validate_email
from django.contrib import messages
from django.core.mail import EmailMessage, send_mail
from django.views import View
from django.urls import reverse
from django.utils.encoding import force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site

from .utils import token_generator

def base(request):
    return render(request, "auth/auth_base.html")

def login(request):
    if request.method == "POST":
        user =  auth.authenticate(username= request.POST["username"], password = request.POST["password"])
        if user is not None:
            return render(request, "index.html")
        else:
            context = { "fieldValues": request.POST }
            messages.error(request, "INVALID CREDENTIALS")
            return render(request, "auth/login.html", context)
    return render(request, "auth/login.html")

def signup(request):
    if request.method == "POST":
        userData = {
            "name": request.POST['name'],
            "username": request.POST['username'],
            "email": request.POST["email"],
            "password": request.POST["password"],
        }
        context = { "fieldValues": request.POST }
        if User.objects.filter(username = userData["username"]).exists():
            messages.error(request, "Username Taken")
            return render(request, "auth/signup.html", context)
        
        if User.objects.filter(email = userData["email"]).exists():
            messages.error(request, "Email already in use")
            return render(request, "auth/signup.html", context)
        
        newUser = User.objects.create(first_name = userData["name"], email = userData["email"], username = userData["username"], password = userData["password"])
        newUser.is_active = False
        newUser.save()
        newUser.is_active = False

        uidb64 = urlsafe_base64_encode(force_bytes(newUser.pk))
        domain = get_current_site(request).domain
        link = reverse('activate', kwargs= { 'uidb64' : uidb64, 'token': token_generator.make_token(newUser)})

        emailData = {
            "subject": "Activatoin Mail - SmartFinances",
            "body": "Hello! To activate your account, click on the link:\n" + "http://" + domain + link 
        }

        email = EmailMessage(
            emailData["subject"],
            emailData["body"],
            "noreply@semycolon.com",
            [userData["email"]],
        )
        email.send(fail_silently=False)
        
        return redirect(login)
    else:
        return render(request, "auth/signup.html")

def usernamevalidate(requset):
    data = json.loads(requset.body)
    username = data['username']
    print(username)
    if not str(username).isalnum():
        return JsonResponse({"usernameError": "username can only be alphaNumeric"}, status = 400)
    if User.objects.filter(username = username):
        return JsonResponse({"usernameError": "username Taken"}, status = 409)
    
    return JsonResponse({"usernameValid": True}, status = 200)

def emailvalidate(requset):
    data = json.loads(requset.body)
    email = data['email']
    if not validate_email(email):
        return JsonResponse({"emailError": "email invalid"}, status = 400)
    if User.objects.filter(email = email):
        return JsonResponse({"emailError": "email already in use"}, status = 409)
    
    return JsonResponse({"emailValid": True}, status = 200)

def verify(request, uidb64, token):
    return render(request, 'index.html')