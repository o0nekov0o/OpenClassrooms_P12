from Website_CRM import models
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

admin.site.register(models.CRM_User, UserAdmin)
