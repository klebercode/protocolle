# coding: utf-8

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import connection 

from models import Client


def create_admin(self, request, queryset):
    for obj in queryset:
        u = User.objects.get(pk=request.user.pk)
        connection.set_schema(obj.schema_name, include_public=False)
        user = User.objects.create_user(u.username, u.email, 'pass')
        user.is_staff = True
        user.is_active = True
        user.is_superuser = True
        user.save()
        connection.set_schema_to_public()
create_admin.short_description = "Criar administrador"


class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'institute']
    ordering = ['name']
    actions = [create_admin]


admin.site.register(Client, ClientAdmin)
