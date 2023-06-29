from datetime import datetime
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class TimeTable(models.Model):
    _name = 'hr.hosp.timetable'
    _description = 'Timetable doctors'
    _rec_name = 'visit_date_time'

    name = fields.Char()

    visit_date_time = fields.Datetime(
        string='Date',
        required=True,
        default=fields.Date.today,
        help='Date of the patient`s visit',
    )

    patient_id = fields.Many2one(
        comodel_name='hr.hosp.patient',
        string='Patient',
        # required=True,
    )

    doctor_id = fields.Many2one(
        comodel_name='hr.hosp.doctor',
        string='Doctor',
        required=True,
    )

    is_free = fields.Boolean()

    @api.onchange('visit_date_time')
    def _onchange_visit_date_time(self):
        minute = self.visit_date_time.minute

        rec_date_time = datetime(
            self.visit_date_time.year,
            self.visit_date_time.month,
            self.visit_date_time.day,
            self.visit_date_time.hour,
            round(minute, -1),
            0)
        self.visit_date_time = rec_date_time

    def _check_record_time(self, vals):
        # self.ensure_one()
        domain = [
            ('doctor_id', '=', vals.get('doctor_id')),
            ('visit_date_time', '=', vals.get('visit_date_time')),
        ]
        if vals.get('id'):
            domain.append(('id', '!=', vals.get('id')))
        res = self.search(domain)
        if len(res) > 0:
            raise ValidationError(_('Error ! This time is busy, use another.'))


    @api.model
    def create(self, vals_list):
        self._check_record_time(vals_list)
        if vals_list.get('patient_id'):
            vals_list['is_free'] = (vals_list.get('patient_id') is False)
        return super().create(vals_list)

    def write(self, vals):
        for tt in self:
            tt._check_record_time(vals)
        if vals.get('patient_id'):
            vals['is_free'] = (vals.get('patient_id') is False)
        return super().write(vals)
