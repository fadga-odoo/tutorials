from odoo import models, fields

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Real Estate Property Type"
    _check_unique_name = models.Constraint(
        'UNIQUE(name)',
        'Property type name must be unique.',
    )
    _order = "name asc"

    name = fields.Char("Name", required=True)
    sequence = fields.Char("Sequence", default=1, help="Used to order stages, lower is better.")
    property_ids = fields.One2many("estate.property", "type_id", string="Properties")