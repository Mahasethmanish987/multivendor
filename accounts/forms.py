from django import forms 
from .models import User,UserProfile
from .validators import allow_only_image_validator

class UserRegistration(forms.ModelForm):
    password=forms.CharField(widget=forms.PasswordInput(),min_length=8)
    confirm_password=forms.CharField(widget=forms.PasswordInput(),min_length=8)
    class Meta:
        model=User
        fields=['email','username','first_name','last_name','phone_number','password']

    def clean(self):
        cleaned_data=super().clean()
        password=cleaned_data.get('password')
        confirm_password=cleaned_data.get('confirm_password')

        if password and confirm_password and password!=confirm_password:
            raise forms.ValidationError('passwords do not match')

        return cleaned_data  

class UserProfileForm(forms.ModelForm):
    address=forms.CharField(widget=forms.TextInput(attrs={'placeholder':'start typing..','required':'required'}))
    profile_picture=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_image_validator])
    cover_photo=forms.FileField(widget=forms.FileInput(attrs={'class':'btn btn-info'}),validators=[allow_only_image_validator])
    # latitude=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    # longitude=forms.CharField(widget=forms.TextInput(attrs={'readonly':'readonly'}))
    class Meta:
        model=UserProfile   
        fields=['profile_picture','cover_photo','address','country','state','pin_code','latitude','longitude']   

    
    def __init__(self,*args,**kwargs):
        super(UserProfileForm,self).__init__(*args,**kwargs)
        for field in self.fields:
            if field=='latitude' or field=='longitude':
                self.fields[field].widget.attrs['readonly']='readonly'
