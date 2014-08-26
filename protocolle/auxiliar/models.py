# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User

from protocolle.core.models import (TipoInstituicao, Grupo, STATE_CHOICES)


class Pessoa(models.Model):
    nome = models.CharField(_(u'Nome'), max_length=200)
    email = models.EmailField(_(u'E-mail'), null=True, blank=True)
    fone = models.CharField(_(u'Fone'), max_length=20, null=True, blank=True)
    endereco = models.CharField(_(u'Endereço'), max_length=200,
                                help_text=_(u'Rua / Avenida'), null=True,
                                blank=True)
    numero = models.IntegerField(_(u'Número'), null=True, blank=True)
    bairro = models.CharField(_(u'Bairro'), max_length=150, null=True,
                              blank=True)
    complemento = models.CharField(_(u'Complemento'), max_length=200,
                                   help_text=_(u'Apartamento / Sala / \
                                               Referência'),
                                   null=True, blank=True)
    cep = models.CharField(_(u'CEP'), max_length=10, null=True, blank=True)
    cidade = models.CharField(_(u'Cidade'), max_length=150, null=True,
                              blank=True)
    uf = models.CharField(_(u'UF'), max_length=2, null=True, blank=True,
                          choices=STATE_CHOICES)

    # def clean(self):
    #   if not self.instituicao.grupo == self.instituicao.grupo:
    #       raise ValidationError('Erro!')

    def __unicode__(self):
        return unicode(self.nome)

    class Meta:
        verbose_name = _(u'Pessoa')
        verbose_name_plural = _(u'Pessoas')
        ordering = ['nome']


class Instituicao(models.Model):
    nome = models.CharField(_(u'Nome'), max_length=100,
                            help_text=_(u'Nome da instituição'))
    tipo_instituicao = models.ForeignKey(TipoInstituicao,
                                         verbose_name=_(u'Tipo de \
                                                        Instituição'),
                                         related_name='InsTiposInstituicao')
    grupo = models.ForeignKey(Grupo, verbose_name=_(u'Grupo'),
                              related_name='InsGrupos')
    email = models.EmailField(_(u'E-mail'), null=True, blank=True)
    fone = models.CharField(_(u'Fone'), max_length=20, null=True, blank=True)
    endereco = models.CharField(_(u'Endereço'), max_length=200,
                                help_text=_(u'Rua / Avenida'),
                                null=True, blank=True)
    numero = models.IntegerField(_(u'Número'), null=True, blank=True)
    bairro = models.CharField(_(u'Bairro'), max_length=150, null=True,
                              blank=True)
    complemento = models.CharField(_(u'Complemento'), max_length=200,
                                   help_text=_(u'Apartamento / Sala / \
                                               Referência'),
                                   null=True, blank=True)
    cep = models.CharField(_(u'CEP'), max_length=10, null=True, blank=True)
    cidade = models.CharField(_(u'Cidade'), max_length=150, null=True,
                              blank=True)
    uf = models.CharField(_(u'UF'), max_length=2, blank=True, null=True,
                          choices=STATE_CHOICES)

    # def clean(self):
    #   if not self.grupo.tipo_instituicao == self.grupo.tipo_instituicao:
    #       raise ValidationError('Erro!')

    def __unicode__(self):
        return unicode(self.nome)

    class Meta:
        verbose_name = _(u'Instituição')
        verbose_name_plural = _(u'Instituições')
        ordering = ['nome']


class Setor(models.Model):
    instituicao = models.ForeignKey('Instituicao',
                                    verbose_name=_(u'Instituição'),
                                    related_name='SetorInstituicoes')
    nome = models.CharField(_(u'Nome'), max_length=100)
    sigla = models.CharField(_(u'Sigla'), max_length=20)
    responsavel = models.ForeignKey(Pessoa, verbose_name=u'Responsável',
                                    related_name='SetorResponsaveis')

    # def clean(self):
    #   if not self.instituicao.grupo == self.instituicao.grupo:
    #       raise ValidationError('Erro!')

    def __unicode__(self):
        return unicode(self.nome)

    class Meta:
        verbose_name = _(u'Setor')
        verbose_name_plural = _(u'Setores')
        ordering = ['nome']


class Instituicao_User(models.Model):
    user = models.OneToOneField(User, unique=True)
    instituicao = models.ForeignKey('Instituicao',
                                    verbose_name=_(u'Instituição'),
                                    blank=True, null=True)

    def __unicode__(self):
        return unicode(self.user)

    class Meta:
        verbose_name = _(u'Instituição')
        verbose_name_plural = _(u'Instituições')


# from django.db.models.signals import post_save

# def create_profile(sender, instance, created, **kwargs):
#     if created:
#         profile, created = UserProfile.objects.get_or_create(user=instance)

# post_save.connect(create_profile, sender=User)
