# -*- coding: utf-8 -*-
from odoo import fields, models

class HrEmployee(models.Model):
    _inherit = 'hr.employee'

    device_user_id = fields.Char(
        string="Biometric Device ID",
        help="User ID as registered on Indentix K90 Pro+ machine"
    )
