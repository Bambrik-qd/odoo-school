from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Visit(models.Model):
    _name = 'hr.hosp.visit'
    _description = 'Patient visits'

    name = fields.Char()

    # visit_date_time = fields.Datetime(
    #     string='Date',
    #     default=fields.Date.today,
    #     help='Date of the patient`s visit',
    #     states = {'draft': [('readonly', False), ('required', False)],
    #               'done': [('readonly', True), ('required', True)]},
    # )

    patient_id = fields.Many2one(
        comodel_name='hr.hosp.patient',
        string='Patient',
        states = {'draft': [('required', False)],
                  'done': [('required', True)]},
    )

    doctor_id = fields.Many2one(
        comodel_name='hr.hosp.doctor',
        string='Doctor',
        states = {'draft': [('readonly', False), ('required', False)],
                  'done': [('readonly', True), ('required', True)]},
    )

    visit_date_id = fields.Many2one(
        comodel_name = 'hr.hosp.timetable',
        domain = "[('doctor_id', '=', doctor_id), ('patient_id', '=', patient_id), ]",
        states = {'draft': [('required', False)],
                  'done': [('required', True)]},
    )

    # disease_ids = fields.Many2many(
    #     comodel_name='hr.hosp.disease',
    #     string='Diseases',
    # )

    diagnosis_id = fields.Many2one(
        comodel_name = 'hr.hosp.diagnosis',
        copy = False,
        states = {'draft': [('required', False)],
                  'done': [('required', True)]},
        )

    state = fields.Selection(
        required = True,
        default = 'draft',
        selection = [
            ('draft', 'Draft'),
            ('need_confirm', 'Need to confirmation'),
            ('done', 'Done'),
        ]
    )

    comment = fields.Text(
        help = 'Commentary from the Doctor-mentor'
    )

    def name_get(self):
        return [(visit.id, "%s" % Visit.patient_id.name) for visit in self]

    def unlink(self):
        for visit in self:
            if visit.diagnosis_id and visit.state == 'done':
                raise ValidationError(_('Error ! You cannot delete a visit with diagnosis.'))
        return super().unlink()

    def _check_record_time(self, vals):
        # self.ensure_one()
        res = self.search([
            ('doctor_id', '=', vals.get('doctor_id')),
            ('visit_date_id', '=', vals.get('visit_date_id')),
            ('id', '!=', vals.get('id')),
        ])
        if len(res) > 0:
            raise ValidationError(_('Error ! This time is busy, use another.'))

    def write(self, vals):
        if self and 'active' in vals and not vals['active']:
            for vis in self:
                if vis.diagnosis_id:
                    raise ValidationError(_('Error ! You cannot archive a visit with diagnosis.'))
        for vis in self:
            if vis.diagnosis_id and vis.doctor_id.is_intern and not vis.comment:
                vals['state'] = 'need_confirm'
            vis._check_record_time(vals)

        return super().write(vals)

    @api.model
    def create(self, vals_list):
        if self.diagnosis_id and self.doctor_id.is_intern:
            vals_list['state'] = 'need_confirm'
        if vals_list['state'] != 'draft':
            self._check_record_time(vals_list)
        return super(Visit, self).create(vals_list)

    @api.onchange('diagnosis_id', 'doctor_id', 'comment')
    def _onchange_diagnosis_id(self):
        if self.diagnosis_id and self.doctor_id.is_intern and not self.comment:
            self.state = 'need_confirm'

    @api.constrains('comment')
    def _constrains_comment(self):
        for vis in self:
            if vis.state == 'need_confirm' and vis.comment:
                # raise ValidationError(_('Error ! Only a mentor can add a comment.'))
                vis.state = 'done'
                                      