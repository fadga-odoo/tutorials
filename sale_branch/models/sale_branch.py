from odoo import models, fields, api

class SaleBranch(models.Model):
    _name = "sale.branch"
    _description = "Cabang Sale"
    
    name = fields.Char()
    sequence_id = fields.Many2one("ir.sequence")
    code = fields.Char()

    @api.model
    def create(self, vals_list):
        for value in vals_list:
            self.env["ir.sequence"].create({
                "name": value["name"],
                "code": value["code"]
            })
        return super().create(vals_list)