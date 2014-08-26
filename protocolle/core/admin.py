# coding: utf-8

from django.contrib import admin

from flexselect import FlexSelectWidget

from protocolle.core.models import (TipoDocumento, Carater, Natureza,
                                    Status, TipoInstituicao, Grupo)


class TipoDocumentoAdmin(admin.ModelAdmin):
    fields = ['nome']
    list_display = ['nome']
    search_fields = ['nome']


class TipoInstituicaoAdmin(admin.ModelAdmin):
    fields = ['nome']
    list_display = ['nome']
    search_fields = ['nome']


class GrupoAdmin(admin.ModelAdmin):
    fields = ['nome', 'tipo_instituicao']
    list_display = ['nome', 'tipo_instituicao']
    list_filter = ['tipo_instituicao']
    search_fields = ['nome', 'tipo_instituicao__nome']


class CaraterAdmin(admin.ModelAdmin):
    fields = ['nome']
    list_display = ['nome']
    search_fields = ['nome']


class NaturezaAdmin(admin.ModelAdmin):
    fields = ['nome']
    list_display = ['nome']
    search_fields = ['nome']


class StatusAdmin(admin.ModelAdmin):
    fields = ['nome']
    list_display = ['nome']
    search_fields = ['nome']


admin.site.register(TipoDocumento, TipoDocumentoAdmin)
admin.site.register(TipoInstituicao, TipoInstituicaoAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Carater, CaraterAdmin)
admin.site.register(Natureza, NaturezaAdmin)
admin.site.register(Status, StatusAdmin)

