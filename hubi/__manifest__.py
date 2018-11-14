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
             "views/shipper_views.xml",
             "views/table_base_views.xml",
             "views/inherited_partner_views.xml",
             "views/inherited_product_template_views.xml",
             "views/inherited_mrp_bom_views.xml",
             "wizard/wiz_create_productprice_views.xml",
             "wizard/wiz_search_product_views.xml",
             "views/inherited_product_pricelist_views.xml",
             "views/inherited_sale_order_views.xml",
             "views/palletization_views.xml",
             "views/inherited_account_invoice_views.xml",
             "views/inherited_account_payment_views.xml",
             "views/inherited_delivery_carrier_views.xml",
             #"views/inherited_account_view.xml",
             
    ],
    'qweb': ['static/src/xml/qweb.xml'],
    'installable': True,
    'application': False,
    'auto_install': False,
}
