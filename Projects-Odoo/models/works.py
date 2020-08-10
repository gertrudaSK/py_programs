from odoo import models, fields, api


class Works(models.Model):
    _name = 'projektai.works'
    _description = "Works Demo"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    projektas_id = fields.Many2one('projektai.project')
    darbuotojas_ids = fields.Many2many('hr.employee', string="Employee")
    darbuotojas_ids = fields.Many2many('hr.employee', string="Employee")
