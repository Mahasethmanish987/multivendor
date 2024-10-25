from django.shortcuts import render,redirect,get_object_or_404
from accounts.forms import UserRegistration
from .forms import VendorForm
from accounts.models import User,UserProfile
from django.contrib import messages 
from accounts.utils import send_verification_email
from django.contrib.auth.decorators import login_required,user_passes_test
from accounts.forms import UserProfileForm 
from .models import vendor
from menu.models import Category,FoodItem
from accounts.views import check_role_vendor
from menu.forms import CategoryForm
from django.template.defaultfilters import slugify
def get_vendor(request):
    vendor1=vendor.objects.get(user=request.user)
    return vendor1
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
        
@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    profile=get_object_or_404(UserProfile,user=request.user)
    vendor1=get_object_or_404(vendor,user=request.user)

    if request.method=='POST':
        profile_form=UserProfileForm(request.POST,request.FILES,instance=profile)
        vendor_form=VendorForm(request.POST,request.FILES,instance=vendor1)

        if profile_form.is_valid() and vendor_form.is_valid():
            profile_form.save()
            vendor_form.save()
            messages.success(request,'settings updated')
            return redirect('vendor:vprofile')
        
        else:
            context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'vendor1':vendor1,
        'profile':profile
    }
            return render(request,'vendor/vprofile.html',context)
    else:
     profile_form=UserProfileForm(instance=profile)
     vendor_form=VendorForm(instance=vendor1)
     context={
        'profile_form':profile_form,
        'vendor_form':vendor_form,
        'vendor1':vendor1,
        'profile':profile
    }
     return render(request,'vendor/vprofile.html',context)
@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def menu_builder(request):
    vendor1=get_vendor(request)
    categories=Category.objects.filter(vendor=vendor1)
    context={
        'categories':categories
    }
    return render(request,'vendor/menu_builder.html',context)
@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def fooditems_by_category(request,pk=None):
    vendor1=get_vendor(request)
    category=get_object_or_404(Category,pk=pk)
    fooditems=FoodItem.objects.filter(vendor=vendor1,category=category)
    context={
        'fooditems':fooditems,
        'category':category
    }
    return render(request,'vendor/fooditems_by_category.html',context)

@login_required(login_url='accounts:login')
@user_passes_test(check_role_vendor)
def add_category(request):
    
    if request.method=='POST':
        form=CategoryForm(request.POST)
        if form.is_valid():
            category=form.save(commit=False)
            category.vendor=get_vendor(request)
            category_name=form.cleaned_data['category_name']
            category.slug=slugify(category_name)


            form.save()
            messages.success(request,'Category added successfully')
            return redirect('vendor:menu_builder')
        else:
            return render(request,'vendor/add_category.html',{'form':form})
    
    else:        
      form = CategoryForm()
      context={
        'form':form
    }
    return render(request,'vendor/add_category.html',context)


def edit_category(request,pk=None):

    category=get_object_or_404(Category,pk=pk)
    if request.method=='POST':
        form=CategoryForm(request.POST,instance=category)
        if form.is_valid():
           category_name=form.cleaned_data['category_name']
           category=form.save(commit=False)
           category.vendor=get_vendor(request)
           category.slug=slugify(category_name)
           category.save()
           messages.success(request,'your form updated successfully')
           return redirect('vendor:menu_builder')

        else:
            return render(request,'vendor/edit_category.html',{'form':form,'category':category}) 
    else:
        form=CategoryForm(instance=category)      

    return render(request,'vendor/edit_category.html',{'form':form,'category':category})


def delete_category(request,pk):
    category=Category.objects.get(pk=pk)
    category.delete()
    messages.success(request,'the category has deleted')
    return redirect('vendor:menu_builder')