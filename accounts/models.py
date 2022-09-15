from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)


class AccountManager(BaseUserManager):
    def create_user(self, email,mobile,first_name,last_name, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError('User must have an email address')
        if not mobile:
            raise ValueError('User must have a mobile number')
        user = self.model(
            first_name  = first_name,
            last_name   = last_name,
            email       = self.normalize_email(email),
            mobile      = mobile,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self,first_name,last_name,mobile, email, password):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            first_name=first_name,
            last_name=last_name,
            email=email,
            mobile=mobile,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    first_name = models.CharField(max_length=50)
    last_name  = models.CharField(max_length=50)
    mobile     = models.CharField(max_length=10, null=True, unique=True)
    email = models.EmailField(
        max_length=255,
        unique=True,
    )
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_verified     = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name','last_name','mobile']

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin






































