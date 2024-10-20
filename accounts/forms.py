from django import forms 
from .models import User 

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


