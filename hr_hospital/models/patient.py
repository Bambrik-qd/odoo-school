from datetime import datetime
from odoo import models, fields, api, _

class Patient(models.Model):
    _name = 'hr.hosp.patient'
    _description = 'Patient'
    _inherit = 'hr.hosp.person'

    # name = fields.Char()
    doctor_id = fields.Many2one(
        comodel_name='hr.hosp.doctor',
        string='Personal doctor', # Observing doctor
        required=True,
    )
    birth_date = fields.Date(string = 'Date of Birth')
    age = fields.Integer(compute = '_compute_age')
    passport_data = fields.Char()
    contact_id = fields.Many2one(comodel_name = 'hr.hosp.contact.person', string = 'Contact person')

    @api.depends('birth_date')
    def _compute_age(self):
        for patient in self:
            if not patient.birth_date:
                patient.age = 0
            else:
                now = datetime.now()
                patient.age = now.year - patient.birth_date.year

    def write(self, vals):
        res = super().write(vals)
        if vals.get('doctor_id'):
            for patient in self:
                self.env['hr.hosp.history.changes.doctor'].create(
                    {
                        'appointment_date_time': datetime.now(),
                        'patient_id': patient.id,
                        'doctor_id': vals.get('doctor_id'),
                    }
                )
        return res

    @api.model
    def create(self, vals_list):
        res = super().create(vals_list)
        self.env['hr.hosp.history.changes.doctor'].create(
            {
                'appointment_date_time': datetime.now(),
                'patient_id': res.id,
                'doctor_id': res.doctor_id.id,
            }
        )
        return res

    def action_change_doctor(self):
        # ids = [rec.id for rec in self]
        return {
            'name': _('Change doctor'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.hosp.change.doctor',
            'target': 'new',
            'context': {
                # 'default_ids': ids,
            },
        }
       