from odoo import models, fields, api


class Wizard(models.TransientModel):
    _name = 'projektai.wizard'
    _description = "Wizard: Quick Registration of Attendees to Sessions"

    def _default_session(self):
        return self.env['projektai.project'].browse(
            self._context.get('active_id'))

    projektas_id = fields.Many2one('projektai.project',
                                   string="Project", required=True,
                                   default=_default_session)
    darbuotojas_ids = fields.Many2many('hr.employee', string="Employee")

    def subscribe(self):
        for session in self.projektas_id:
            session.darbuotojas_ids |= self.darbuotojas_ids
        return {}
