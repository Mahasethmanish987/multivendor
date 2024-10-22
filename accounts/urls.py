from  django.urls import path 

from  . import views
app_name='accounts'

urlpatterns=[
    path('',views.myAccount,name='myAccount'),
    path('userRegistration/',views.userRegistration,name='userRegistration'),
    path('login/',views.login_view,name='login'),
    path('logout/',views.logout_view,name='logout'),
    
    path('custDashboard/',views.custDashboard,name='custDashboard'),
    path('vendorDashboard/',views.vendorDashboard,name='vendorDashboard'),
    path('activate/<uidb64>/<token>/',views.activate,name='activate'),
    
    #Forgot Password
    path('forgot_password/',views.forgot_password,name='forgot_password'),
    path('reset_password_validate/<uidb64>/<token>/',views.reset_password_validate,name='reset_password_validate'),
    path('reset_password/',views.reset_password,name='reset_password'),

    
    


]