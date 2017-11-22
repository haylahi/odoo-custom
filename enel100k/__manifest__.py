# -*- coding: utf-8 -*-
{
    'name': "Enel100K",

    'summary': """
        Proyecto 100K""",

    'description': """
        Colecta de información de clientes en los locales de Enel Perú.
    """,

    'author': "MYR CONSULTORIA EN SISTEMAS SAC ",
    'website': "http://www.myrconsulting.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category': 'Todoo',
    'version': '0.1.2',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','inputmask_widget','web_export_view'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'security/access_rules.xml',
        'views/views.xml',
        'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}