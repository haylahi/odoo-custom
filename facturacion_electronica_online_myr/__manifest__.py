# -*- coding: utf-8 -*-
{
    'name': "CPE - Online MyR",

    'summary': """
        Facturación Electrónica - Online 2018""",

    'description': """
        Facturación Electrónica - Online 2018
    """,

    'author': "MYR CONSULTORIA EN SISTEMAS SAC ",
    'website': "http://www.myrconsulting.net",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/openerp/addons/base/module/module_data.xml
    # for the full list
    'category' : 'Accounting & Finance',
    'version': '1.0.0',

    # any module necessary for this one to work correctly
    'depends': ['base','mail','account','odoope_einvoice_base','odoope_ruc_validation','odoope_toponyms'],

    # always loaded
    'data': [
        'data/ir.config_parameter.xml',
        'data/ir.ui_view.xml',
        'views/account_invoice_view.xml',
        #'security/access_rules.xml',
        #'views/views.xml',
        #'views/templates.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'auto_install': False,
    'application': True,
}