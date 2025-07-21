from odoo import models, fields, api,  _
from datetime import datetime, timedelta
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError, ValidationError
from odoo.addons.base.models.res_partner import WARNING_MESSAGE, WARNING_HELP
import logging

_logger = logging.getLogger(__name__)

class CrmLead(models.Model):
    _inherit = 'crm.lead'
       
    doitac_id = fields.Many2one('doitac.crm', string="Đối tác")


class DoitacCrm(models.Model):
    _name = 'doitac.crm'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _rec_name = 'tendoitac'

    doitac_ids = fields.One2many('crm.lead','doitac_id', string="Khách hàng")    

    tendoitac = fields.Char(string="Tên đối tác")
    madoitac = fields.Char(string="Mã/Nhóm đối tác")
    diachidoitac = fields.Char(string="Địa chỉ")
    dienthoai = fields.Char(string="Điện thoại")
    emaildoitac = fields.Char(string="Email")
    lienhe = fields.Char(string="Người liên hệ")
    thanhpho = fields.Char(string="Tỉnh/TP")
    phutrach_id = fields.Many2one('res.users', 'Phụ trách', default=lambda self: self.env.user, index=True, tracking=True)
    nguoigioithieu = fields.Char(string="Người giới thiệu")
    trangthai = fields.Selection([
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

    # Safe widget fields - không store để tránh lỗi database
    total_count_book = fields.Integer(
        string="Booking", 
        readonly=True, 
        compute='_compute_count_booking',
        store=False
    )
    
    review_count = fields.Integer(
        string="Review", 
        readonly=True, 
        compute='_compute_review_count',
        store=False
    )

    form_count = fields.Integer(
        string="Count Form", 
        compute='_compute_form_lead_count', 
        store=False
    )

    # Utility methods
    def _is_model_available(self, model_name):
        """Kiểm tra xem model có tồn tại trong registry không"""
        try:
            return model_name in self.env.registry
        except Exception:
            return False

    def _safe_search_count(self, model_name, domain):
        """Tìm kiếm an toàn với error handling"""
        try:
            if not self._is_model_available(model_name):
                return 0
            return self.env[model_name].search_count(domain)
        except Exception as e:
            _logger.warning(f"Error searching {model_name}: {e}")
            return 0

    # Compute methods
    def _compute_total_count_lead(self):
        for rec in self:
            total_count_lead = self.env['crm.lead'].search_count([('doitac_id', '=', rec.id)])
            rec.total_count_lead = total_count_lead

    @api.depends()  # Không depends vào field cụ thể để tránh lỗi
    def _compute_count_booking(self):
        for rec in self:
            try:
                total_booking = 0
                
                if rec._is_model_available('salereport.booking'):
                    # Kiểm tra xem có trường doitac_id trong booking không
                    booking_model = self.env['salereport.booking']
                    if 'doitac_id' in booking_model._fields:
                        # Tìm trực tiếp qua doitac_id (hiệu quả hơn)
                        total_booking = rec._safe_search_count(
                            'salereport.booking',
                            [('doitac_id', '=', rec.id)]
                        )
                    else:
                        # Fallback: tìm qua leads (cách cũ)
                        leads = rec.doitac_ids
                        for lead in leads:
                            count = rec._safe_search_count(
                                'salereport.booking',
                                [('leadbooking_ids', '=', lead.id)]
                            )
                            total_booking += count
                
                rec.total_count_book = total_booking
            except Exception as e:
                _logger.warning(f"Error computing booking count: {e}")
                rec.total_count_book = 0

    @api.depends()
    def _compute_review_count(self):
        for rec in self:
            try:
                total_review = 0
                
                if rec._is_model_available('salereport.review'):
                    # Kiểm tra xem có trường doitac_id trong review không
                    review_model = self.env['salereport.review']
                    if 'doitac_id' in review_model._fields:
                        # Tìm trực tiếp qua doitac_id
                        total_review = rec._safe_search_count(
                            'salereport.review',
                            [('doitac_id', '=', rec.id)]
                        )
                    else:
                        # Fallback: tìm qua leads
                        leads = rec.doitac_ids
                        for lead in leads:
                            count = rec._safe_search_count(
                                'salereport.review',
                                [('lead_ids', '=', lead.id)]
                            )
                            total_review += count
                
                rec.review_count = total_review
            except Exception as e:
                _logger.warning(f"Error computing review count: {e}")
                rec.review_count = 0

    @api.depends()
    def _compute_form_lead_count(self):
        for rec in self:
            try:
                if rec._is_model_available('formreview.lead'):
                    leads = rec.doitac_ids
                    total_form = 0
                    for lead in leads:
                        count = rec._safe_search_count(
                            'formreview.lead',
                            [('lead_form_id', '=', lead.id)]
                        )
                        total_form += count
                    rec.form_count = total_form
                else:
                    rec.form_count = 0
            except Exception as e:
                _logger.warning(f"Error computing form count: {e}")
                rec.form_count = 0

    # Action methods
    def action_view_sale_booking(self):
        """Action an toàn để xem booking"""
        try:
            if not self._is_model_available('salereport.booking'):
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Thông báo',
                        'message': 'Module Salereport chưa được cài đặt',
                        'type': 'warning',
                    }
                }

            booking_ids = []
            booking_model = self.env['salereport.booking']
            
            # Kiểm tra xem có trường doitac_id không
            if 'doitac_id' in booking_model._fields:
                # Tìm trực tiếp qua doitac_id
                bookings = booking_model.search([('doitac_id', '=', self.id)])
                booking_ids = bookings.ids
            else:
                # Fallback: tìm qua leads
                leads = self.doitac_ids
                for lead in leads:
                    bookings = booking_model.search([('leadbooking_ids', '=', lead.id)])
                    booking_ids.extend(bookings.ids)
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Booking của đối tác',
                'res_model': 'salereport.booking',
                'domain': [('id', 'in', booking_ids)],
                'view_mode': 'tree,form',
                'target': 'current',
            }
        except Exception as e:
            _logger.error(f"Error in action_view_sale_booking: {e}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Lỗi',
                    'message': 'Có lỗi xảy ra khi mở danh sách booking',
                    'type': 'danger',
                }
            }

    def action_view_lead_review(self):
        """Action an toàn để xem review"""
        try:
            if not self._is_model_available('salereport.review'):
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Thông báo',
                        'message': 'Module Salereport chưa được cài đặt',
                        'type': 'warning',
                    }
                }

            review_ids = []
            review_model = self.env['salereport.review']
            
            # Kiểm tra xem có trường doitac_id không
            if 'doitac_id' in review_model._fields:
                # Tìm trực tiếp qua doitac_id
                reviews = review_model.search([('doitac_id', '=', self.id)])
                review_ids = reviews.ids
            else:
                # Fallback: tìm qua leads
                leads = self.doitac_ids
                for lead in leads:
                    reviews = review_model.search([('lead_ids', '=', lead.id)])
                    review_ids.extend(reviews.ids)
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Review của đối tác',
                'res_model': 'salereport.review',
                'domain': [('id', 'in', review_ids)],
                'view_mode': 'tree,form',
                'target': 'current',
            }
        except Exception as e:
            _logger.error(f"Error in action_view_lead_review: {e}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Lỗi',
                    'message': 'Có lỗi xảy ra khi mở danh sách review',
                    'type': 'danger',
                }
            }

    def action_view_form_lead(self):
        """Action an toàn để xem form"""
        try:
            if not self._is_model_available('formreview.lead'):
                return {
                    'type': 'ir.actions.client',
                    'tag': 'display_notification',
                    'params': {
                        'title': 'Thông báo',
                        'message': 'Model form không khả dụng',
                        'type': 'warning',
                    }
                }

            leads = self.doitac_ids
            form_ids = []
            
            for lead in leads:
                forms = self.env['formreview.lead'].search([
                    ('lead_form_id', '=', lead.id)
                ])
                form_ids.extend(forms.ids)
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Form của đối tác',
                'res_model': 'formreview.lead',
                'domain': [('id', 'in', form_ids)],
                'view_mode': 'tree,form',
                'target': 'current',
            }
        except Exception as e:
            _logger.error(f"Error in action_view_form_lead: {e}")
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Lỗi',
                    'message': 'Có lỗi xảy ra khi mở danh sách form',
                    'type': 'danger',
                }
            }

    def action_send_email(self):
        self.ensure_one()
        template_id = self.env.ref('bissweb.email_template_dss').id
        compose_form_id = self.env.ref('mail.email_compose_message_wizard_form').id

        ctx = {
            'default_model': self._name,
            'default_res_id': self.id,
            'default_use_template': bool(template_id),
            'default_template_id': template_id,
            'default_composition_mode': 'comment',
            'mark_so_as_sent': True,
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

    def debug_recompute(self):
        """Debug method để recompute các field"""
        for rec in self:
            # Force recompute
            rec._compute_count_booking()
            rec._compute_review_count()
            rec._compute_form_lead_count()
            
        return {
            'type': 'ir.actions.client',
            'tag': 'display_notification',
            'params': {
                'title': 'Debug',
                'message': f'Recomputed: Booking={self.total_count_book}, Review={self.review_count}, Form={self.form_count}',
                'type': 'success',
            }
        }
    
    def action_send_email_tree(self):
        template_id = self.env.ref('bissweb.email_template_dss').id
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
            'default_multi_mode': True,
            'active_ids': record_ids,
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