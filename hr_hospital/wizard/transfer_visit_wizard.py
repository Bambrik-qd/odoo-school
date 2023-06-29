from odoo import models, fields, _

class TransferVisitWizard(models.TransientModel):
    _name = 'hr.hosp.transfer.visit'
    _description = 'Transfer visit'

    doctor_id = fields.Many2one(
        comodel_name='hr.hosp.doctor',
        string='Doctor',
        required=True,
    )

    patient_id = fields.Many2one(
        comodel_name = 'hr.hosp.patient'
    )

    timetable_id = fields.Many2one(
        comodel_name = 'hr.hosp.timetable',
        domain = "[('doctor_id', '=', doctor_id),('patient_id', '=', patient_id),]"
    )

    new_timetable_id = fields.Many2one(
        comodel_name = 'hr.hosp.timetable',
        domain = "[('doctor_id', '=', doctor_id),('is_free', '=', True),]"
    )

    def action_open_wizard(self):
        ids = [rec.id for rec in self]
        return {
            'name': _('Transfer visit'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.hosp.transfer.visit',
            'target': 'new',
            'context': {
                'default_ids': ids,
            },
        }

    def action_change_time(self):
        self.ensure_one()
        visits = self.env['hr.hosp.visit'].search([
                    ('visit_date_id', '=', self.timetable_id.id),
                    ('doctor_id', '=', self.doctor_id.id),
                    ('patient_id', '=', self.patient_id.id),
                    ])

        old_time = self.env['hr.hosp.timetable'].browse(self.timetable_id.id)
        new_time = self.env['hr.hosp.timetable'].browse(self.new_timetable_id.id)

        new_time.patient_id = self.patient_id.id
        old_time.patient_id = False

        new_time.is_free = False
        old_time.is_free = True
        for visit in visits:
            visit.visit_date_id = new_time
            