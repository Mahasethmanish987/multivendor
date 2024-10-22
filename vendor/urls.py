from django.urls import path 
from . import views 
from accounts import views as accountviews 

app_name='vendor'
urlpatterns=[
    path('',accountviews.vendorDashboard,name='vendor'),
    path('registerVendor/',views.registerVendor,name='registerVendor'),
    path('profile/',views.vprofile,name='vprofile'),

]
