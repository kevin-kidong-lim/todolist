from django.contrib import admin

# Register your models here.
from .models import Member
from .models import LoginHistory
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter  
# from jet.filters import DateRangeFilter,DateTimeRangeFilter
from .member_filters import MemberAdminListFilter


@admin.register(LoginHistory)
class LoginHistoryAdmin(admin.ModelAdmin):
    list_display = ('member', 'login_date', 'ip_address', 'device_info')
    search_fields = ['member__user_id', 'ip_address', 'device_info']
    list_filter = ('login_date',)
    date_hierarchy = 'login_date'


from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
class UserCreationForm(forms.ModelForm):

   password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
   password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

   class Meta:
       model = Member
       fields = ('user_id','email', 'user_nm')

   def clean_password2(self):
       # Check that the two password entries match
       password1 = self.cleaned_data.get("password1")
       password2 = self.cleaned_data.get("password2")
       if password1 and password2 and password1 != password2:
           raise ValidationError("Passwords don't match")
       return password2

   def save(self, commit=True):
       # Save the provided password in hashed format
       user = super().save(commit=False)
       user.set_password(self.cleaned_data["password1"])
       user.is_admin = True
       user.is_superuser = True
       if commit:
           user.save()
       return user


class UserChangeForm(forms.ModelForm):

   password = ReadOnlyPasswordHashField()

   class Meta:
       model = Member
       fields = ('user_id', 'email', 'password', 'user_nm', 'is_active', 'is_admin','is_superuser',)
   

class UserAdmin(BaseUserAdmin):
       # The forms to add and change user instances
   form = UserChangeForm
   add_form = UserCreationForm

   # The fields to be used in displaying the User model.
   # These override the definitions on the base UserAdmin
   # that reference specific fields on auth.User.
   list_display = ('user_id', 'email', 'user_nm', 'is_admin')
   list_filter = ('is_admin',)
   fieldsets = (
       (None, {'fields': ('user_id', 'password')}),
       ('Personal info', {'fields': ('user_nm',)}),
       ('Permissions', {'fields': ('is_admin','is_superuser')}),
      
   )
   readonly_fields = ('user_id', )
   # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
   # overrides get_fieldsets to use this attribute when creating a user.
   add_fieldsets = (
       (None, {
           'classes': ('wide',),
           'fields': ('user_id','email', 'user_nm', 'password1', 'password2'),
       }),
   )
   search_fields = ('user_id',)
   ordering = ('user_id',)
   filter_horizontal = ()


# Now register the new UserAdmin...
admin.site.register(Member, UserAdmin) 