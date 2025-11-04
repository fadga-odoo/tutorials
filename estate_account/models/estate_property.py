from odoo import models, fields, api

class EstateProperty(models.Model):
    _inherit = "estate.property"

    def mark_as_sold(self):
        entries = []
        for record in self:
            # To create an invoice, we only need 3 information at least:
            # 1. Customer/Buyer: account_move.partner_id
            # 2. Move type: account_move.move_type
            # 3. Journal type: ?

            entries.append({
                "partner_id": record.buyer.id,
                "move_type": "out_invoice",
                "invoice_line_ids": [
                    (0, 0, {
                        'name': 'Commission (6% of selling price)',
                        'quantity': 1,
                        'price_unit': record.selling_price * 0.06,
                    }),
                    (0, 0, {
                        'name': 'Administrative Fees',
                        'quantity': 1,
                        'price_unit': 100.00,
                    }),
                ],
            })

        # Creating one invoice with two items/lines in it:
        self.env["account.move"].create(entries)
        return super().mark_as_sold()