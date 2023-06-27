from odoo import models, fields, api

class Person(models.AbstractModel):
    _name = 'hr.hosp.person'
    _description = 'Person'

    name = fields.Char(compute = '_compute_name')
    last_name = fields.Char()
    first_name = fields.Char()
    phone = fields.Char(
                        # compute='_compute_mobile',
                        readonly=False,
                        store=True)    # Mobile
    email = fields.Char()
    gender = fields.Selection(selection = [
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')])
    photo = fields.Image()

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for person in self:
            person.name = f"{person.last_name} {person.first_name}"
    