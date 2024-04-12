from django.contrib import admin
from .models import TodoItems
# Register your models here.
class TodoAdmin(admin.ModelAdmin):
    list_display = ('title','user','created_at','completed','modified_at')
admin.site.register(TodoItems,TodoAdmin)