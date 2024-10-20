from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.conf import settings 
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
def detectUser(user):
    if user.role==1:
        redirectUrl='vendorDashboard'
    elif user.role==2:
        redirectUrl='custDashboard'
    elif user.role==None and user.is_superadmin:
        redirectUrl='/admin'   
    return redirectUrl     


def send_verification_email(request,user,mail_subject,email_template,):
    from_email=settings.DEFAULT_FROM_EMAIL
    print(from_email)
    current_site=get_current_site(request)
    print(current_site)
    mail_subject=mail_subject
    message=render_to_string(email_template,{
       'user':user,
       'domain':current_site,
       'uid':urlsafe_base64_encode(force_bytes(user.pk)),
       'token':default_token_generator.make_token(user)
    })
    to_email=user.email
    mail=EmailMessage(mail_subject,message,from_email,to=[to_email])
    mail.send()
    
    