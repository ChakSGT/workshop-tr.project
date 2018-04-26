
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class Course(models.Model):
    _name = 'tr.project'

    name = fields.Char(
        string="Name of Project",
        required=True,
    )
    code = fields.Text(
        string="Project ID",
        required=True,
    )
    budget = fields.Float(
        digits=(6, 2),
        string="Budget",
        domain=[('budget', '>', 0)],
        required=True,
    )
    customer_ids = fields.One2many(
        comodel_name="tr.take.customer",
        inverse_name="project_ids",
        string="Customers",
        domain=[('state', '!=', 'reject')],
        required=False,
        readonly=True,
    )
    balance = fields.Float(
        digits=(6, 2),
        string="Balance",
        compute='_compute_balance',
        required=False,
        readonly=True,
    )

    @api.multi
    @api.constrains('code')
    def _identify_same_code(self):
        for r in self:
            obj = self.search([('code', '=ilike', r.code), ('id', '!=', r.id)])
            if obj:
                raise ValidationError("Code duplicate")

    @api.constrains('budget')
    def _check_budget(self):
        if self.budget < 0:
            raise ValidationError("Budget more than 0")

    @api.multi
    @api.depends('customer_ids')
    def _compute_balance(self):
        for r in self:
            r.balance = r.budget
            ans = 0
            for history in r.customer_ids:
                if history.state == "approve":
                    ans += history.money
            r.balance = r.budget-ans

class Session(models.Model):
    _name = 'tr.take.customer'

    state = fields.Selection([
        ('draft', 'Draft'),
        ('wait', 'Wait'),
        ('approve', 'Approve'),
        ('reject', 'Reject'),
    ], default='draft')

    date = fields.Date(
        string="Date",
        required=True,
    )

    cur_date = fields.Date.today()

    user = fields.Many2one(
        comodel_name="res.partner",
        string="User",
        required=True,
        domain=[('customer', '=', True)],
    )
    project_ids = fields.Many2one(
        string="Projects",
        comodel_name="tr.project",
        required=True,
    )
    balance = fields.Float(
        string="Balance",
        related="project_ids.balance",
        readonly=True,
    )
    sale_ids = fields.Many2many(
        comodel_name="res.users",
        string="Sale",
    )
    new_field_ids = fields.Many2many(
        comodel_name="",
        relation="",
        column1="",
        column2="",
        string="",
    )

    money = fields.Float(
        string="Money",
        digit=(6, 2),
        required=True,
    )
    delete_ids = fields.Many2many(
        comodel_name="delete.wizard",
        string="Deletes",
    )
    order_ids = fields.Many2one('sale.order')

    # @api.multi
    # @api.constrains('user')
    # def _identify_same_user(self):
    #     for r in self:
    #         obj = self.search([('user', '=', r.user), ('date', '=', r.date)])
    #         if obj:
    #             raise ValidationError("Please try again select user")


    @api.constrains('money')
    def _check_money(self):
        if self.money < 0:
            raise ValidationError("Please try again input money")

    @api.constrains('date')
    def _check_date(self):
        if self.date < self.cur_date:
            raise ValidationError("Please try again select date")


    @api.constrains('money')
    def _check_something(self):
        for r in self:
            if r.money < r.balance:
                r.state = 'approve'

    @api.multi
    def action_request(self):
        self.state = 'wait'

    @api.multi
    def action_approve(self):
        self.state = 'approve'

    @api.multi
    def action_reject(self):
        self.state = 'reject'



