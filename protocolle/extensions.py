# coding: utf-8

from django.core.urlresolvers import reverse_lazy

# from grappelli_extensions.nodes import CLNode


class Navbar(object):
    nodes = (
        ('Tramites', {'nodes': (
            ('Documentos', {
                'url': reverse_lazy('admin:protocolo_tramite_changelist'),
                'perm': 'protocolo.change_tramite',
            }),
        )}),
        ('Protocolos', {'nodes': (
            ('Documentos', {
                'url': reverse_lazy('admin:protocolo_documento_changelist'),
                'perm': 'protocolo.change_documento',
            }),
        )}),
        ('Cadastros', {'nodes': (
            ('Instituições', {
                'url': reverse_lazy('admin:auxiliar_instituicao_changelist'),
                'perm': 'auxiliar.change_classe',
            }),
            ('Pessoas', {
                'url': reverse_lazy('admin:auxiliar_pessoa_changelist'),
                'perm': 'auxiliar.change_pessoa',
            }),
            ('Setores', {
                'url': reverse_lazy('admin:auxiliar_setor_changelist'),
                'perm': 'auxiliar.change_setor',
            }),
        )}),
        ('Configurações', {'nodes': (
            ('Carateres', {
                'url': reverse_lazy('admin:core_carater_changelist'),
                'perm': 'core.change_classe',
            }),
            ('Grupos', {
                'url': reverse_lazy('admin:core_grupo_changelist'),
                'perm': 'core.change_classe',
            }),
            ('Naturezas', {
                'url': reverse_lazy('admin:core_natureza_changelist'),
                'perm': 'core.change_classe',
            }),
            ('Status', {
                'url': reverse_lazy('admin:core_status_changelist'),
                'perm': 'core.change_classe',
            }),
            ('Tipos de Documento', {
                'url': reverse_lazy('admin:core_tipodocumento_changelist'),
                'perm': 'core.change_tipodocumento',
            }),
            ('Tipos de Instituição', {
                'url': reverse_lazy('admin:core_tipoinstituicao_changelist'),
                'perm': 'core.change_tipoinstituicao',
            }),
        )}),
        ('Administração', {'nodes': (
            ('Usuários', {
                'url': reverse_lazy('admin:auth_user_changelist'),
                'perm': 'auth.change_user',
            }),
            ('Grupos', {
                'url': reverse_lazy('admin:auth_group_changelist'),
                'perm': 'auth.change_group',
            }),
            ('Clientes', {
                'url': reverse_lazy('admin:customers_client_changelist'),
                'perm': 'customers.change_client',
            }),
        )}),
        # ('Sites',
        #     {'url': reverse_lazy('admin:sites_site_changelist')}),
        # ('Nodes', {'nodes': (
        #     CLNode('auth', 'user'),
        #     CLNode('sites', 'site'),
        # )}),
        # CLNode('auth', 'user', u"Site users"),
    )


class Sidebar(object):
    nodes = (
        ('Administração', {'nodes': (
            ('Usuários', {
                'url': reverse_lazy('admin:auth_user_changelist'),
                'perm': 'auth.change_user',
            }),
            ('Grupos', {
                'url': reverse_lazy('admin:auth_group_changelist'),
                'perm': 'auth.change_group',
            }),
        )}),
        # ('Sites',
        #     {'url': reverse_lazy('admin:sites_site_changelist')}),
        # ('Nodes', {'nodes': (
        #     CLNode('auth', 'user'),
        #     CLNode('sites', 'site'),
        # )}),
        # CLNode('auth', 'user', u"Site users"),
    )
