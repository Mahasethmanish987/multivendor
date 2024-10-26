from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth import authenticate,login ,logout
from .forms import UserRegistration 
from .models import User
from django.contrib.auth.decorators import login_required,user_passes_test
from .utils import detectUser
from django.core.exceptions import PermissionDenied
from .utils import send_verification_email
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from vendor.models import vendor
# Create your views here.
from django.urls import reverse

def check_role_customer(user):
    if user.role==2:
        return True
    else:
        raise PermissionDenied
    
def check_role_vendor(user):
    if user.role==1:
        return True
    else:
        raise PermissionDenied    
def userRegistration(request):
    if request.user.is_authenticated:
        messages.info(request,'You are already logged in ')
        return redirect('myapp:index')
    
    if request.method=='POST':
        form=UserRegistration(request.POST)
        if form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            phone_number=form.cleaned_data['phone_number']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,phone_number=phone_number,password=password)
            user.role=User.CUSTOMER
            user.save()
            mail_subject='please activate your account'
            email_template='accounts/account_verification.html'
            send_verification_email(request,user,mail_subject,email_template)


            messages.info(request,'user has been successfully registered and verification email is send to your email address')

            return redirect('myapp:index')
        else:
            return render(request,'accounts/userRegistration.html',{'form':form})
    else:
        form=UserRegistration()
        return render(request,'accounts/userRegistration.html',{'form':form})    
        

def login_view(request):
    if request.user.is_authenticated:
        messages.info(request,'You are already logged in ')
        return redirect('myapp:index')
    
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        user=authenticate(request,email=email,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'account LoggedIn')
            return redirect('accounts:myAccount')
        else:
            messages.error(request,'Invalid credentials')
            return render(request,'accounts/login.html')
        
    else:
        return render(request,'accounts/login.html')    


def logout_view(request):
    logout(request)
    messages.info(request,'you have been logged out')
    return redirect('accounts:login')

@login_required(login_url='accounts:myapp')
def myAccount(request):
    user=request.user
    redirectUrl=detectUser(user)
    if redirectUrl=='admin:index':
        return redirect(reverse(redirectUrl))
    else:
      return redirect(reverse(f'accounts:{redirectUrl}'))


@login_required(login_url='accounts:login')
@user_passes_test(check_role_customer)
def custDashboard(request):
    return render(request,'accounts/custDashboard.html')

@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def vendorDashboard(request):
   return render(request,'vendor/vendorDashboard.html')


def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
       user.is_active=True
       user.save()
       messages.success(request,'congratulations user has been activated')
       return redirect('accounts:login')
    else:
        messages.error(request,'invalid link')
        return redirect('myapp:index')   


def forgot_password(request):
    if request.user.is_authenticated:
        messages.info(request,'User is already logged in')
        return redirect('myapp:index')
    if request.method=='POST':
        email=request.POST.get('email')
        if User.objects.filter(email=email).exists():
            user=User.objects.get(email=email)


            mail_subject='Reset your password'
            email_template='accounts/reset_password_link.html'
            send_verification_email(request,user,mail_subject,email_template)
            messages.success(request,'password reset link send successfully')
            return redirect('accounts:login')
        
        else:
            messages.error(request,'no such email found')
            return redirect('accounts:forgot_password')
    return render(request,'accounts/forget_password.html')    


def reset_password_validate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        request.session['uid']=uid 
        messages.info(request,'please reset your password')
        return redirect('accounts:reset_password')
    else:
        messages.error(request,'these link has been expired')
        return redirect('accounts:forgot_password')        


def reset_password(request):
    if request.method=='POST':
        password=request.POST.get('password')
        confirm_password=request.POST.get('confirm_password')
        if password==confirm_password:
            pk=request.session.get('uid')
            if pk is None:
                messages.error(request,'session expired or invalid')
                return redirect('accounts:forgot_password')
            
            try:
              user=User.objects.get(pk=pk)

            except User.DoesNotExist:
                messages.error(request,'User Not Found')
                return redirect('accounts:forgot_password')
            
            user.set_password(password)
            user.is_active=True
            user.save()
            messages.success(request,'password reset completed')
            return redirect('accounts:login')
        else:
            messages.error(request,'password and confirm password does not match')
            return redirect('accounts:reset_password.html')

    return render(request,'accounts/reset_password.html')    