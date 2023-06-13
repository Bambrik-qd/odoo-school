from odoo import models, fields

class Patient(models.Model):
    _name = 'hr.hosp.patient'
    _description = 'Patient'

    name = fields.Char()
    doctor_id = fields.Many2one(
        comodel_name='hr.hosp.doctor',
        string='Observing doctor',
        required=True,
    )
