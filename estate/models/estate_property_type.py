from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property type name must be unique.',
    )

    name = fields.Char("Name", required=True)