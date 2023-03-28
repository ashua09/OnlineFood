from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from django.db.models.fields.related import OneToOneField

# Create your models here.

class UserManager(BaseUserManager):
    def create_user(self, first_name, last_name, username, email, password=None):
        if not email:
            raise ValueError('You must have an email')
        if not username:
            raise ValueError('You must have an username')
        
        user=self.model(
            email = self.normalize_email(email),
            username = username,
            first_name = first_name,
            last_name = last_name
        )

        user.set_password(password)
        user.save(using=self.db)
        return user

    def create_superuser(self, first_name, last_name, username, email, password=None):
        user = self.create_user(
        email = self.normalize_email(email),
        username = username,
        password = password,
        first_name = first_name,
        last_name = last_name
        )

        user.is_admin = True
        user.is_active = True
        user.is_staff = True
        user.is_superadmin = True
        
        user.save(using=self.db)
        return user


class User(AbstractBaseUser):
    VENDOR = 1
    CUSTOMER = 2
    ROLE_CHOICE=(
        (VENDOR,'Vendor'),
        (CUSTOMER,'Customer')
    )

    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    username = models.CharField(unique=True,max_length=100)
    email = models.EmailField(unique=True, max_length=254)
    phone_number = models.CharField(max_length=15)
    role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)

    #required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now_add=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    #Login Field
    USERNAME_FIELD= 'email'
    REQUIRED_FIELDS= ['username','first_name','last_name']

    objects=UserManager()

    def __str__(self):
        return self.email
    def has_perm(self, perm, obj=None):
        return self.is_admin
    def has_module_perms(self, app_label):
        return True

    def get_role(self):
        if self.role == 1:
            user_role = 'Vendor'
        elif self.role == 2:
            user_role = 'Customer'
        return user_role

    def full_name(self):
        return f'{self.first_name} {self.last_name}'
    

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(blank=True, max_length=300)
    profile_picture = models.ImageField(blank=True, null=True, upload_to='users/profile_pictures')
    cover_picture = models.ImageField(blank=True, null=True, upload_to='users/cover_photos')
    city = models.CharField(blank=True, max_length=20)
    state = models.CharField(blank=True, max_length=20)
    country = models.CharField(blank=True, max_length=20)
    pin_code = models.CharField(blank=True, null=True, max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    # longitude = models.CharField(blank=True, null=True ,max_length=20)
    # latitude = models.CharField(blank=True, null=True, max_length=20)

    def __str__(self):
        return self.user.email

    # def full_address(self):
    #     return f'{self.address_line_1} {self.address_line_2}'
