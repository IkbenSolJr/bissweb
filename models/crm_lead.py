from odoo import models, fields, api
from datetime import datetime, timedelta

class CrmLead(models.Model):
    _inherit = 'crm.lead'
       
       
    meeting_count = fields.Integer(string="Meeting Count", compute="_compute_meeting_count")

    def _compute_meeting_count(self):   
        for lead in self:
            lead.meeting_count = self.env['calendar.event'].search_count([('lead_id', '=', lead.id)])

    def action_schedule_meeting(self):
        self.ensure_one()
        action = self.env["ir.actions.actions"]._for_xml_id("calendar.action_calendar_event")
        action['context'] = {
            'default_lead_id': self.id,
            'default_name': f"Đặt lịch - {self.name}",
            'default_start': fields.Datetime.now(),
            'default_duration': 1.0,  # default duration in hours
            'user_id': self.user_id.id,  # Responsible user as meeting organizer
            'description': self.description,  # Copy description from lead
            'allday': False,
            'default_partner_id': self.partner_id.id if self.partner_id else False,
        }
        return action


class CalendarEvent(models.Model):
    _inherit = 'calendar.event'

    lead_id = fields.Many2one('crm.lead', string="Lead")  