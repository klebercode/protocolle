# coding: utf-8
from django import forms
from django.utils.translation import ugettext_lazy as _

from protocolle.current_user import get_current_user


class CreateAdminForm(forms.Form):
    _selected_action = forms.CharField(widget=forms.MultipleHiddenInput)
    username = forms.CharField(label=_(u'Usuário'), widget=forms.TextInput(
                               attrs={'value': get_current_user().username}))
    email = forms.EmailField(label=_(u'Email'), widget=forms.TextInput(
                             attrs={'value': get_current_user().email}))
    password = forms.CharField(label=_(u'Senha'), widget=forms.PasswordInput())

    # TODO: estudar mais sobre isso
    # def __init__(self, request, *args, **kwargs):
    #     super(CreateAdminForm, self).__init__(*args, **kwargs)
    #     self.fields['username'].widget.attrs['value'] = request.user.username
    #     self.fields['email'].widget.attrs['value'] = request.user.email
