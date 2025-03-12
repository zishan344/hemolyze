from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UserDetails
from django.contrib.auth.forms import UserChangeForm, UserCreationForm

class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = CustomUser
        fields = '__all__'

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if not username:
            raise ValueError('Username is required')
        return username

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ('email', 'username') 

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ['email', 'username', 'is_active', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'groups']
    readonly_fields = ['date_joined', 'last_login']
    ordering = ['email']
    
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}), 
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2'),  
        }),
    )

    search_fields = ['email', 'username'] 
    ordering = ['email']

class UserDetailsAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'phone_number', 'availability_status']
    list_filter = ['availability_status', 'last_donation_date']
    search_fields = ['user__email', 'user__username', 'name', 'phone_number'] 
    fieldsets = (
        ('User Information', {'fields': ('user', 'name')}),
        ('Contact Details', {'fields': ('phone_number', 'address')}),
        ('Donation Information', {'fields': ('age', 'last_donation_date', 'availability_status')}),
    )

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(UserDetails, UserDetailsAdmin)