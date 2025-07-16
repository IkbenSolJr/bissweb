# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models
from odoo.osv import expression

class HrAttendance(models.Model):
    _inherit = "hr.employee"

    last_check_in = fields.Datetime(
        related='last_attendance_id.check_in', store=True)
    last_check_out = fields.Datetime(
        related='last_attendance_id.check_out', store=True) 
