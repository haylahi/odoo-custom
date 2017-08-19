# -*- coding: utf-8 -*-
{
    'name': "Petroamerica",

    'summary': """
        Este modulo ha sido creado para el proyecto Petroamerica""",

    'description': """
        Este modulo permite crear y administrar los permisos de usuario (under Settings > Users)
    """,

    'author': "Ricardo Livelli Salazar",
    'website': "http://www.myrconsulting.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
    'security/user_groups.xml',
	'security/ir.model.access.csv',
	'security/petro_access_rules.xml',
	'views/user_access_views.xml'
    ],
}
