# from odoo import models, fields

class ContactPerson(models.Model):
    _name = 'hr.hosp.contact.person'
    _description = 'Contact person'
    _inherit = 'hr.hosp.person'
