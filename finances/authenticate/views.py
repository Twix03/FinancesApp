from collections.abc import Callable, Iterable, Mapping
from typing import Any
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
from django.utils.encoding import force_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import PasswordResetTokenGenerator
import threading

class EmailThread(threading.Thread):
    def __init__(self, email):
        self.email = email
        threading.Thread.__init__(self)
    
    def run(self):
        self.email.send(fail_silently=False)

from .utils import token_generator

def login(request):
    if request.method == "POST":
        newuser = auth.authenticate(request, username = request.POST["username"], password = request.POST["password"])
        print("Usrtr data: ",newuser)
        if newuser is not None:
            auth.login(request, newuser)
            return redirect("index")
        else:
            messages.error(request, "errpr")
            return render(request, "auth/login.html")
    else:
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
        
        newUser = User.objects.create_user(first_name = userData["name"], email = userData["email"], username = userData["username"], password = userData["password"])

        print("created Userr : ",newUser.check_password("12345678"))
        
        newUser.is_active = False
        newUser.save()

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
        EmailThread(email).start()
        
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
    try:
        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = id)
        if not token_generator.check_token(user, token):
            messages.info(request, "Account already activated")
            return redirect('login')
        user.is_active = True
        user.save()
        messages.success(request, "Account activated successfully")
        return redirect('index')
    except Exception as ex:
        pass
    
def signout(request):
    auth.logout(request)
    if '_auth_user_id' not in request.session:
        print("SUCCESS")
    else:
        print("Failed")

    return redirect(login)

def reset_password(request):
    if request.method == "POST":
        
        email = request.POST["email"]
        if not validate_email(email):
            messages.warning(request, "Enter a VALID email")
            return redirect('reset_password')
        
        user = User.objects.filter(email = email)

        if user.exists():
            uidb64 = urlsafe_base64_encode(force_bytes(user[0].pk))
            domain = get_current_site(request).domain
            link = reverse('new_password', kwargs= { 'uidb64' : uidb64, 'token': PasswordResetTokenGenerator().make_token(user[0])})

            emailData = {
                "subject": "Password Reset Mail - SmartFinances",
                "body": "Hello! To reset your account, click on the link:\n" + "http://" + domain + link 
            }

            email = EmailMessage(
                emailData["subject"],
                emailData["body"],
                "noreply@semycolon.com",
                [email],
            )
            EmailThread(email).start()
            messages.success(request, "Mail sent successfully, please check your inbox")
            return redirect('reset_password')
        
        else:
            messages.warning(request, "No user exists with given email")
            return redirect('reset_password')
        
    else:
        return render(request, "auth/password-reset.html")
    
def new_password(request, uidb64, token):
    if request.method == "POST":
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]

        if pass1 != pass2:
            messages.error(request, "Passwords do not match")
            return render(request, "auth/resetpassword.html")

        if len(pass1) < 8:
            messages.error(request, "Passwords too short (minimum 8 characters required)")
            return render(request, "auth/resetpassword.html")
        else:
            try:
                id = force_str(urlsafe_base64_decode(uidb64))
                user = User.objects.get(pk = id)
                user.set_password(pass1)
                user.save()
                print("hello")
                messages.success(request, "Password changed successfully")
                return redirect('login')
            except Exception as ex:
                import pdb
                pdb.set_trace()
                messages.error(request, "something went wrong")
                render(request, "auth/resetpassword.html")
    else:
        context = {
            "uidb64": uidb64,
            "token": token,
        }
        print("uidb64--> ", uidb64) 
        print("token--> ", token)

        id = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk = id)
        if not PasswordResetTokenGenerator().check_token(user, token):
            print("wrong-->")
            messages.error(request, "Link already used, generate new link below")
            return redirect('reset_password')
        return render(request, "auth/resetpassword.html", context)