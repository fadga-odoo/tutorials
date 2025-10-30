from odoo import models, fields

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Real Estate Property Tag"
    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property tag name must be unique.',
    )

    name = fields.Char("Name", required=True)