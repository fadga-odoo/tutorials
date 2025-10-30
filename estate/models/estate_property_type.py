from odoo import models, fields, api

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
    offer_ids = fields.One2many("estate.property.offer", "property_type_id", string="Offers")
    offer_count = fields.Integer(compute="_compute_offer_count")

    @api.depends("offer_ids")
    def _compute_offer_count(self):
        for record in self:
            record.offer_count = len(record.offer_ids)