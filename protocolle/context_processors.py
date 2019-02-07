# coding: utf-8

from protocolle.auxiliar.models import (Status)

def get_status_id(status):
    s = Status.objects.get(nome=status)
    return s.pk

