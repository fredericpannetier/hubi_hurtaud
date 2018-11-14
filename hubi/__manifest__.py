# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.
{
    'name' : 'hubi',
    'version' : '1.0',
    'summary': 'hubi',
    'description': """
Gestion HUBI
""",
    
	'depends' : ['base','base_setup','product','analytic','mail','sale','hubiBOM','delivery'],
    'data': ["data/hubi_template_email.xml",
             "views/module_option_views.xml",
             "wizard/wiz_confirm_dialog_views.xml",
             
             
    ],
    'qweb': ['static/src/xml/qweb.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
