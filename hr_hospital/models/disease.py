from odoo import models, fields

class Disease(models.Model):
    _name = 'hr.hosp.disease'
    _description = 'Types of diseases'

    name = fields.Char()
