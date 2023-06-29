from odoo import models, fields

class Diagnosis(models.Model):
    _name = 'hr.hosp.diagnosis'
    _description = 'Diagnoses'

    name = fields.Char()
    diagnosis_date = fields.Datetime()
    doctor_id = fields.Many2one(
        comodel_name='hr.hosp.doctor',
        string='Doctor who made diagnosis',
        required=True,
    )
    patient_id = fields.Many2one(
        comodel_name='hr.hosp.patient',
        string='Patient',
    )
    disease_id = fields.Many2one(
        comodel_name='hr.hosp.disease',
        string='Disease',
    )

    description = fields.Char(string = 'Appointment for treatment')
    # visit_id = fields.Many2one(comodel_name = 'hr.hosp.visit')
   