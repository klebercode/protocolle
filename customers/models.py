# coding: utf-8

from django.db import models
from django.utils.translation import ugettext_lazy as _

from tenant_schemas.models import TenantMixin

from protocolle.auxiliar.models import Instituicao


class Client(TenantMixin):
    institute = models.ForeignKey(Instituicao, verbose_name=_(u'Instituição'),
                                  blank=True, null=True)
    name = models.CharField(max_length=100)
    paid_until = models.DateField()
    on_trial = models.BooleanField()
    created_on = models.DateField(auto_now_add=True)

    # default true, schema will be automatically created
    # and synced when it is saved
    auto_create_schema = True

    def __unicode__(self):
        return unicode(self.name)

    class Meta:
        verbose_name = u'Cliente'
        verbose_name_plural = u'Clientes'
