from odoo import models, fields, api, _
from odoo.exceptions import ValidationError

class Doctor(models.Model):
    _name = 'hr.hosp.doctor'
    _description = 'Doctor'
    _inherit = 'hr.hosp.person'

    name = fields.Char()
    active = fields.Boolean(
        default=True,
    )
    speciality = fields.Char()
    is_intern = fields.Boolean()
    mentor_id = fields.Many2one(
        comodel_name = 'hr.hosp.doctor',
        domain = [('is_intern', '=', False)],
    )

    def _check_is_intern(self, mentor_id):
        self.ensure_one()
        mentor = self.browse(mentor_id)
        if mentor.is_intern:
            raise ValidationError(_('Error ! Mentor cannot be an intern.'))

    @api.model
    def create(self, vals_list):
        if vals_list.get('mentor_id'):
            self._check_is_intern(vals_list.get('mentor_id'))

        return super(Doctor, self).create(vals_list)

    def write(self, vals):
        for doc in self:
            if not vals.get('is_intern', True):
                vals['mentor_id'] = False
            elif vals.get('mentor_id') and doc.id != vals.get('mentor_id'):
                self._check_is_intern(vals.get('mentor_id'))
            elif doc.id == vals.get('mentor_id'):
                raise ValidationError(_('Error ! Mentor cannot be himself.'))

        return super(Doctor, self).write(vals)

    def action_write_timetable(self):
        ids = [rec.id for rec in self]
        return {
            'name': _('Write timetable'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.hosp.write.timetable',
            'target': 'new',
            'context': {
                'default_ids': ids,
            },
        }
