# coding: utf-8

from django.db import models
# from django.db.models import Q
from django.db.models.signals import post_save  # , pre_save, m2m_changed
from django.utils.translation import ugettext_lazy as _

import datetime
# from datetime import date
now = datetime.datetime.now()

from protocolle.core.models import (TipoDocumento, Carater, Natureza,
                                    Status, OPERATION_CHOICES)
from protocolle.auxiliar.models import (Instituicao, Pessoa, Setor)


class Documento(models.Model):
    operacao = models.IntegerField(_(u'Operação'), choices=OPERATION_CHOICES)
    tipo_documento = models.ForeignKey(TipoDocumento,
                                       verbose_name=_(u'Tipo de Documento'),
                                       related_name='DocTiposDocumento')
    protocolo = models.CharField(_(u'Número do Protocolo'), max_length=100,
                                 unique=True, default=0, editable=False)
    numero = models.CharField(_(u'Número do Documento'), max_length=100)
    data_recebimento = models.DateTimeField(_(u'Data de Recebimento'),
                                            auto_now_add=True)
    data_documento = models.DateField(_(u'Data do Documento'))
    data_validade = models.DateField(_(u'Data de Validade'),
                                     null=True, blank=True)
    folhas = models.IntegerField(_(u'Número de Folhas'), null=True, blank=True)
    carater = models.ForeignKey(Carater, verbose_name=_(u'Caráter'),
                                related_name='DocCarateres')
    natureza = models.ForeignKey(Natureza, verbose_name=_(u'Natureza'),
                                 related_name='DocNaturezas')
    origem = models.ForeignKey(Instituicao,
                               verbose_name=_(u'Instituição Origem'),
                               related_name='DocInstituicoesOri')
    destino = models.ForeignKey(Instituicao,
                                verbose_name=_(u'Instituição Destino'),
                                related_name='DocInstituicoesDes')
    assunto = models.TextField(_(u'Assunto'))
    interessado = models.ForeignKey(Pessoa, verbose_name=_(u'Interessado'),
                                    related_name='DocPessoasRem')
    status = models.ForeignKey(Status, verbose_name=_(u'Status'),
                               related_name='DocSituacoes', editable=False)
    observacao = models.TextField(_(u'Observação'), null=True, blank=True)

    def save(self, *args, **kwargs):
        """
        Funcao para gerar o número de protocolo
        unico e personalizado
        """
        if not self.id:
            # verifica se existem dados na tabela Documento
            d = Documento.objects.all()
            if not d:
                # se nao: gerar protocolo = 1
                k = 1
            else:
                # se sim: gerar protocolo + 1
                i = Documento.objects.all().order_by('-id')[0]
                k = i.id+1
            # inseri um formato com zeros e ano (Ex: 00000002/2014)
            self.protocolo = '%08d/%d' % (k, now.year)
        super(Documento, self).save(*args, **kwargs)

    def __unicode__(self):
        # return self.protocolo
        return "%s | %s | %s | %s | %s" % (
            self.protocolo,
            self.data_recebimento.strftime("%d/%m/%Y"),
            unicode(self.tipo_documento),
            unicode(self.origem),
            unicode(self.interessado))

    class Meta:
        verbose_name = _(u'Documento')
        verbose_name_plural = _(u'Documentos')


class DocumentoAnexo(models.Model):
    documento = models.ForeignKey('Documento', related_name='AneDocumentos')
    arquivo = models.FileField(_(u'Arquivo'), upload_to=u'anexos',
                               help_text='Selecione um arquivo')

    def attach_link(self):
        if self.arquivo:
            return "<a href='%s'>Baixar</a>" % self.arquivo.url
        else:
            return "Nenhum arquivo encontrado"
    attach_link.allow_tags = True
    attach_link.short_description = _(u'Arquivo')

    def __unicode__(self):
        return self.pk

    class Meta:
        verbose_name = _(u'Anexo')
        verbose_name_plural = _(u'Anexos')


class Tramite_Documento(models.Model):
    tramite = models.ForeignKey('Tramite')
    protocolo = models.ForeignKey('Documento', related_name='doc_fk')
    folhas = models.IntegerField(_(u'Número de Folhas'), null=True, blank=True)

    class Meta:
        verbose_name = _(u'Documento do Tramite')
        verbose_name_plural = _(u'Documentos do Tramite')


