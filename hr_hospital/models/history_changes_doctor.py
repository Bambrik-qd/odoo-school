from odoo import models, fields

class HistoryChangesDoctor(models.Model):
    _name = 'hr.hosp.history.changes.doctor'
    _description = 'History personal doctor changes'
    # _rec_name = 'patient_id'

    appointment_date_time = fields.Datetime()
    patient_id = fields.Many2one(
        comodel_name = 'hr.hosp.patient',
        ondelete = 'cascade',
    )
    doctor_id = fields.Many2one(
        comodel_name = 'hr.hosp.doctor',
        ondelete = 'cascade',
    )

    def name_get(self):
        return [(rec.id, f'Patient: {rec.patient_id.name}, '
                        f'Doctor: {rec.doctor_id.name}')
                for rec in self]
