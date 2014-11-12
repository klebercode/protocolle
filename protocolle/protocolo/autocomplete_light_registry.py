# coding: utf-8

import autocomplete_light

from django.db.models import Q

from protocolle.current_user import get_current_user

from protocolle.auxiliar.models import Instituicao_User
from protocolle.protocolo.models import Documento, Tramite, Tramite_Documento


class DocumentoAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ('protocolo', 'tipo_documento__nome', 'numero',
                     'data_documento', 'data_validade', 'folhas',
                     'carater__nome', 'natureza__nome', 'origem__nome',
                     'destino__nome', 'assunto', 'interessado__nome',
                     'observacao', 'status__nome',)
    autocomplete_js_attributes = {'placeholder': 'Buscar documento...',
                                  'minimum_characters': 1}
    widget_js_attributes = {'max_values': 10}

    def choices_for_request(self):
        iu = Instituicao_User.objects.get(user=get_current_user)

        try:
            # busca os tramites relacionados a insituicao do usuario
            t = Tramite.objects.filter(
                destino_id=iu.instituicao).order_by('-id')[:1]
            # busca os documentos relacionados aos tramites
            td = Tramite_Documento.objects.filter(tramite=t).order_by('-id')

            # return qs.filter(
            #     Q(status__nome='Arquivado') |
            #     Q(status__nome='Entregue'))
            self.choices = Documento.objects.filter(
                Q(status__nome='Tramitando') |
                Q(status__nome='Parado'),
                Q(destino_id=iu.instituicao) |
                Q(pk__in=td.all().values('protocolo_id')))
            # if not self.request.user.is_staff:
            # self.choices = Documento.objects.exclude(
            #     Q(status__nome='Arquivado') |
            #     Q(status__nome='Entregue'))
        except:
            # return qs.filter(
            #     Q(origem_id=iu.instituicao) |
            #     Q(destino_id=iu.instituicao))
            self.choices = Documento.objects.filter(
                Q(status__nome='Tramitando') |
                Q(status__nome='Parado'),
                Q(destino_id=iu.instituicao))

        # self.choices = self.choices.filter(private=False)
        return super(DocumentoAutocomplete, self).choices_for_request()


autocomplete_light.register(Documento, DocumentoAutocomplete)
