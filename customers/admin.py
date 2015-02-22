# coding: utf-8

from django.contrib import admin, messages
from django.contrib.admin.helpers import ACTION_CHECKBOX_NAME
from django.template.response import TemplateResponse
from django.contrib.auth.models import User
from django.db import connection
from django.http import HttpResponseRedirect

from protocolle.core.models import Status, TipoInstituicao, Carater, Natureza
from models import Client

from forms import CreateAdminForm


def create_admin(self, request, queryset):
    form = None
    # u = User.objects.get(pk=request.user.pk)

    if 'apply' in request.POST:
        form = CreateAdminForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            for obj in queryset:
                connection.set_schema(obj.schema_name, include_public=False)

                user = User.objects.create_user(username, email, password)

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

                # adicionando os carateres
                c = {'Normal', 'Urgente'}
                for i in c:
                    new_carater = Carater(nome=i)
                    new_carater.save()

                # adicionando as naturezas
                n = {'Aberto', 'Confidencial'}
                for i in n:
                    new_natureza = Natureza(nome=i)
                    new_natureza.save()

                connection.set_schema_to_public()

                messages.success(request, 'Admin "%s" para Cliente "%s": \
                                 criado com sucesso.' % (username, obj.name))

                return HttpResponseRedirect(request.get_full_path())

    if not form:
        form = CreateAdminForm(initial={'_selected_action':
                               request.POST.getlist(ACTION_CHECKBOX_NAME)})
                               # request=request)

    opts = self.model._meta
    app_label = opts.app_label
    module_name = opts.module_name,

    context = {
        'title': "Criar Administrador",
        'opts': opts,
        'app_label': app_label,
        'module_name': module_name,
        'create_form': form,
    }
    return TemplateResponse(request, 'admin/create_admin.html',
                            context, current_app=self.admin_site.name)
create_admin.short_description = "Criar Administrador"


def drop_schema(self, request, queryset):
    for obj in queryset:
        if request.POST.get('post'):
            cursor = connection.cursor()
            cursor.execute('DROP SCHEMA %s CASCADE' % obj.schema_name)
            obj.delete()
            messages.success(request, 'Cliente "%s" e seus dados: removido \
                             com sucesso.' % obj.name)
        else:
            opts = self.model._meta
            app_label = opts.app_label
            module_name = opts.module_name,

            context = {
                'title': "Tem certeza que deseja continuar?",
                'queryset': queryset,
                'action_checkbox_name': ACTION_CHECKBOX_NAME,
                'opts': opts,
                'app_label': app_label,
                'module_name': module_name,
            }
            return TemplateResponse(request, 'admin/drop_schema.html',
                                    context, current_app=self.admin_site.name)
drop_schema.short_description = "Remover Clientes e Dados selecionados"


class ClientAdmin(admin.ModelAdmin):
    list_per_page = 15
    list_display = ['name', 'institute']
    ordering = ['name']
    actions = [drop_schema, create_admin]


admin.site.register(Client, ClientAdmin)