class Tramite(models.Model):
    data_tramite = models.DateTimeField(_(u'Data do Tramite'),
                                        auto_now_add=True)
    origem = models.ForeignKey(Instituicao,
                               verbose_name=_(u'Instituição Origem'),
                               related_name='TraInstituicoesOri')
    origem_setor = models.ForeignKey(Setor, verbose_name=_(u'Setor Origem'),
                                     related_name='TraSetoresOri')
    destino = models.ForeignKey(Instituicao,
                                verbose_name=_(u'Instituição Destino'),
                                related_name='TraInstituicoesDes')
    destino_setor = models.ForeignKey(Setor, verbose_name=_(u'Setor Destino'),
                                      related_name='TraSetoresDes')
    motivo = models.TextField(_(u'Motivo'), blank=True, null=True)
    protocolo = models.ManyToManyField(Documento,
                                       verbose_name=_(u'Protocolos'),
                                       related_name='TraDocumentos',
                                       through=Tramite_Documento)
                                       # limit_choices_to={'status':
                                       #                   Documento.objects.exclude(
                                       #                       pk=2)})
# Funcao para filtrar os documentos com status diferente de 'Arquivado'
# Nao funciona com o m2m do grappelli, por conta do raw_id_fields

    def get_documentos(self):
        # return self.documento.all()
        # return '<br>' .join([k.protocolo for k in self.documento.all()])
        out = []
        for k in self.protocolo.all():
            out.append(
                # Removi essa parte porque ela inseria o link
                # para o documento e agora nem todos os documentos
                # sao editaveis, entao nao fazia sentido
                # '<a href="../%s/%s">%s</a><br>' % (
                #     Documento._meta.verbose_name.lower(),
                #     k.pk, k.protocolo)
                '%s<br>' % k.protocolo
            )
        return '\n'.join(out)
    get_documentos.allow_tags = True
    get_documentos.short_description = 'Protocolos'

    def get_documentos_guia(self):
        out = []
        for k in self.protocolo.all():
            out.append(
                '<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td><td>%s</td> \
                <td>%s</td></tr>' % (k.protocolo, k.tipo_documento, k.numero,
                                     k.assunto, k.interessado,
                                     k.data_recebimento))
            # out.append(
            #     k.protocolo, k.tipo_documento, k.numero,
            #     k.assunto, k.interessado, k.data_recebimento)
        return ''.join(out)
        # return ''.join(out)
    get_documentos_guia.allow_tags = True

    def __unicode__(self):
        return unicode(self.pk)

    class Meta:
        verbose_name = u'Tramite'
        verbose_name_plural = u'Tramites'


def status_changed(sender, instance, **kwargs):
    """
    funcao que envia um sinal para mudar o status
    dos documentos atraves da tabela: Tramite_Documento
    por conta do InLine no admin
    """
    s = Status.objects.get_or_create(nome='Tramitando')
    if s.pk:
        instance.protocolo.status_id = s.pk
        instance.protocolo.save()

post_save.connect(status_changed,
                  sender=Tramite_Documento,
                  dispatch_uid='status_changed_tramitando')  # weak=False)

# # funcao que envia um sinal para alterar o status dos documentos atraves da
# tabela: Tramite se ela nao tiver um InLine
# start
# def save_handler(sender, instance, *args, **kwargs):
#     m2m_changed.connect(m2m_handler, sender=sender.protocolo.through,
#                         weak=False)

# def m2m_handler(sender, instance, action, *args, **kwargs):
#     if action =='post_clear':
#         for d in Documento.objects.all():
#             # instance.m2m_field.add(sub)
#             d.status_id = 1
#             d.save()

# post_save.connect(save_handler, sender=Tramite, weak=False)
# # end

# def do_something(sender, **kwargs):
    # the object which is saved can be accessed via kwargs 'instance' key.
    # obj = kwargs['instance']
    # print 'the object is now saved.'
    # ...do something else...

# here we connect a post_save signal for MyModel
# in other terms whenever an instance of MyModel is saved
# the 'do_something' function will be called.
# post_save.connect(do_something, sender=Tramite)
