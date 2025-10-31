from odoo import models, fields, api

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def mark_as_sold(self):
        return super().mark_as_sold()