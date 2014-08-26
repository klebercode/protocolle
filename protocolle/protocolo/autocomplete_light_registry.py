# coding: utf-8

import autocomplete_light

from django.db.models import Q

from models import Documento


class DocumentoAutocomplete(autocomplete_light.AutocompleteModelBase):
    search_fields = ('protocolo', 'tipo_documento__nome', 'numero', 
                     'data_documento', 'data_validade', 'folhas', 
                     'carater__nome', 'natureza__nome', 'origem__nome', 
                     'destino__nome', 'assunto', 'interessado__nome', 
                     'observacao', 'status__nome',)
    autocomplete_js_attributes = {'placeholder': 'Buscar documento...',
                                  'minimum_characters': 1,}
    widget_js_attributes = {'max_values': 10,}

    def choices_for_request(self):
        # if not self.request.user.is_staff:
        self.choices = Documento.objects.exclude(Q(status__nome='Arquivado') |\
                                                 Q(status__nome='Entregue'))

        # self.choices = self.choices.filter(private=False)
        return super(DocumentoAutocomplete, self).choices_for_request()


autocomplete_light.register(Documento, DocumentoAutocomplete)

