from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


class CustomUserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    def _create_user(self, email, password=None, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    class Role(models.TextChoices):
        ANON = "ANON", "Anon"
        CLIENT = "CLIENT", "Client"
        ORGANIZATION = "ORGANIZATION", "Organization"

    base_role = Role.ANON
    username = None
    email = models.EmailField(_('email address'), unique=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()
    def save(self, *args, **kwargs):
        if not self.pk:
            self.role = self.base_role
            return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.email




class Client(User):
    first_name = models.CharField(max_length=200, null=True, blank=True)
    last_name = models.CharField(max_length=200, null=True, blank=True)
    phone_number = models.CharField(max_length=200, null=True, blank=True)
    location = models.CharField(max_length=250, null=True, blank=True)
    nin = models.CharField(null=True, max_length=3, blank=True)
    age = models.CharField(null=True, max_length=3, blank=True)
    weight = models.CharField(null=True, max_length=3, blank=True)
    blood_group = models.CharField(max_length=4, null=True)
    wants_to_donate = models.BooleanField(default=True)
    needs_donation = models.BooleanField(default=False)
    base_role = User.Role.CLIENT
    is_verified = models.BooleanField(default=False)
    donations = models.IntegerField(default=0)


    #learn 1 to 1 rel

    # class Meta:
    #     proxy = True

class Organization(User):
    company_name = models.CharField(max_length=250)
    CAC = models.CharField(max_length=30)
    location = models.CharField(max_length=250)
    address = models.TextField(null=True, blank=True)
    base_role = User.Role.ORGANIZATION
    is_verified = models.BooleanField(default=False)

    #learn 1 to 1 rel

    # class Meta:
    #     proxy = True


class Transaction():
    #two users, date time, isapproved[]
    #holds two users, patient and donors
    #hold organisation
    #successful


    # temp
    hospital = models.ForeignKey(Organization, on_delete=models.SET_NULL)
    clients = models.ForeignKey(Client, on_delete=models.SET_NULL)
    date = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    pass

#class Patient():
    #one to many relationship # hospital and patients
    #pass



@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)