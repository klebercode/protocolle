# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _


STATE_CHOICES = (
    ('AC', u'Acre'),
    ('AL', u'Alagoas'),
    ('AP', u'Amapá'),
    ('AM', u'Amazonas'),
    ('BA', u'Bahia'),
    ('CE', u'Ceará'),
    ('DF', u'Distrito Federal'),
    ('ES', u'Espírito Santo'),
    ('GO', u'Goiás'),
    ('MA', u'Maranhão'),
    ('MT', u'Mato Grosso'),
    ('MS', u'Mato Grosso do Sul'),
    ('MG', u'Minas Gerais'),
    ('PA', u'Pará'),
    ('PB', u'Paraíba'),
    ('PR', u'Paraná'),
    ('PE', u'Pernambuco'),
    ('PI', u'Piauí'),
    ('RJ', u'Rio de Janeiro'),
    ('RN', u'Rio Grande do Norte'),
    ('RS', u'Rio Grande do Sul'),
    ('RO', u'Rondônia'),
    ('RR', u'Roraima'),
    ('SC', u'Santa Catarina'),
    ('SP', u'São Paulo'),
    ('SE', u'Sergipe'),
    ('TO', u'Tocantins'),
)

OPERATION_CHOICES = (
    (1, u'Entrada'),
    (2, u'Saída'),
)


class TipoDocumento(models.Model):
    nome = models.CharField(_(u'Nome'), max_length=100,
                            help_text=_(u'Carta / Ofício / Balancete'))

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = _(u'Tipo de Documento')
        verbose_name_plural = _(u'Tipos de Documento')
        ordering = ['nome']


class Carater(models.Model):
    nome = models.CharField(_(u'Nome'), max_length=30,
                            help_text=_(u'Normal / Urgente / Urgentissímo'))

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = _(u'Caráter')
        verbose_name_plural = _(u'Caráteres')
        ordering = ['nome']


class Natureza(models.Model):
    nome = models.CharField(_(u'Nome'), max_length=20,
                            help_text=_(u'Aberto / Sigiloso'))

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = _(u'Natureza')
        verbose_name_plural = _(u'Naturezas')
        ordering = ['nome']


class Status(models.Model):
    nome = models.CharField(_(u'Nome'), max_length=20,
                            help_text=_(u'Tramitando / Arquivado / Parado \
                                        / Entregue'))

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = _(u'Status')
        verbose_name_plural = _(u'Status')
        ordering = ['nome']


class TipoInstituicao(models.Model):
    nome = models.CharField(_(u'Nome'), max_length=20,
                            help_text=_(u'Interna / Externa'))

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = _(u'Tipo de Instituição')
        verbose_name_plural = _(u'Tipos de Instituição')
        ordering = ['nome']


class Grupo(models.Model):
    nome = models.CharField(_(u'Nome'), max_length=100,
                            help_text=_(u'Empresa Privada / Orgão Público / Administração Direta'))
    tipo_instituicao = models.ForeignKey(TipoInstituicao,
                                         verbose_name=_(u'Tipo de Instituição'),
                                         related_name='TiposInstituicao')

    def __unicode__(self):
        return self.nome

    class Meta:
        verbose_name = _(u'Grupo')
        verbose_name_plural = _(u'Grupos')
        ordering = ['nome']

