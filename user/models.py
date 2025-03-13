from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, Group
from user.managers import CustomUserManager

class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=20, unique=True)  
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    objects = CustomUserManager()
    
    def save(self, *args, **kwargs):
        is_new = self._state.adding
        super().save(*args, **kwargs)
        
        if is_new:
            if self.is_superuser:
                # Create and add to admin group for superuser
                admin_group, _ = Group.objects.get_or_create(name='admin')
                self.groups.add(admin_group)
            else:
                # Create and add to user group for regular users
                user_group, _ = Group.objects.get_or_create(name='user')
                self.groups.add(user_group)
    
    def __str__(self):
        return str(self.username) if self.username else str(self.email)

class UserDetails(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='userdetails')
    name = models.CharField(max_length=150, blank=True)
    address = models.TextField(blank=True)
    age = models.IntegerField(blank=True, null=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    last_donation_date = models.DateField(blank=True, null=True)
    availability_status = models.BooleanField(default=False)
    
    def __str__(self) -> str:
        user_identifier = str(self.user.username) if self.user.username else str(self.user.email)
        return f"{user_identifier}'s details"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)