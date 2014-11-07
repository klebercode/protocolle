# coding: utf-8

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import connection

from protocolle.core.models import Status, TipoInstituicao
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
        # adicionando os status
        s = {'Tramitando', 'Arquivado', 'Parado', 'Entregue'}
        for i in s:
            new_status = Status(nome=i)
            new_status.save()
        # adicionando os tipos de instituicao
        ti = {'Externa', 'Interna'}
        for i in ti:
            new_tipoinst = TipoInstituicao(nome=i)
            new_tipoinst.save()
        connection.set_schema_to_public()
create_admin.short_description = "Criar administrador"


class ClientAdmin(admin.ModelAdmin):
    list_display = ['name', 'institute']
    ordering = ['name']
    actions = [create_admin]


admin.site.register(Client, ClientAdmin)
