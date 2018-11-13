# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, RedirectWarning, except_orm, Warning
from . import tools_hubi
   
class HubiProductPriceList(models.Model):
    _inherit = "product.pricelist"
    
    shipping = fields.Boolean(string='Shipping', default=False)
    shipping_price_kg = fields.Float(string='Shipping Price Kg')
    
class HubiProductPriceListItem(models.Model):
    _inherit = "product.pricelist.item"
    
    def _is_Visible(self):
        return tools_hubi._is_Visible_class(self, 'PriceList')

    def _default_is_Visible(self, valeur):
        return tools_hubi._default_is_Visible_class(self,valeur) 

    @api.one
    @api.depends('categ_id', 'product_tmpl_id', 'product_id', 'pricelist_id')
    def _get_pricelistitem_info(self):
        if self.categ_id:
            self.info_price = _("") 
        elif self.product_tmpl_id:
            #products_templ=self.env['product.template']
            products_templ = self.env['product.template'].search([('id', '=', self.product_tmpl_id.id)])            
            #self.info_price = ("%s %s %s %s") % (products_templ.categ_id.display_name, products_templ.family_id.name, products_templ.weight, products_templ.uom_id.name)
            #self.info_price = ("%s %s %s %s %s %s %s") % (products_templ.categ_id.display_name,"/", products_templ.caliber_id.name,"/", products_templ.packaging_id.name,"/", products_templ.quantity)
            price_kg = 0
            
            #if self.base == 'pricelist' and self.base_pricelist_id:
            #        price_tmp = self.base_pricelist_id._compute_price_rule([(products_templ, qty, partner)])[products_templ.id][0] 
            #        price = self.base_pricelist_id.currency_id.compute(price_tmp, self.currency_id, round=False)
            #else:
            #        price = products_templ.price_compute(self.base)[product.id]
            
            price_uom = self.env['product.uom'].browse([products_templ.uom_id.id])
            
            if self.base == 'standard_price':
                price = products_templ.standard_price
            else:    
                price = products_templ.list_price
            convert_to_price_uom = (lambda price: products_templ.uom_id._compute_price(price, price_uom))

            if price is not False:
                if self.compute_price == 'fixed':
                        price = convert_to_price_uom(self.fixed_price)
                elif self.compute_price == 'percentage':
                        price = (price - (price * (self.percent_price / 100))) or 0.0
                else:
                    # formula
                    price_limit = price
                    price = (price - (price * (self.price_discount / 100))) or 0.0
                    if self.price_round:
                        price = tools.float_round(price, precision_rounding=self.price_round)

                    if self.price_surcharge:
                        price_surcharge = convert_to_price_uom(self.price_surcharge)
                        price += price_surcharge

                    if self.price_min_margin:
                        price_min_margin = convert_to_price_uom(self.price_min_margin)
                        price = max(price, price_limit + price_min_margin)

                    if self.price_max_margin:
                        price_max_margin = convert_to_price_uom(self.price_max_margin)
                        price = min(price, price_limit + price_max_margin)
               
                if products_templ.weight:
                    price_kg = price / products_templ.weight
                    
            self.info_price = ("%s %s %s %s %s %s %.2f %s %s %s") % (products_templ.quantity," ",products_templ.uom_id.name, ' - ',products_templ.weight," Kg - ", price_kg," ", self.currency_id.symbol," /Kg")
        elif self.product_id:
            self.info_price = _("")
        else:
            self.info_price = _("")
            
    @api.one
    @api.depends('categ_id', 'product_tmpl_id', 'product_id', 'pricelist_id')
    def _get_default_price(self):
        if self.categ_id:
            self.default_price = '0'
        elif self.product_tmpl_id:
            products_templ=self.env['product.template']
            products_templ = self.env['product.template'].search([('id', '=', self.product_tmpl_id.id)])            
            
            self.default_price = ("%s") % (products_templ.list_price)
        elif self.product_id:
            self.default_price = '0'
        else:
            self.default_price = '0'            

    @api.onchange('price_ean13')
    def _onchange_barcode(self):
        # Test si code EAN13 correct
        #result = {}
        if self.price_ean13:
            if (len(self.price_ean13) < 12 or len(self.price_ean13) > 14):
                raise ValidationError("ERROR : Barcode EAN13. The length is invalid")
            else:
                cle_ean13 = tools_hubi.calcul_cle_code_ean13(self, self.price_ean13)
                self.price_ean13 = tools_hubi.mid(self.price_ean13,0,12) + cle_ean13


    price_option = fields.Boolean(string='Price Option', default=False)
    price_color = fields.Selection([("#FF00FF", "magenta"),("#0000FF", "blue"),
                                    ("#FFFF00", "yellow"),("#FF0000", "red"),
                                    ("#008000", "green"),("#D2691E", "brown"),
                                    ("#FFFFFF", "white"),("#CCCCCC", "grey"),
                                    ("#FFC0CB", "pink")], string='Price Color')
    internal_code = fields.Char(string='Internal Code')
    price_ean13 = fields.Char(string='Price EAN13')
    price_ifls = fields.Char(string='Price IFLS')
    customer_ref = fields.Char(string='Customer Ref')
    description_promo = fields.Char(string='Description Promo')
    #price_printer = fields.Char(string='Price Printer')
    price_printer =  fields.Many2one('hubi.printer', string='Label Printer', domain=[('isimpetiq', '=', True)])
    etiq_format = fields.Selection([("1", "large"),("2", "small"),("3", "weight"),("4", "other")], string="Etiq Format")
    etiq_modele = fields.Selection([("1", "classic"),("2", "FD Taste of the quality"),
                                    ("3", "Taste of the quality"),("4", "carton")], string="Etiq Modele")
   
    info_price = fields.Char(
        'Info', compute='_get_pricelistitem_info',
        help="Information for this product (Quantity - Weight - Price weight")
    default_price = fields.Char('Default Price', compute='_get_default_price', help="Default price for this product.")
    #color = fields.Integer(string='Price Color')
    label_model_id =  fields.Many2one('hubi.labelmodel', string='Label model')

    is_ifls=fields.Boolean(string='is_IFLS', compute='_is_Visible', default=lambda self: self._default_is_Visible('GESTION_IFLS'))
    is_etiq_format=fields.Boolean(string='is_ETIQ_FORMAT', compute='_is_Visible', default=lambda self: self._default_is_Visible('ETIQ_FORMAT'))
    is_etiq_mode=fields.Boolean(string='is_ETIQ_MODE', compute='_is_Visible', default=lambda self: self._default_is_Visible('ETIQ_MODE'))
    is_tarif_option=fields.Boolean(string='is_TARIF_OPTION', compute='_is_Visible', default=lambda self: self._default_is_Visible('TARIF_OPTION'))
    is_tarif_code_interne=fields.Boolean(string='is_CODE_INTERNE', compute='_is_Visible', default=lambda self: self._default_is_Visible('TARIF_CODE_INTERNE'))
    is_tarif_ref_client=fields.Boolean(string='is_REF_CLIENT', compute='_is_Visible', default=lambda self: self._default_is_Visible('TARIF_REF_CLIENT'))
    is_tarif_lib_promo=fields.Boolean(string='is_LIB_PROMO', compute='_is_Visible', default=lambda self: self._default_is_Visible('TARIF_LIB_PROMO'))
