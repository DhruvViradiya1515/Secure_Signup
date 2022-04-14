from django.contrib.sites.shortcuts import get_current_site
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.core.mail import send_mail,EmailMessage
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
import numpy as np
import authentication
from SE import settings
from . tokens import generate_token
from authentication.models import Contact
from datetime import datetime
import re
special_chars = ['!','#','?','$','&']
# Create your views here.
def home(request):
    return render(request,'index.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        desc = request.POST.get("desc")
        contact = Contact(name=name,email=email,phone=phone,desc=desc,date = datetime.today())
        contact.save()
        messages.success(request,"Your message has been sent !!")

    # return HttpResponse("Hello there, this is contact")
    return render(request,"contact.html")

def about(request):
    # return HttpResponse("Hello there, this is about")
    return render(request,"about.html")

def signup(request):

    if(request.method == "POST"):
        username = request.POST['username']
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        pin = request.POST['pin']
        phone = request.POST['phone']
        if User.objects.filter(username=username):
            messages.error(request,"User_name already exist Please try some otther username")
            return redirect('home')

        if User.objects.filter(email=email):
            messages.error(request,"Email already exist")
            return redirect('home')
        
        if len(username) > 10:
            messages.error(request,"User name must be less than 10 characters")
            return redirect('home')

        if( len(pin) != 6):
            messages.error(request,"Pin must be of length 6")
            return redirect('home')

        for i in pass1:
            if(i in special_chars):
                t1 = pass1.count(i)
                if(t1 != 1):
                    messages.error(request,"password should contain at least one special character among {'!','#','?','$','&'}")
                    return redirect('home')

        if( len(pass1)<8 or len(pass1)>13):
            messages.error(request,"Pin must be of length between 8 to 13")
            return redirect('home')
        if pass1 != pass2:
            messages.error(request,"Passsword didn't match")
            return redirect('home')

        if not username.isalnum():
            messages.error(request,"Username must be alpha numberic")
            return redirect('home')

        if(len(re.findall(r'[A-Z]',pass1))<1):
            messages.error(request,"Passwors should contain atleast one upper case")
            return redirect('home')
        
        if(len(re.findall(r'[a-z]',pass1))<1):
            messages.error(request,"Passwors should contain atleast one upper case")
            return redirect('home')

        myuser = User.objects.create_user(username,email,pass1)
        myuser.first_name = fname
        myuser.last_name = lname
        myuser.pin = pin
        myuser.is_active = False
        myuser.save()

        messages.success(request,'Hello there, Your account has been succcesfully created. We have sent you an confirmation email, please confirm your email in order to activate your account.')


        subject = 'Welcome to '
        message = f"Hello {myuser.first_name} !!\n\tWelcome, Thanks for visiting our website. \n We have also sent you a confirmation email, please confirm your email in order to activate your account. \n\n Thanking you"
        from_email = settings.EMAIL_HOST_USER
        to_list = [myuser.email]
        send_mail(subject,message,from_email,to_list,fail_silently=True)

        current_site = get_current_site(request)
        email_subject = 'Confirm your Email at '
        message2 = render_to_string('email_confirmation.html',
            {'name':myuser.first_name,'domain':current_site.domain,'uid': urlsafe_base64_encode(force_bytes(myuser.pk)),
            'token': generate_token.make_token(myuser)}) 

        email = EmailMessage(email_subject,message2,settings.EMAIL_HOST_USER,[myuser.email],)
        email.fail_silently = True
        email.send()

        return redirect('Login')

    return render(request,'signup.html')


def activate(request,uidb64,token):

    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        myuser = User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        myuser = None

    if(myuser is not None and generate_token.check_token(myuser,token)):
        myuser.is_active = True
        myuser.save()
        login(request,myuser)
        return redirect('home')
    else:
        return redirect(request,'activation_failed.html')


def Login(request):

    if(request.method == "POST"):
        username = request.POST['username']
        pass1 = request.POST['pass1']
        pin = request.POST['pin']
        user = authenticate(username=username,password=pass1)
        
        if(user is not None):
            login(request,user)
            fname = user.first_name
            return render(request,'index.html',{'fname':fname})
        
        else:
            messages.error(request,'Your are breaking my heart, you\'r not using the same credentials')
            return redirect('home')

    return render(request,'Login.html')

def signout(request):
    logout(request)
    messages.success(request,"You've logged out succesfully, Hope we'll meet again")
    return redirect('home')