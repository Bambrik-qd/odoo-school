from odoo import models, fields

class Visit(models.Model):
    _name = 'hr.hosp.visit'
    _description = 'Patient visits'

    name = fields.Char()

    visit_date = fields.Date(
        string='Date',
        default=fields.Date.today,
        help='Date of the patient`s visit'
    )

    patient_id = fields.Many2one(
        comodel_name='hr.hosp.patient',
        string='Patient',
    )
    disease_ids = fields.Many2many(
        comodel_name='hr.hosp.disease',
        string='Diseases',
    )

    doctor_id = fields.Many2one(
        comodel_name='hr.hosp.doctor',
        string='Doctor'
    )
