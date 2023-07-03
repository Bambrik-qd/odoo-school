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
    history_ids = fields.One2many(
        comodel_name = 'hr.hosp.history.changes.doctor', 
        inverse_name='patient_id',
        string = 'History changes doctor')
    diseases_ids = fields.One2many(
        comodel_name = 'hr.hosp.disease.history',
        string = 'History diseasis',
        # relation = 'patient_deseases_line_rel',
        inverse_name = 'patient_id',  
        auto_join=True,
    )    

    description = fields.Text()

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
       
    def action_visit(self):
        self.ensure_one()
        return {
            'name': _('Visits'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hr.hosp.visit',
            'target': 'new',
            'context': {
                'default_patient_id': self.id,
                'default_doctor_id': self.doctor_id.id,
            },
        }
        
    def action_visits(self):
        # ids = [rec.id for rec in self]
        self.ensure_one()
        return {
            'name': _('Visits'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'hr.hosp.visit',
            'target': 'new',
            'domain': [('patient_id', '=', self.id)],
            # 'context': {
            #     'search_default_patient_id': self.id,
            # },
        }
        
    def action_appointments(self):
        # ids = [rec.id for rec in self]
        self.ensure_one()
        return {
            'name': _('Appointments'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'hr.hosp.diagnosis',
            'target': 'current',
            'domain': [('patient_id', '=', self.id)],
            # 'context': {
            #     'search_default_patient_id': self.id,
            # },
        }
     
    def action_analyzes(self):
        # ids = [rec.id for rec in self]
        self.ensure_one()
        return {
            'name': _('Analyzes'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'hr.hosp.analysis.history',
            'target': 'current',
            'domain': [('patient_id', '=', self.id),
                       ('doctor_id', '=', self.doctor_id.id),
                       ],
            # 'context': {
            #     'search_default_patient_id': self.id,
            # },
        }
       
class DiseaseHistory(models.Model):
    _name = 'hr.hosp.disease.history'
    _description = 'History diseasis'
    # _rec_name = 'disease_id'
    
    disease_id = fields.Many2one(comodel_name = 'hr.hosp.disease')
    patient_id = fields.Many2one(comodel_name = 'hr.hosp.patient')    
    disease_date = fields.Date()   
    name = fields.Char(readonly=True, compute = '_compute_name')
    
    def _compute_name(self):
        for rec in self:
            rec.name = f'{rec.disease_date}: {rec.disease_id.name}'
