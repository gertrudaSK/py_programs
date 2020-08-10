from odoo import models, fields, api


class Invoice(models.Model):
    _name = 'projektai.invoice'
    _description = "Invoice Demo"

    number = fields.Char(string="Invoice Number", required=True)
    date = fields.Date(string="Date", default=fields.Date.today)
    klientas_id = fields.Many2one('res.partner',
                                  ondelete='set null', string="Client",
                                  index=True)
    projektas_id = fields.Many2one('projektai.project')
    line_id = fields.One2many('projektai.invoiceline', 'invoice_id',
                              string="Lines")

    our_company_name = fields.Char(compute='_compute_data')
    company_ID = fields.Char(compute='_compute_data')
    company_address = fields.Char(compute='_compute_data')

    client_ID = fields.Char(compute='_get_client_data')
    client_address = fields.Char(compute='_get_client_data')
    subtotal = fields.Float(string="Subtotal", compute='_subtotal')
    taxes = fields.Float(string="VAT(21%)", compute='_taxes')
    total = fields.Float(string="Total (EUR)", compute="_total")

    @api.depends('subtotal', 'taxes')
    def _total(self):
        for r in self:
            r.total = round(r.subtotal + r.taxes, 2)

    @api.depends('subtotal')
    def _taxes(self):
        for r in self:
            r.taxes = round(r.subtotal * 0.21, 2)

    @api.depends('number')
    def _subtotal(self):
        for r in self:
            total = self.env['projektai.invoice'].search([('number',
                                                           '=',
                                                           r.number)]).line_id
            items = []
            for i in total:
                items.append(i.total_price)
            r.subtotal = round(sum(items), 2)

    def _compute_data(self):
        for r in self:
            r.our_company_name = "Our Company Title"
            r.company_ID = "1111111"
            r.company_address = "Address"

    @api.depends('klientas_id')
    def _get_client_data(self):
        for r in self:
            r.client_ID = self.env['res.partner'].search([('id', '=',
                                                           r.klientas_id.id)]).zip
            address1 = self.env['res.partner'].search([('id', '=',
                                                        r.klientas_id.id)]).street

            r.client_address = str(address1)


class InvoiceLine(models.Model):
    _name = 'projektai.invoiceline'

    description = fields.Many2one('projektai.works')
    total_price = fields.Float(compute='_total_price', store=True)
    invoice_id = fields.Many2one('projektai.invoice')
    quantity = fields.Integer()
    unite_price = fields.Float()

    @api.depends('quantity', 'unite_price')
    def _total_price(self):
        for r in self:
            r.total_price = round(r.unite_price * r.quantity, 2)
