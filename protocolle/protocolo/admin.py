# coding: utf-8
from django.contrib import admin, messages
from django.contrib.admin.options import TabularInline
# from django.core.exceptions import PermissionDenied
# from django import forms
# from django.template import RequestContext
from django.conf.urls import patterns
from django.shortcuts import render
from django.db.models import Q
from django.utils import timezone

# from flexselect import FlexSelectWidget

import autocomplete_light
# import autocomplete_light_registry
import string

from protocolle.core.models import Status
from protocolle.auxiliar.models import Instituicao_User
from protocolle.protocolo.models import (Documento, DocumentoAnexo, Tramite,
                                         Tramite_Documento)

# import barcode
# from barcode.writer import ImageWriter

# from django.forms.widgets import HiddenInput


def get_superuser(request):
    return request.user.is_superuser


def get_instituicao_user(user):
    iu = Instituicao_User.objects.get(user_id=user)
    return iu


def get_status_id(status):
    s = Status.objects.get(nome=status)
    return s.pk


def atualiza_protocolo_num(self, request, queryset):
    """Corrige bug do ano no numero do protocolo"""
    for obj in queryset:
        obj.protocolo = string.replace(obj.protocolo, '2015', '2016')
        obj.save()
atualiza_protocolo_num.short_description = 'Atualiza Número do Protocolo'


def arquivar_doc(self, request, queryset):
    """
    Antes de arquivar o documento o sistema verifica se existe algum tramite
    para o documento
    - se existir: sera verificado se o ultimo destino do
    documento no tramite e igual a insituicao do usuario
    - se nao existir: sera verificado se o destino no cadastro do
    documento e igual a instituicao do usuario
    """
    for obj in queryset:
        iu = Instituicao_User.objects.get(user_id=request.user.pk)
        # print "doc id: %s" % obj.pk

        try:
            # se existir tramite
            td = Tramite_Documento.objects.filter(
                protocolo_id=obj.pk).order_by('-id')[0]
            # print "prot id: %s" % td.protocolo_id
            # print "tram id: %s" % td.tramite_id
            t = Tramite.objects.get(id=td.tramite_id)
            # print "tram dest: %s" % t.destino
            # print "inst user: %s" % iu.instituicao
            destiny = t.destino_id
            # print "try: %s" % destiny

        except:
            # se nao existir tramite
            destiny = obj.destino_id
            # print "except: %s" % destiny

        if iu.instituicao_id == destiny:
            if obj.status_id == get_status_id('Tramitando') \
               or obj.status_id == get_status_id('Parado'):
                queryset.update(status=get_status_id('Arquivado'))
                messages.success(request, 'O Documento foi arquivado com \
                                 sucesso.')
            else:
                messages.error(request, 'O Documento não está tramitando ou \
                               parado.')
        else:
            messages.error(request, 'O Documento não está nesta instituição.')
            arquivar_doc.short_description = "Arquivar documento"


def desarquivar_doc(self, request, queryset):
    """
    Antes de desarquivar o documento o sistema verifica se existe algum tramite
    para o documento
    - se existir: sera verificado se o ultimo destino do
    documento no tramite e igual a insituicao do usuario e
    o status sera alterado para 'Tramitando'
    - se nao existir: sera verificado se o destino no cadastro do
    documento e igual a instituicao do usuario e
    o status sera alterado para 'Parado'
    """
    for obj in queryset:
        iu = Instituicao_User.objects.get(user_id=request.user.pk)

        try:
            # se existir tramite
            td = Tramite_Documento.objects.filter(
                protocolo_id=obj.pk).order_by('-id')[0]
            t = Tramite.objects.get(id=td.tramite_id)
            destiny = t.destino_id

        except:
            # se nao existir tramite
            destiny = obj.destino_id

        if iu.instituicao_id == destiny:
            if obj.status_id == get_status_id('Arquivado'):
                if Tramite_Documento.objects.filter(protocolo_id=obj.pk):
                    # se existir tramite
                    sta = 'Tramitando'
                else:
                    # se nao existir tramite
                    sta = 'Parado'
                    queryset.update(status=get_status_id(sta))
                    messages.success(request, 'O Documento foi desarquivado com \
                                     sucesso.')
            else:
                messages.error(request, 'O Documento não está arquivado.')
        else:
            messages.error(request, 'O Documento não está arquivado nesta \
                           instituição.')
            desarquivar_doc.short_description = "Desarquivar documento"


