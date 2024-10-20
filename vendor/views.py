from django.shortcuts import render,redirect
from accounts.forms import UserRegistration
from .forms import VendorForm
from accounts.models import User,UserProfile
from django.contrib import messages 
from accounts.utils import send_verification_email

# Create your views here.
def registerVendor(request):

    if request.method=='POST':
        form=UserRegistration(request.POST)
        v_form=VendorForm(request.POST,request.FILES)
        if form.is_valid() and v_form.is_valid():
            first_name=form.cleaned_data['first_name']
            last_name=form.cleaned_data['last_name']
            username=form.cleaned_data['username']
            email=form.cleaned_data['email']
            password=form.cleaned_data['password']
            phone_number=form.cleaned_data['phone_number']
            user=User.objects.create_user(first_name=first_name,last_name=last_name,username=username,email=email,phone_number=phone_number,password=password)
            user.role=User.RESTAURANT
            user.save()
            mail_subject='please activate your account'
            email_template='accounts/account_verification.html'
            send_verification_email(request,user,mail_subject,email_template)

            vendor=v_form.save(commit=False)
            vendor.user=user
            user_profile=UserProfile.objects.get(user=user)
            vendor.user_profile=user_profile
            vendor.save()
            messages.success(request,'vendor registration successful')
            return redirect('myapp:index')
        else:
            context={
                'form':form,
                'v_form':v_form
            }
            return render(request,'vendor/registerVendor.html',context)
    else:
        form=UserRegistration()
        v_form=VendorForm()
        return render(request,'vendor/registerVendor.html',{'form':form,'v_form':v_form})    
        


