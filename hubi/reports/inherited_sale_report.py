# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import tools
from odoo import fields, models


class HubiSaleReport(models.Model):
    _inherit = "sale.report"

    carrier_name = fields.Char('Carrier Name', readonly=True)
    category_name = fields.Char('Category Name', readonly=True)
    caliber_name = fields.Char('Caliber Name', readonly=True)
    packaging_name = fields.Char('Packaging Name', readonly=True)
    
    packaging_date = fields.Datetime('Date Order', readonly=True)
    sending_date = fields.Datetime('Sending Date', readonly=True)
    effective_date = fields.Datetime('Effective Date', readonly=True)
    invoice_status = fields.Selection([
        ('upselling', 'Upselling Opportunity'),
        ('invoiced', 'Fully Invoiced'),
        ('to invoice', 'To Invoice'),
        ('no', 'Nothing to Invoice')
        ], string='Invoice Status', readonly=True)
    price_weight = fields.Float(string='Price Weight', group_operator='avg', readonly=True)
    

    def _select(self):
        return super(HubiSaleReport, self)._select() + """,dc.name as carrier_name,
                pc.complete_name as category_name, hfc.name as caliber_name, 
                hfp.name as packaging_name, s.effective_date as effective_date, 
                s.sending_date as sending_date, s.packaging_date as packaging_date,
                s.invoice_status as invoice_status, avg(l.price_weight) as price_weight"""

    def _from(self):
        return super(HubiSaleReport, self)._from() + """left join delivery_carrier dc on (s.carrier_id = dc.id)
                    left join product_category pc on (t.categ_id = pc.id)
                    left join hubi_family hfc on (t.caliber_id = hfc.id)
                    left join hubi_family hfp on (t.packaging_id = hfp.id)"""

    def _group_by(self):
        return super(HubiSaleReport, self)._group_by() + """, dc.name,
                    pc.complete_name, hfc.name,hfp.name,
                    s.effective_date, s.sending_date,
                    s.packaging_date, s.invoice_status"""
                    
