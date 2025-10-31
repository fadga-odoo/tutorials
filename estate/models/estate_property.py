from odoo import models, fields, api
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Real Estate Property"
    _check_expected_price = models.Constraint(
        'CHECK(expected_price >= 0)',
        'Expected price must be greater than 0.',
    )
    _check_selling_price = models.Constraint(
        'CHECK(selling_price >= 0)',
        'Selling price must be greater than 0.',
    )
    _order = "id desc"

    name = fields.Char("Title", required=True)
    description = fields.Text()
    postcode = fields.Char("Postcode")
    next_three_months = fields.Date.today() + relativedelta(months=3)
    date_availability = fields.Date("Available From", copy=False, default=next_three_months)
    expected_price = fields.Float("Expected Price", required=True)
    selling_price = fields.Float("Selling Price", readonly=True, copy=False)
    bedrooms = fields.Integer("Bedrooms", default=2)
    living_area = fields.Integer("Living Area (sqm)")
    facades = fields.Integer("Facades")
    garage = fields.Boolean("Garage")
    garden = fields.Boolean("Garden")
    garden_area = fields.Integer("Garden Area (sqm)")
    garden_orientation = fields.Selection(selection=[("north", "North"), ("south", "South"), ("east", "East"), ("west", "West")], string="Garden Orientation")
    type_id = fields.Many2one("estate.property.type", string="Property Type")
    buyer = fields.Many2one("res.partner", string="Buyer", copy="False")
    salesperson = fields.Many2one("res.partner", string="Salesperson", default=lambda self: self.env.user)
    tag_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer", "property_id", string="Offers")
    active = fields.Boolean(default=True)
    state = fields.Selection(string="Status", selection=[
        ("new", "New"),
        ("offer_received", "Offer Received"),
        ("offer_accepted", "Offer Accepted"),
        ("sold", "Sold"),
        ("cancelled", "Cancelled")],
        required=True, copy=False, default="new")
    total_area = fields.Integer(compute="_compute_total_area")
    best_price = fields.Float("Best Offer", compute="_compute_best_price")

    @api.depends("living_area", "garden_area")
    def _compute_total_area(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best_price(self):
        for record in self:
            if record.offer_ids:
                record.best_price = max(record.offer_ids.mapped("price"))
            else:
                record.best_price = 0.0
    
    @api.onchange("garden")
    def _onchange_garden(self):
        if self.garden:
            self.garden_area = 10
            self.garden_orientation = "north"
        else:
            self.garden_area = None
            self.garden_orientation = None

    def mark_as_sold(self):
        for record in self:
            if record.state == "cancelled":
                raise UserError("Cancelled properties cannot be sold.")
            record.state = "sold"
        return True
    
    def mark_as_cancelled(self):
        for record in self:
            if record.state == "sold":
                raise UserError("Sold properties cannot be cancelled.")
            record.state = "cancelled"
        return True
    
    @api.constrains("expected_price", "selling_price")
    def _check_expected_and_selling_price(self):
        for record in self:
            if float_is_zero(record.selling_price, precision_rounding=0.01):
                continue
            minimum_price = record.expected_price * 0.9
            if float_compare(record.selling_price, minimum_price, precision_rounding=0.01) == -1:
                raise ValidationError("Selling price cannot be lower than 90% of the expected price.")
    
    @api.ondelete(at_uninstall=False)
    def _unlink_except_offered_property(self):
        for record in self:
            if record.state != "new" or record.state != "cancelled":
                raise UserError("Cannot delete an offered property, only properties in state 'New' or 'Cancelled' can be deleted.")

class Users(models.Model):
    _inherit = "res.users"

    property_ids = fields.One2many("estate.property", "salesperson", string="Property IDs", domain=['|', ('state', '=', 'new'), ('state', '=', 'offer_received')])