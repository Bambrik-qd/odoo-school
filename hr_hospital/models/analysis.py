from odoo import models, fields, api

class Analysis(models.Model):
    _name = 'hr.hosp.analysis'
    _description = 'Analyzes (prices, description)'
    
    name = fields.Char()
    price = fields.Float()
    description = fields.Text()

    
class AnalysisHistory(models.Model):
    _name = 'hr.hosp.analysis.history'
    _description = 'Patient analyzes'   
    
    patient_id = fields.Many2one(
        comodel_name = 'hr.hosp.patient'
    )
    
    doctor_id = fields.Many2one(
        comodel_name = 'hr.hosp.doctor',        
    )
    
    analysis_id = fields.Many2one(
        comodel_name = 'hr.hosp.analysis'
    )
    
    date = fields.Date()
    
    amount = fields.Float()