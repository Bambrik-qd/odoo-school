from odoo import models, fields, api, _

class Disease(models.Model):
    _name = 'hr.hosp.disease'
    _description = 'Types of diseases'
    _parent_name = 'parent_id'
    _parent_store = True

    name = fields.Char(translate = True)
    parent_id = fields.Many2one(
        comodel_name = 'hr.hosp.disease',
        string = 'Parent Category',
        index = True,
        ondelete = 'cascade',
    )
    parent_path = fields.Char(index = True, unaccent=False)

    @api.constrains('parent_id')
    def check_parent_id(self):
        if not self._check_recursion():
            raise ValueError(_('Error ! You cannot create recursive categories.'))

    # def name_get(self):
    #     res = []
    #     for category in self:
    #         res.append((category.id, " / ".join(category.parents_and_self.mapped('name'))))
    #     return res

