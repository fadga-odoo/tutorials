from odoo import fields, models, api

class SaleOrder(models.Model):
    _inherit = ["sale.order"]

    branch_id = fields.Many2one("sale.branch")

    @api.model
    def create(self, vals_list):
        for value in vals_list:
            branch = self.env["sale.branch"].browse(value["branch_id"])
            value["name"] = branch.sequence_id.name
        return super().create(vals_list)