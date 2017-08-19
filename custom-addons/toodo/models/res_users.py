# -*- coding: utf-8 -*-
##############################################################################
# For copyright and license notices, see __openerp__.py file in root directory
##############################################################################

from openerp import api, fields, models, _


class ResUsers(models.Model):
    _inherit = 'res.users'

    @api.model
    def create(self, vals):
        vals['email'] = 'email@dominio.com'
        return super(ResUsers, self).create(vals)
