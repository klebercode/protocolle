# coding: utf-8

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User

from flexselect import FlexSelectWidget

from protocolle.core.models import Grupo
from protocolle.auxiliar.models import (Instituicao, Pessoa, Setor,
                                        Instituicao_User)


class InstituicaoWidget(FlexSelectWidget):
    trigger_fields = ['tipo_instituicao']

    def details(self, base_field_instance, instance):
        return ""

    def queryset(self, instance):
        tipo_instituicao_id = instance.tipo_instituicao.id
        return Grupo.objects.filter(tipo_instituicao=tipo_instituicao_id)

    def empty_choices_text(self, instance):
        return "Selecione um Tipo de Instituição"


class InstituicaoAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('nome', 'tipo_instituicao', 'grupo')
        }),
        ('Contato', {
            'fields': ('email', 'fone')
        }),
        ('Endereço', {
            'fields': ('endereco', 'numero', 'bairro',
                       'complemento', 'cep', 'cidade', 'uf')
        }),
    )
    list_display = ['nome', 'tipo_instituicao', 'grupo', 'email', 'fone']
    list_filter = ['tipo_instituicao', 'grupo', 'bairro', 'cidade', 'uf']
    search_fields = ['nome', 'tipo_instituicao__nome', 'grupo__nome',
                     'email', 'fone', 'endereco', 'numero', 'bairro',
                     'complemento', 'cep', 'cidade', 'uf']

    # raw_id_fields = ('tipo_instituicao',)

    # autocomplete_lookup_fields = {
        # 'fk': ['instituicao'],
    # }

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        """
        Alters the widget displayed for the base field.
        """
        if db_field.name == 'grupo':
            kwargs['widget'] = InstituicaoWidget(
                base_field=db_field,
                modeladmin=self,
                request=request,
            )
        return super(InstituicaoAdmin,
                     self).formfield_for_foreignkey(db_field,
                                                    request, **kwargs)


class SetorAdmin(admin.ModelAdmin):
    fields = ['instituicao', 'nome', 'sigla', 'responsavel']
    list_display = ['nome', 'sigla', 'instituicao', 'responsavel']
    list_filter = ['instituicao', 'responsavel']
    search_fields = ['nome', 'sigla', 'instituicao__nome', 'responsavel__nome']
    # change_list_template = "admin/change_list_filter_sidebar.html"
    # change_list_filter_template = "admin/filter_listing.html"


class PessoaAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('nome', 'email', 'fone')
        }),
        ('Endereço', {
            'fields': ('endereco', 'numero', 'bairro',
                       'complemento', 'cep', 'cidade', 'uf')
        }),
    )
    list_display = ['nome', 'email', 'fone']
    list_filter = ['bairro', 'cidade', 'uf']
    search_fields = ['nome', 'email', 'fone', 'endereco', 'numero',
                     'bairro', 'complemento', 'cep', 'cidade', 'uf']


class Instituicao_UserInline(admin.TabularInline):
    model = Instituicao_User
    can_delete = False


class Instituicao_UserAdmin(UserAdmin):
    list_display = UserAdmin.list_display + ('get_instituicao',)
    inlines = (Instituicao_UserInline,)

    def get_instituicao(self, obj):
        try:
            instituicao = obj.get_profile().instituicao
            return instituicao
        except:
            return ""
    get_instituicao.allow_tags = True
    get_instituicao.short_description = u'Instituição'


admin.site.unregister(User)
admin.site.register(User, Instituicao_UserAdmin)
admin.site.register(Instituicao, InstituicaoAdmin)
admin.site.register(Setor, SetorAdmin)
admin.site.register(Pessoa, PessoaAdmin)
