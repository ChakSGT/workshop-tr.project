# -*- coding: utf-8 -*-

from odoo import models, fields, api

class Wizard(models.TransientModel):
    _name = 'change.date'

    date_visit = fields.Date(
        string="Date",
        required=True,
    )

    def confirm_change_date(self):
        active_model = self._context['active_model']
        active_id = self._context['active_id']
        tr_visit = self.env[active_model]
        visits = tr_visit.browse(active_id)
        for visit in visits:
            visit.write({
                'date': self.date_visit,
            })

class delete(models.TransientModel):
    _name = 'delete.wizard'

    @api.multi
    def _get_customer(self):
        visits = self.env['tr.take.customer'].search([
            '|',
            ('state', '=', 'reject'),
            '&',
            ('state', '=', 'draft'),
            ('money', '<', '1000'),
        ])
        visit_ids = []
        for visit in visits:
            visit_ids.append(visit.id)

        return visit_ids

    customer_ids = fields.Many2many(
        comodel_name="tr.take.customer",
        string="Record to delete",
        required=False,
        default=_get_customer,
    )

    @api.multi
    def confirm_delete(self):
        for de in self.customer_ids:
            de.unlink()
        return {}

class change_state(models.TransientModel):
    _name = 'change.state'

    @api.multi
    def _get_customer(self):
        visits = self.env['tr.take.customer'].search([
            ('state', '=', 'wait'),
        ])
        visit_ids = []
        for visit in visits:
            visit_ids.append(visit.id)

        return visit_ids

    customer_ids = fields.Many2many(
        comodel_name="tr.take.customer",
        string="Record to change state",
        required=False,
        default=_get_customer,
    )

    @api.multi
    def confirm_change_state(self):
        for de in self.customer_ids:
            de.write({
                'state': 'approve',
            })