def entregar_doc(self, request, queryset):
    for obj in queryset:
        iu = Instituicao_User.objects.get(user_id=request.user.pk)

        try:
            # se existir tramite
            td = Tramite_Documento.objects.filter(
                protocolo_id=obj.pk).order_by('-id')[0]
            t = Tramite.objects.get(id=td.tramite_id)
            destiny = t.destino_id

        except:
            # se nao existir tramite
            destiny = obj.destino_id

        if not iu.instituicao_id == destiny:
            if obj.status_id == get_status_id('Tramitando') \
               or obj.status_id == get_status_id('Parado'):
                queryset.update(status=get_status_id('Entregue'))
                messages.success(request, 'O Documento foi entregue com \
                                 sucesso.')
            else:
                messages.error(request, 'O Documento não está tramitando ou \
                               parado.')
        else:
            messages.error(request, 'O Documento está nesta instituição, \
                           então você deve arquivá-lo.')
            entregar_doc.short_description = "Documento Entregue"


class DocumentoAnexoInline(TabularInline):
    model = DocumentoAnexo
    fields = ('arquivo',)
    extra = 1


class DocumentoAdmin(admin.ModelAdmin):
    readonly_fields = ('status', 'protocolo',)
    list_per_page = 15
    list_filter = ('tipo_documento', 'carater', 'natureza', 'origem',
                   'destino', 'interessado', 'status')
    list_display = ('get_protocolo', 'get_data_recebimento', 'tipo_documento',
                    'numero', 'truncate_origem', 'truncate_remetente',
                    'status', 'operacao', 'get_anexos',
                    'action_link')
    search_fields = ('data_recebimento', 'protocolo',
                     'tipo_documento__nome', 'numero', 'carater__nome',
                     'natureza__nome', 'origem__nome', 'interessado__nome',
                     'status__nome', 'data_documento', 'data_validade',
                     'destino__nome', 'assunto', 'observacao')
    fieldsets = (
        (None, {
            'fields': (('operacao', 'protocolo', 'status'),
                       ('tipo_documento', 'numero'),
                       ('data_documento', 'data_validade', 'folhas'),
                       ('carater', 'natureza'), 'origem', 'assunto',
                       'interessado', 'observacao')
        }),
    )
    date_hierarchy = 'data_recebimento'
    raw_id_fields = ('origem', 'destino', 'interessado')

    autocomplete_lookup_fields = {
        'fk': ['origem', 'destino', 'interessado'],
    }

    inlines = [DocumentoAnexoInline]

    actions = [arquivar_doc, desarquivar_doc, entregar_doc]

    def save_model(self, request, obj, form, change):
        """
        Salva automaticamente o destino do documento igual a instituicao do
        usuario
        """
        iu = Instituicao_User.objects.get(user=request.user)
        obj.destino = iu.instituicao
        obj.save()

        if not obj.origem == iu.instituicao and obj.destino == iu.instituicao:
            messages.info(request, 'Não esqueça de arquivar o documento, \
                          caso não se faça nescessário uma tramitação.')
        else:
            messages.info(request, 'Não esqueça de atualizar o status do \
                          Documento.')

    def has_change_permission(self, request, obj=None):
        """
        Bloquear a edicao de documentos que estao com status diferente
        de 'Parado'
        E testa se é super usuário
        """
        if obj is not None and obj.status_id != get_status_id('Parado'):
            if not request.user.is_superuser:
                return False
            else:
                return True
        return super(DocumentoAdmin,
                     self).has_change_permission(request, obj=obj)

    # def get_list_display_links(self, request, list_display):
    #     """
    #     Remover link para edicao na lista
    #     """
    #     return []

    def get_actions(self, request):
        """
        Remover a acao de deletar na lista
        """
        actions = super(DocumentoAdmin, self).get_actions(request)
        # if request.user.username[0].upper() != 'J':
        if 'delete_selected' in actions:
            del actions['delete_selected']
            return actions

    def action_link(self, obj):
        """
        Adicionar os botoes de acao apenas nos documentos com status igual
        a 'Parado'
        """
        # app_name = obj._meta.app_label
        # url_name = obj._meta.module_name
        # data_id = obj.id

        action_buttons = """
        <nav class="grp-pagination">
        <ul>
        <li>
        <a href="/{0}/{1}/{2}" \
                class="grp-results">Editar</a>
        <a href="/{0}/{1}/{2}/delete" \
                class="grp-results grp-delete-link">Deletar</a>
        </li>
        </ul>
        </nav>
        """.format(obj._meta.app_label,
                   obj._meta.module_name,
                   obj.id,)

        if obj.status_id == get_status_id('Parado'):
            return action_buttons
        else:
            return ""
    action_link.allow_tags = True
    action_link.short_description = 'Ações'

    def get_protocolo(self, obj):
        if not obj.status_id == get_status_id('Parado'):
            return "</a>%s<a>" % obj.protocolo
        else:
            return obj.protocolo
    get_protocolo.allow_tags = True
    get_protocolo.short_description = 'Protocolo'
    get_protocolo.admin_order_field = 'protocolo'

    def get_data_recebimento(self, obj):
        data_recebimento = timezone.localtime(obj.data_recebimento)
        return data_recebimento.strftime('%d/%m/%Y %H:%M')
    get_data_recebimento.allow_tags = True
    get_data_recebimento.short_description = 'Data do Recebimento'
    get_data_recebimento.admin_order_field = 'data_recebimento'

    def truncate_origem(self, obj):
        text = str(obj.origem).decode('utf8')
        return (text[:30] + '...') if len(text) > 30 else text
    truncate_origem.short_description = 'Instituição de Origem'
    truncate_origem.admin_order_field = 'origem'

    def truncate_destino(self, obj):
        text = str(obj.destino).decode('utf8')
        return (text[:30] + '...') if len(text) > 30 else text
    truncate_destino.short_description = 'Instituição de Destino'
    truncate_destino.admin_order_field = 'destino'

    def truncate_remetente(self, obj):
        text = str(obj.interessado).decode('utf8')
        return (text[:30] + '...') if len(text) > 30 else text
    truncate_remetente.short_description = 'Remetente'
    truncate_remetente.admin_order_field = 'interessado'

    def queryset(self, request):
        """
        filtra os documentos com destino igual ao do usuario ou
        documentos com tramite para para a instituicao do usuario
        """
        qs = super(DocumentoAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        # pega a insittuicao do usuario
        iu = Instituicao_User.objects.get(user=request.user)

        try:
            # busca os tramites relacionados a insituicao do usuario
            t = Tramite.objects.filter(
                Q(origem_id=iu.instituicao) | Q(destino_id=iu.instituicao)
            ).order_by('-id')
            # busca os documentos relacionados aos tramites
            td = Tramite_Documento.objects.filter(tramite=t).order_by('-id')

            return qs.filter(
                Q(origem_id=iu.instituicao) |
                Q(destino_id=iu.instituicao) |
                Q(pk__in=td.all().values('protocolo_id')))
        except:
            return qs.filter(
                Q(origem_id=iu.instituicao) |
                Q(destino_id=iu.instituicao))


class Tramite_DocumentoInline(admin.TabularInline):
    model = Tramite_Documento
    extra = 1
    form = autocomplete_light.modelform_factory(Tramite_Documento)
    # sortable_field_name = "order"
    fields = ['protocolo', 'folhas']


# class TramiteAdminForm(forms.ModelForm):
#     """
#     Funcao para filtrar os documentos com status diferente de 'Arquivado'
#     Nao funciona com o m2m do grappelli, por conta do raw_id_fields
#     Essa eh outra forma de fazer (mais intrusiva) criando um FormModel
#     """
#     protocolo = forms.ModelMultipleChoiceField(Documento.objects.all(),
#         widget=autocomplete_light.MultipleChoiceWidget(
#             'DocumentoAutocomplete'))

#     class Meta:
#         model = Tramite

#         widget = {
#             'protocolo': autocomplete_light.ChoiceWidget(
#                 'DocumentoAutocomplete')
#         }

#     def __init__(self, *args, **kwargs):
#         super(TramiteAdminForm, self).__init__(*args, **kwargs)
#         self.fields['protocolo'].queryset = Documento.objects.exclude(
#             status__nome='Arquivado')

# Funcao para customizar o widget m2m
# Mas nao deu certo!
#         super(TramiteAdminForm, self).__init__(*args, **kwargs)
#         wtf = Documento.objects.exclude(status__nome='Arquivado')
#         w = self.fields['protocolo'].widget
#         choices = []
#         for choice in wtf:
#             choices.append((choice.tipo_documento, choice.protocolo))
#         w.choices = choices

class TramiteAdmin(admin.ModelAdmin):
    list_filter = ('origem', 'origem_setor', 'destino', 'destino_setor')
    list_per_page = 15
    list_display = ('get_numero_guia', 'get_data_tramite', 'truncate_origem',
                    'truncate_origem_setor', 'truncate_destino',
                    'truncate_destino_setor', 'get_documentos', 'action_link')
    search_fields = ('id', 'data_tramite', 'origem__nome',
                     'origem_setor__nome', 'destino__nome',
                     'destino_setor__nome', 'protocolo__protocolo',)
    date_hierarchy = 'data_tramite'
    # filter_horizontal = ('protocolo',)
    raw_id_fields = ('origem', 'origem_setor', 'destino', 'destino_setor',)
    # 'protocolo',)

    # related_lookup_fields = {
    autocomplete_lookup_fields = {
        'fk': ['origem', 'origem_setor', 'destino', 'destino_setor'],
        # 'm2m': ['protocolo'],
    }

    # form = TramiteAdminForm
    form = autocomplete_light.modelform_factory(Tramite)

    inlines = [Tramite_DocumentoInline]

    # change_list_template = "admin/protocolle/change_list.html"
    # change_list_template = "admin/change_list_filter_sidebar.html"
    # review_template = 'admin/protocolo/detail_view.html'

    # def get_queryset(self):
    #     qs = self.model._default_manager.get_queryset()
    #     # try to find model admin queryset
    #     model_admin = self.GET.get("TramiteAdmin", None)
    #     if model_admin:
    #         module, classname = model_admin.split(",")
    #         ma = import_from(module, classname)
    #         # FIXME: we are not using the admin_site here, do we need it?
    #         qs = ma(self.model, None).get_queryset(self.request)
    #     qs = self.get_filtered_queryset(qs)
    #     print qs
    #     return qs

    # Funcao para filtrar os documentos com status diferente de 'Arquivado'
    # Nao funciona com o m2m do grappelli, por conta do raw_id_fields
    # def formfield_for_manytomany(self, db_field, request, **kwargs):
    #     print db_field.name
    #     if db_field.name == "protocolo":
    #         kwargs["queryset"] = Documento.objects.exclude(
    #             status__nome='Arquivado')
    #     return super(TramiteAdmin, self).formfield_for_manytomany(
    #         db_field, request, **kwargs)

    def has_change_permission(self, request, obj=None):
        """
        Bloquear a edicao de tramite
        E testa se é super usuário
        """
        if obj is not None:
            if not request.user.is_superuser:
                return False
            else:
                return True
        return super(TramiteAdmin,
                     self).has_change_permission(request, obj=obj)

    def get_urls(self):
        urls = super(TramiteAdmin, self).get_urls()
        my_urls = patterns(
            '',
            (r'(?P<id>[\d\+]+)/guia/$',
             self.admin_site.admin_view(self.guia)),
            (r'(?P<id>[\d\+]+)/etiqueta/$',
             self.admin_site.admin_view(self.etiqueta)),
        )
        return my_urls + urls

    def guia(self, request, id):
        tramite = Tramite.objects.get(pk=id)
        zero_id = '%08d' % (tramite.pk,)

        # EAN = barcode.get_barcode('Code39')
        # ean = EAN(zero_id)

        # ean = barcode.get('Code39',
        #                   zero_id,
        #                   writer=ImageWriter())
        # filename = ean.save('protocolle/core/static/ean13')

        # tramite_documento = tramite_documento.objects.get(pk=id)
        context = {
            'title': 'Review Tramite: %s' % tramite.data_tramite,
            'tramite': tramite,
            # 'codigo': filename.replace('protocolle/core', ''),
            'codigo_zero': zero_id,
            'instituicao': get_instituicao_user(request.user.pk)

            # 'opts': self.model._meta,
            # 'root_path': self.admin_site.root_path,
        }

        return render(request, 'protocolo/guia.html', context)

    def etiqueta(self, request, id):
        tramite = Tramite.objects.get(pk=id)
        zero_id = '%08d' % tramite.pk

        # EAN = barcode.get_barcode('Code39')
        # ean = EAN(zero_id)

        # ean = barcode.get('Code39',
        #                   zero_id,
        #                   writer=ImageWriter())
        # filename = ean.save('protocolle/core/static/ean13')

        # tramite_documento = tramite_documento.objects.get(pk=id)
        context = {
            'title': 'Review Tramite: %s' % tramite.data_tramite,
            'tramite': tramite,
            # 'codigo': filename.replace('protocolle/core', ''),
            'codigo_zero': zero_id,
            'instituicao': get_instituicao_user(request.user.pk)

            # 'opts': self.model._meta,
            # 'root_path': self.admin_site.root_path,
        }

        return render(request, 'protocolo/etiqueta.html', context)

    def action_link(self, obj):
        # app_name = obj._meta.app_label
        # url_name = obj._meta.module_name
        # data_id = obj.id

        # <a href="/{0}/{1}/{2}" class="grp-results">Editar</a>
        return """
    <nav class="grp-pagination">
    <ul>
    <li>
    <a href="{2}/guia/" class="grp-results" \
            onclick="return showAddAnotherPopup(this);">Guia</a>
    <a href="{2}/etiqueta/" class="grp-results" \
            onclick="return showAddAnotherPopup(this);"> \
            Etiqueta</a>
    <a href="/{0}/{1}/{2}/delete" \
            class="grp-results grp-delete-link">Deletar</a>
    </li>
    </ul>
    </nav>
    """.format(obj._meta.app_label,
               obj._meta.module_name,
               obj.id,)
    action_link.allow_tags = True
    action_link.short_description = 'Ações'

    def get_numero_guia(self, obj):
        return '</a>%08d<a>' % obj.id
    get_numero_guia.allow_tags = True
    get_numero_guia.short_description = 'N. da Guia'
    get_numero_guia.admin_order_field = 'pk'

    def get_data_tramite(self, obj):
        data_tramite = timezone.localtime(obj.data_tramite)
        return data_tramite.strftime('%d/%m/%Y %H:%M')
    get_data_tramite.allow_tags = True
    get_data_tramite.short_description = 'Data do Trâmite'
    get_data_tramite.admin_order_field = 'data_tramite'

    def truncate_origem(self, obj):
        text = str(obj.origem).decode('utf8')
        return (text[:30] + '...') if len(text) > 30 else text
    truncate_origem.short_description = 'Instituição de Origem'
    truncate_origem.admin_order_field = 'origem'

    def truncate_destino(self, obj):
        text = str(obj.destino).decode('utf8')
        return (text[:30] + '...') if len(text) > 30 else text
    truncate_destino.short_description = 'Instituição de Destino'
    truncate_destino.admin_order_field = 'destino'

    def truncate_origem_setor(self, obj):
        text = str(obj.origem_setor).decode('utf8')
        return (text[:30] + '...') if len(text) > 30 else text
    truncate_origem_setor.short_description = 'Setor Origem'
    truncate_origem_setor.admin_order_field = 'origem_setor'

    def truncate_destino_setor(self, obj):
        text = str(obj.destino_setor).decode('utf8')
        return (text[:30] + '...') if len(text) > 30 else text
    truncate_destino_setor.short_description = 'Setor Destino'
    truncate_destino_setor.admin_order_field = 'destino_setor'

    def queryset(self, request):
        """
        Filtrar apenas os tramites que o usuario esta envolvido, seja como
        origem ou como destino
        """
        qs = super(TramiteAdmin, self).queryset(request)
        if request.user.is_superuser:
            return qs
        # pega a instituicao do usuario
        iu = Instituicao_User.objects.get(user=request.user)
        # faz o filtro por qualquer relacionamento da insituicao com o tramite
        return qs.filter(Q(origem_id=iu.instituicao) |
                         Q(destino_id=iu.instituicao))

    # def action(self,form):
    #   return "<a href='preview/%s' class='grp-button' \
    #   onclick='return showAddAnotherPopup(this);'>view</a>" % (form.id)
    # action.allow_tags = True


admin.site.register(Tramite, TramiteAdmin)
admin.site.register(Documento, DocumentoAdmin)
