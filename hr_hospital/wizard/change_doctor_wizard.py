from odoo import models, fields

class ChangeDoctorWizard(models.TransientModel):
    _name = 'hr.hosp.change.doctor'
    _description = 'Change doctor group'

    # old_doctor_ids = fields.Many2one(
    #     comodel_name='hr.hosp.doctor',
    #     string='Doctors (old)',
    #     required=True,
    # )
    new_doctor_id = fields.Many2one(
        comodel_name='hr.hosp.doctor',
        string='Doctor (new)',
        required=True,
    )

    def action_change_doctor(self):
        for rec in self:
            for pat in self.env.context['active_ids']:
                patient = self.env['hr.hosp.patient'].browse(pat)
                patient.doctor_id = rec.new_doctor_id.id
