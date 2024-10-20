from django.db import models
from django.contrib.auth.models import AbstractBaseUser,BaseUserManager

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self,first_name,last_name,username,email,phone_number,password=None):
        if not email:
            raise ValueError('User must have email address')
        if not username:
            raise ValueError('user must haver username')
        
        user=self.model(
            email=self.normalize_email(email),
                        username=username,
                        first_name=first_name,
                        last_name=last_name,
                        phone_number=phone_number
                        )
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self,first_name,username,email,last_name,phone_number,password=None):

        user=self.create_user(
            email=self.normalize_email(email),
            username=username,
            first_name=first_name,
            last_name=last_name,
            password=password,
            phone_number=phone_number
        )
        user.is_admin=True
        user.is_active=True
        user.is_staff=True
        user.is_superadmin=True
        user.save(using=self._db)

        return user 
    
    def get_by_natural_key(self,email):
        return self.get(email=email)

class User(AbstractBaseUser):
    RESTAURANT=1
    CUSTOMER=2
    ROLE_CHOICE=(
        (RESTAURANT,'Restaurant'),
        (CUSTOMER,'Customer')
    )    
    first_name=models.CharField(max_length=50)
    last_name=models.CharField(max_length=50)
    username=models.CharField(max_length=50 ,unique=True)
    email=models.EmailField(max_length=100,unique=True)
    phone_number=models.CharField(max_length=20,unique=True)
    role=models.PositiveSmallIntegerField(choices=ROLE_CHOICE,blank=True,null=True)


    #REQUIRED FIELDS

    date_joined=models.DateTimeField(auto_now_add=True)
    last_login=models.DateTimeField(auto_now=True)
    modified_at=models.DateTimeField(auto_now=True)
    is_admin=models.BooleanField(default=False)
    is_staff=models.BooleanField(default=False)
    is_active=models.BooleanField(default=False)
    is_superadmin=models.BooleanField(default=False)

    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username','first_name','last_name','phone_number']
    objects=UserManager()

    def __str__(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return self.is_admin 
    def has_module_perms(self,app_label):
        return True
    def get_role(self):

        if self.role==self.RESTAURANT:
            return 'Restaurant'
        elif self.role==self.CUSTOMER:
            return 'Customer'
        
        else:
            return 'unknown'

class UserProfile(models.Model):
    user=models.OneToOneField(User,on_delete=models.CASCADE)
    profile_picture=models.ImageField(upload_to='users/profile_picture',blank=True,null=True)
    cover_photo=models.ImageField(upload_to='users/cover_photo',blank=True,null=True)
    address_line1=models.CharField(max_length=50,blank=True,null=True) 
    address_line2=models.CharField(max_length=50,blank=True,null=True) 
    country=models.CharField(max_length=50,blank=True,null=True)
    state=models.CharField(max_length=50,blank=True,null=True) 
    pin_code=models.CharField(max_length=50,blank=True,null=True) 
    longitude=models.CharField(max_length=50,blank=True,null=True) 
    latitude=models.CharField(max_length=50,blank=True,null=True) 
    created_at=models.DateTimeField(auto_now_add=True)
    modified_at=models.DateTimeField(auto_now=True) 

    def __str__(self):
        return self.user.email

            
    
        
        