from odoo import models, fields, api


class Partner(models.Model):
    _inherit = 'res.partner'

    projektas_ids = fields.One2many('projektai.project', 'klientas_id',
                                    string="Project", readonly='True')
