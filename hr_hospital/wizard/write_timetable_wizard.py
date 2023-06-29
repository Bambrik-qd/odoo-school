from datetime import datetime, timedelta
from odoo import models, fields

class WriteTimetableWizard(models.TransientModel):
    _name = 'hr.hosp.write.timetable'
    _description = 'Write timetable'

    doctor_ids = fields.Many2many(
        comodel_name='hr.hosp.doctor',
        string='Doctors',
        required=True,
    )
    begin_date = fields.Date()
    end_date = fields.Date()

    begin_time = fields.Float(string = 'Hours begin')
    end_time = fields.Float(string = 'Hours end')

    def action_write_timetable(self):
        time_visit = timedelta(minutes = 10)
        # begin_t = fields.datetime.now()
        # end_t = fields.datetime.now()
        for rec in self:
            begin = datetime(rec.begin_date.year, rec.begin_date.month, rec.begin_date.day, 0, 0, 0)
            end = datetime(rec.end_date.year, rec.end_date.month, rec.end_date.day, 0, 0, 0)

            res = self.env['hr.hosp.timetable'].search([
                        ('doctor_id', 'in', rec.env.context['active_ids']),
                        ('visit_date_time', '>=', begin),
                        ('visit_date_time', '<=', end + timedelta(hours = rec.end_time)),
                    ])
            res.unlink()
            for doc in rec.env.context['active_ids']:
                while begin <= end:
                    begin_t = begin + timedelta(hours = rec.begin_time)
                    end_t = begin + timedelta(hours = rec.end_time)
                    while begin_t <= end_t:
                        res = self.env['hr.hosp.timetable'].create([{
                            'doctor_id': doc,
                            'visit_date_time': begin_t,
                            'is_free': True,
                        }])

                        begin_t += time_visit
                    begin += timedelta(days = 1)
