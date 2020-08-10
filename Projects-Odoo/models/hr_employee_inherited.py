from odoo import models, fields, api


class Employee(models.Model):
    _inherit = 'hr.employee'

    vadovas = fields.Boolean(string="Manager", default=False)
    projektas_ids = fields.Many2many('projektai.project', string="Project",
                                     readonly='True')
    work_ids = fields.Many2many('projektai.works', string="Works",
                                readonly='True')
