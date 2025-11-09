from odoo import models, fields

class ResUsers(models.Model):
    _inherit = "res.users"

    teams_as_leader = fields.Many2many(
        comodel_name="crm.team",
        string="All current teams as leader",
        compute="_compute_teams_as_leader",
        store=False,
        readonly=True
    )

    teams_as_member = fields.Many2many(
        comodel_name="crm.team",
        string="All current teams as member",
        compute="_compute_teams_as_member",
        store=False,
        readonly=True
    )

    def _compute_teams_as_member(self):
        for record in self:
            record.teams_as_member = record.crm_team_member_ids.mapped('crm_team_id')
    
    def _compute_teams_as_leader(self):
        for record in self:
            record.teams_as_leader = self.env['crm.team'].search([('user_id', '=', record.id)]) 