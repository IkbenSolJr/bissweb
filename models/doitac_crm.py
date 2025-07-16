from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError, ValidationError
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP


class CrmLead(models.Model):
    _inherit = 'crm.lead'
       
    doitac_id = fields.Many2one('doitac.crm', string="Đối tác")



# class dsscustomers(models.Model):
#     _inherit = 'dsscustomers.dsscustomers'

#     doitackh_id = fields.Many2one('doitac.crm', string="Đối tác")


class DoitacCrm(models.Model):
    _name = 'doitac.crm'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'tendoitac'

    doitac_ids =  fields.One2many('crm.lead','doitac_id',string="Khách hàng")    
    # khkyhd_ids =  fields.One2many('dsscustomers.dsscustomers','doitackh_id',string="Khách hàng ký hợp đồng")  

    tendoitac = fields.Char(string="Tên đối tác")
    madoitac = fields.Char(string="Mã/Nhóm đối tác")
    diachidoitac = fields.Char(string="Địa chỉ")
    dienthoai = fields.Char(string="Điện thoại")
    emaildoitac = fields.Char(string="Email")
    lienhe = fields.Char(string="Người liên hệ")
    thanhpho = fields.Char(string="Tỉnh/TP")
    phutrach_id = fields.Many2one('res.users', 'Phụ trách', default=lambda self: self.env.user,index=True, tracking=True)
    nguoigioithieu = fields.Char(string="Người giới thiệu")
    trangthai =  fields.Selection([
                ('dakyket', 'Đã ký kết'),
                ('rattiemnang', 'Rất tiềm năng (đã gửi KH thành công)'),
                ('dangkyket', 'Đang ký kết'),
                ('tichcuc', 'Tích cực tương tác'),
                ('tiemnang', 'Tiềm năng'),
                ('khongtuongtac', 'Không tương tác')
                ], string="Trạng thái")
    zalo = fields.Char(string="Zalo")
    facebook = fields.Char(string="Facecbook")
    note = fields.Text(string="Ghi chú")
    total_count_lead = fields.Integer(string="Tổng số", readonly=True, compute='_compute_total_count_lead')   
    team_id = fields.Many2one('crm.team', string='Sales Team', default=lambda self: self.env.user.team_id, store=True)
    # phongban = fields.Many2one('hr.department', string="Team", default=lambda self: self.env.user.department_id)

    

    
    def _compute_total_count_lead(self):
        for rec in self:
            total_count_lead = self.env['crm.lead'].search_count([('doitac_id', '=', rec.id)])
            rec.total_count_lead = total_count_lead
       

    def action_send_email(self):
        self.ensure_one()  # Ensure that the button is triggered for a single record
        template_id = self.env.ref('bissweb.email_template_dss').id  # Replace with your email template XML ID
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        ctx = {
            'default_model': self._name,
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,  # Add context variables if needed
        }
        return {
            'name': 'Soạn Email',
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
    

    def action_send_email_tree(self):
        
        template_id = self.env.ref('bissweb.email_template_dss').id  # Replace with your email template XML ID
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id
        record_ids = self.env.context.get('active_ids', [])
        if not record_ids:
            raise Warning('No records selected.')

        ctx = {
            'default_model': self._name,
            'default_res_id': record_ids[0] if record_ids else False,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'mass_mail',         
            'default_multi_mode': True,  # Enable multi mode for sending emails to multiple records
            'active_ids': record_ids,  # Pass the selected records

        }
        return {
            'name': 'Soạn Email',
            'type': 'ir.actions.act_window',
            'res_model': 'mail.compose.message',
            'view_mode': 'form',
            'view_id': compose_form_id,
            'target': 'new',
            'context': ctx,
        }
    