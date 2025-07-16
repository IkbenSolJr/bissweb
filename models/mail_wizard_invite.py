from lxml import etree
from lxml.html import builder as html

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class Invite(models.TransientModel):
    _inherit = 'mail.wizard.invite'

     # Override the default value of the field 'send_mail' to False
    send_mail = fields.Boolean('Send Email', default=False)

# Disable the user_assigned Email
class CrmLead(models.Model):
    _inherit = 'crm.lead'

    @api.model
    def message_post(self, **kwargs):
        # If user assignment is being made, suppress the email notification
        if 'user_id' in kwargs and kwargs['user_id']:
            kwargs['notify_users'] = False  # Prevent email notification
        return super(CrmLead, self).message_post(**kwargs)
        
    # @api.model
    # def create(self, values):
    #     # Create the lead record
    #     lead = super(CrmLead, self).create(values)
    #     lead_name = lead.name

    #     # If user_id is assigned, post a message to the channel
    #     if lead.user_id:
    #         message = f"Lead {lead_name} has been assigned to {lead.user_id.name}."

    #         # Find the channel where you want to post the message
    #         channel = self.env['mail.channel'].search([('name', '=', 'Lead Assignments')], limit=1)
    #         if not channel:
    #             # If no channel found, you can raise an error or create one
    #             raise UserError("The 'Lead Assignments' channel does not exist. Please create the channel first.")

    #         # Post the message to the channel
    #         channel.message_post(
    #             body=message,
    #             message_type='comment',  # This is a comment message type
    #             author_id=lead.user_id.id,  # Set the author as the assigned user
    #         )

    #         # Add the assigned user as a follower of the lead (optional)
    #         lead.message_subscribe([lead.user_id.id])

    #     return lead

    # def write(self, values):
    #     for lead in self:
    #         lead_name = lead.name
    #     # Check if user_id is being updated
    #     if 'user_id' in values:
    #         # Get the old and new user_id
    #         old_user_id = self.user_id
    #         new_user_id = self.env['res.users'].browse(values['user_id'])

    #         if old_user_id != new_user_id:  # Only post if user_id is really changed
    #             message = f"Lead {lead_name} has been reassigned from {old_user_id.name} to {new_user_id.name}."
    #             for lead in self:
    #                 # Find the channel where you want to post the reassignment message
    #                 channel = self.env['mail.channel'].search([('name', '=', 'Lead Assignments')], limit=1)
    #                 if not channel:
    #                     raise UserError("The 'Lead Assignments' channel does not exist. Please create the channel first.")

    #                 # Post the reassignment message to the channel
    #                 channel.message_post(
    #                     body=message,
    #                     message_type='comment',  # This is a comment message type
    #                     author_id=new_user_id.id,  # Set the author as the reassigned user
    #                 )

    #                 # Add the new user as a follower if they are not already a follower
    #                 lead.message_subscribe([new_user_id.id])

    #     # Proceed with the normal write method
    #     return super(CrmLead, self).write(values)