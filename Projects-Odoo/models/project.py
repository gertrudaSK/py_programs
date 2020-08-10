from datetime import timedelta

from odoo import models, fields, api, _


class Project(models.Model):
    _name = 'projektai.project'
    _description = "Project Demo"

    name = fields.Char(string="Title", required=True)
    description = fields.Text()
    start_date = fields.Date(string="Start Date", default=fields.Date.today)
    end_date = fields.Date(string="End Date")
    klientas_id = fields.Many2one('res.partner',
                                  ondelete='set null', string="Client",
                                  index=True)
    vadovas_id = fields.Many2one('hr.employee', string="Manager",
                                 domain=[('vadovas', '=',
                                          True)])
    color = fields.Integer()

    darbuotojas_ids = fields.Many2many('hr.employee', string="Employee")
    darbai_ids = fields.One2many('projektai.works', 'projektas_id',
                                 string="Works")
    invoice_ids = fields.One2many('projektai.invoice', 'projektas_id',
                                  string="Invoices")

    employee_percentage = fields.Float(string='Employees percentage',
                                       compute='_involved_employees')

    end_date_calendar = fields.Date(string='End', compute='_get_end_date')

    employees_count = fields.Integer(string="Employees Count",
                                     compute="_get_count", store=True)

    status = fields.Selection([
        ('draft', "Draft"),
        ('started', "Started"),
        ('done', "Done"),
        ('cancelled', "Cancelled"),
    ], string="Progress", default='draft', translate=True)

    image = fields.Binary("Image", attachment=True)

    document_ids = fields.One2many('projektai.document', 'project_id',
                                   string='Documents')

    def send_project_report(self):
        # Find the e-mail template
        template = self.env.ref('projektai.projektai_project_mail_template')
        # You can also find the e-mail template like this:
        # template = self.env['ir.model.data'].get_object('send_mail_template_demo', 'example_email_template')

        # Send out the e-mail template to the user
        self.env['mail.template'].browse(template.id).send_mail(self.id)

    @api.depends('darbuotojas_ids')
    def _get_count(self):
        for r in self:
            r.employees_count = len(r.darbuotojas_ids)

    @api.depends('end_date')
    def _get_end_date(self):
        for r in self:
            one_day = timedelta(days=1)
            r.end_date_calendar = r.end_date + one_day

    @api.depends('darbuotojas_ids')
    def _involved_employees(self):
        total_sum = self.env['hr.employee'].search_count([])
        for r in self:
            r.employee_percentage = 100 * len(r.darbuotojas_ids) / total_sum

    @api.depends('vadovas_id')
    def function(self):
        for r in self:
            # ids = [5, 7, 8, 12]
            self.update({
                'darbuotojas_ids': [[4, False, r.vadovas_id.id]]
            })


class ProjectDocument(models.Model):
    _name = 'projektai.document'

    name = fields.Char(string='Filename')
    file = fields.Binary(string=_('File'), attachment=True)
    comment = fields.Text(string=_('Notes'))

    project_id = fields.Many2one('projektai.project')

    # @api.depends('vadovas_id')
    # def _manager(self):
    #     for r in self:
    # if r.vadovas_id:
    #     project_id = self.env['projektai.project'].browse(
    #         self._context.get(
    #             'active_ids'))
    #     values = {'projektai_project_id': project_id, 'hr_amployee_id':
    #         r.vadovas_id}
    #
    #     id = self.env['hr.employee_projektai_project_rel'].create(
    #         values)

    # r.write({'darbuotojas_ids':[(4,[r.vadovas_id.id])]})

    # r.darbuotojas_ids = [(4,[r.vadovas_id.id])]
