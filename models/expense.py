# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import api, fields, models


class HrExpenseSheetdss(models.Model):
    _inherit = "hr.expense.sheet"

    chuky_dexuat = fields.Binary(string="Chữ ký người lập")
    chuky_leader = fields.Binary(string="Chữ ký trưởng bộ phận")
    chuky_nhansu = fields.Binary(string="Chữ ký nhân sự")
    chuky_ketoan = fields.Binary(string="Chữ ký kế toán")
    chuky_duyet = fields.Binary(string="Chữ ký duyệt")


