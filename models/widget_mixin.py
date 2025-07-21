from odoo import models, fields, api
import logging

_logger = logging.getLogger(__name__)

class WidgetMixin(models.AbstractModel):
    """
    Mixin an toàn để thêm widget functionality
    Tự động detect các module có sẵn và chỉ load những gì cần thiết
    """
    _name = 'widget.mixin'
    _description = 'Safe Widget Mixin'

    # Safe computed fields - chỉ tính toán nếu model tồn tại
    total_count_book = fields.Integer(
        string="Booking", 
        readonly=True, 
        compute='_compute_count_booking',
        store=False  # Không store để tránh lỗi database
    )
    
    review_count = fields.Integer(
        string="Review", 
        readonly=True, 
        compute='_compute_review_count',
        store=False
    )

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

    def _get_related_leads(self):
        """Lấy danh sách leads liên quan - override trong model con"""
        if hasattr(self, 'doitac_ids'):
            # Cho doitac.crm
            return self.doitac_ids
        elif self._name == 'crm.lead':
            # Cho crm.lead
            return self
        else:
            return self.env['crm.lead'].browse()

    @api.depends()  # Không depends vào field cụ thể để tránh lỗi
    def _compute_count_booking(self):
        for rec in self:
            try:
                leads = rec._get_related_leads()
                total_booking = 0
                
                if rec._is_model_available('salereport.booking'):
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
                leads = rec._get_related_leads()
                total_review = 0
                
                if rec._is_model_available('salereport.review'):
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

    def action_view_sale_booking(self):
        """Action an toàn để xem booking"""
        try:
            if not self._is_model_available('salereport.booking'):
                return {
                    'type': 'ir.actions.act_window_close',
                    'infos': {'message': 'Module Salereport chưa được cài đặt'}
                }

            leads = self._get_related_leads()
            booking_ids = []
            
            for lead in leads:
                bookings = self.env['salereport.booking'].search([
                    ('leadbooking_ids', '=', lead.id)
                ])
                booking_ids.extend(bookings.ids)
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Booking',
                'res_model': 'salereport.booking',
                'domain': [('id', 'in', booking_ids)],
                'view_mode': 'tree,form',
                'target': 'current',
            }
        except Exception as e:
            _logger.error(f"Error in action_view_sale_booking: {e}")
            return {'type': 'ir.actions.act_window_close'}

    def action_view_lead_review(self):
        """Action an toàn để xem review"""
        try:
            if not self._is_model_available('salereport.review'):
                return {
                    'type': 'ir.actions.act_window_close',
                    'infos': {'message': 'Module Salereport chưa được cài đặt'}
                }

            leads = self._get_related_leads()
            review_ids = []
            
            for lead in leads:
                reviews = self.env['salereport.review'].search([
                    ('lead_ids', '=', lead.id)
                ])
                review_ids.extend(reviews.ids)
            
            return {
                'type': 'ir.actions.act_window',
                'name': 'Review',
                'res_model': 'salereport.review',
                'domain': [('id', 'in', review_ids)],
                'view_mode': 'tree,form',
                'target': 'current',
            }
        except Exception as e:
            _logger.error(f"Error in action_view_lead_review: {e}")
            return {'type': 'ir.actions.act_window_close'}