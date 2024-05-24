from django.contrib import admin

from .models import MyUser

@admin.register(MyUser)
class myuseradmin(admin.ModelAdmin):
    list_display = ['id','email','first_name','last_name','password','username']
# Register your models here.
