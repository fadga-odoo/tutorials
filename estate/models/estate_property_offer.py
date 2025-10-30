from odoo import models, fields,api
from odoo.exceptions import UserError
from datetime import timedelta

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Real Estate Property Offer"
    _check_price = models.Constraint(
        'CHECK(price >= 0)',
        'Price must be greater than 0.',
    )
    
    price = fields.Float("Price")
    status = fields.Selection(selection=[
        ("accepted", "Accepted"),
        ("refused", "Refused")],
        copy=False)
    validity = fields.Integer("Validity (days)", default=7)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    date_deadline = fields.Date("Deadline", compute="_compute_date_deadline", inverse="_inverse_date_deadline")

    @api.depends("create_date", "validity")
    def _compute_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            record.date_deadline = (create_date + timedelta(days=record.validity)).date()
    
    def _inverse_date_deadline(self):
        for record in self:
            create_date = record.create_date or fields.Datetime.now()
            if record.date_deadline:
                delta = record.date_deadline - create_date.date()
                record.validity = delta.days
    
    def accept_offer(self):
        for record in self:
            # Check if an offer has been accepted for this property
            if record.property_id.offer_ids.filtered(lambda offer: offer.status == "accepted"):
                raise UserError("An offer has already been accepted for this property")
            
            # Updating property attributes
            record.property_id.selling_price = record.price
            record.property_id.buyer = record.partner_id
            record.property_id.state = "offer_accepted"
            record.status = "accepted"

            # Refuse other offers
            other_offers = record.property_id.offer_ids - record
            other_offers.write({"status": "refused"})
        return True
    
    def refuse_offer(self):
        for record in self:
            if record.status == "accepted":
                raise UserError("An accepted offer cannot be refused.")
            # Reset property state to "New" (and probably should be "Offer Received") if all offers are refused.
            if all(offer.status == "refused" for offer in record.property_id.offer_ids):
                record.property_id.state = "new"
            record.status = "refused"
        return True