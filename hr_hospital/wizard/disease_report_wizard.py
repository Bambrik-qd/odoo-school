from datetime import date
from odoo import models, fields, _



class DiseaseReportWizard(models.TransientModel):
    _name = 'hr.hosp.disease.report'
    _description = 'Disease report for the period'

    begin_date = fields.Date()
    end_date = fields.Date()

    # disease_id = fields.Many2one(
    #     comodel_name = 'hr.hosp.disease',
    # )
    # count_diagnosis = fields.Integer()

    def action_generate_report(self):

        records = self.env['hr.hosp.count.diagnosis'].search([])
        records.unlink()

        for rec in self:

            domain = [
                    ('diagnosis_date', '>=', rec.begin_date),
                    ('diagnosis_date', '<=', rec.end_date),
                    ]
            # if len(rec.ids) > 0:
            #     domain.append(('doctor_id' , 'in', rec.ids))
            # diseases = self.env['hr.hosp.disease'].search([])
            if 'active_ids' in rec.env.context:
                domain.append(('doctor_id' , 'in', rec.env.context['active_ids']))
            diagnoses = self.env['hr.hosp.diagnosis'].search(domain)
            diseases = diagnoses.mapped('disease_id')
            for dis in diseases:
                year =   rec.begin_date.year
                month = rec.begin_date.month
                while year <= rec.end_date.year:
                    while month <= rec.end_date.month:
                        self.env['hr.hosp.count.diagnosis'].create(
                            {
                                'mounth_data': date(year, month, 1),
                                'disease_id': dis.id,
                                'count_diagnosis': diagnoses.search_count([
                                    ('disease_id', '=', dis.id),
                                    ('diagnosis_date', '>=', date(year, month, 1)),
                                    ('diagnosis_date', '<', date(year, month+1, 1)),
                                ]),
                            }
                        )
                        month += 1
                    year += 1
        return {
            'name': _('Number of diagnoses for disease for the period'),
            'type': 'ir.actions.act_window',
            'view_mode': 'tree',
            'res_model': 'hr.hosp.count.diagnosis',
            'target': 'new',
            'context': {
                # 'default_ids': ids,
            },
        }


class CountDiagnosis(models.TransientModel):
    _name = 'hr.hosp.count.diagnosis'
    _description = 'Number of diagnoses for disease for the period'

    mounth_data = fields.Date(
        string = 'Mounth/Year'
    )
    disease_id = fields.Many2one(
        comodel_name = 'hr.hosp.disease',
    )
    count_diagnosis = fields.Integer()
