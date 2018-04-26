# -*- coding: utf-8 -*-
from odoo import fields, models, api

class sale(models.Model):
    _inherit = 'sale.order'

    # Add a new column to the res.partner model, by default partners are not
    # instructors

    tr_project_ids = fields.Many2one('tr.project',
        string="Projects")

    tr_take_ids = fields.One2many(
        comodel_name="tr.take.customer",
        inverse_name="order_ids",
        string="Sale Order Data",
        required=False,
    )
    @api.onchange('tr_project_ids')
    def _onchange_tr_project(self):
        project_id = self.tr_take_ids.search([('project_ids', '=', self.tr_project_ids.id)])
        take_list = []
        for r in project_id:
            take_list.append(r.id)
        self.tr_take_ids = take_list

    @api.multi
    def write(self, vals):
        if 'tr_project_id' in vals and vals.get('tr_project_id'):
            for line in self.tr_take_ids:
                line.unlink()
            take_list = []
            pro_obj = self.env['tr.project'].browse(vals.get('tr_project_id'))
            for take_line in pro_obj.tr_take_ids:
                take_list.append(take_line.id)
            vals['tr_take_ids'] = [(6, 0, take_list)]
        res = super(sale, self).write(vals)
        return res

