# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class UserHoliday(models.Model):
    _inherit = "hr.leave"

    leave_manager_id = fields.Many2one(related='employee_id.leave_manager_id', string="Người duyệt")
    # show_leaves = fields.Boolean(related='employee_id.show_leaves')
    # allocation_used_count = fields.Float(related='employee_id.allocation_used_count')
    # allocation_count = fields.Float(related='employee_id.allocation_count')
    # leave_date_to = fields.Date(related='employee_id.leave_date_to')
    # current_leave_state = fields.Selection(related='employee_id.current_leave_state')



# class HrExpenseApproved(models.Model):
#     _inherit = "hr.expense.sheet"

#     chuky_dexuat = fields.Binary(string="Chữ ký người lập")
#     chuky_leader = fields.Binary(string="Chữ ký trưởng bộ phận")
#     chuky_nhansu = fields.Binary(string="Chữ ký nhân sự")
#     chuky_ketoan = fields.Binary(string="Chữ ký kế toán")
#     chuky_duyet = fields.Binary(string="Chữ ký duyệt")