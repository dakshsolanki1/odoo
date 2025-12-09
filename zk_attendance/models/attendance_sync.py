# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError
import logging

_logger = logging.getLogger(__name__)

try:
    from zk import ZK, const
    ZK_LIB = True
except ImportError:
    ZK_LIB = False
    _logger.warning("zk library not installed. Run: pip install zk")

class ZkAttendanceSync(models.Model):
    _name = 'zk.attendance.sync'
    _description = 'Indentix K90 Pro+ Device'

    name = fields.Char(string="Device Name", default="Indentix K90 Pro+", required=True)
    device_ip = fields.Char(string="IP Address", required=True)
    device_port = fields.Integer(string="Port", default=4370)
    last_sync = fields.Datetime(string="Last Successful Sync", readonly=True)

    def test_connection(self):
        if not ZK_LIB:
            raise UserError(_("Python 'zk' library not installed. Contact admin."))
        try:
            zk = ZK(self.device_ip, port=self.device_port, timeout=10, password=0, force_udp=False, ommit_ping=False)
            conn = zk.connect()
            conn.test_voice()
            conn.disconnect()
            raise UserError(_("Connection Successful! Device is online."))
        except Exception as e:
            raise UserError(_("Connection Failed: %s") % str(e))

    def sync_now(self):
        if not ZK_LIB:
            raise UserError(_("Missing 'zk' library. Install with: pip install zk"))

        try:
            zk = ZK(self.device_ip, port=self.device_port, timeout=30)
            conn = zk.connect()
            att_logs = conn.get_attendance()
            conn.disconnect()

            created = 0
            for log in att_logs:
                employee = self.env['hr.employee'].search([('device_user_id', '=', str(log.user_id))], limit=1)
                if employee:
                    self.env['hr.attendance'].create({
                        'employee_id': employee.id,
                        'check_in' if log.punch == 0 else 'check_out': log.timestamp,
                    })
                    created += 1

            self.last_sync = fields.Datetime.now()
            return {
                'type': 'ir.actions.client',
                'tag': 'display_notification',
                'params': {
                    'title': 'Success',
                    'message': _('%d attendance records imported!') % created,
                    'type': 'success',
                    'sticky': False,
                }
            }
        except Exception as e:
            _logger.exception("ZK Sync failed")
            raise UserError(_("Sync failed: %s") % str(e))
