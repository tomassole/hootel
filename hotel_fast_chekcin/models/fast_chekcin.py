# Copyright 2020 Jose Luis Algara (Alda hotels) <osotranquilo@gmail.com>
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl).

import json
from datetime import datetime
from odoo import api, models, fields
# from odoo.tools import (
#     DEFAULT_SERVER_DATE_FORMAT,
#     DEFAULT_SERVER_DATETIME_FORMAT)
import logging
_logger = logging.getLogger(__name__)

DEFAULT_FASTCHECKIN_DATE_FORMAT = "%Y-%m-%d"
DEFAULT_FASTCHECKIN_TIME_FORMAT = "%H:%M:%S"
DEFAULT_FASTCHECKIN_DATETIME_FORMAT = "%s %s" % (
    DEFAULT_FASTCHECKIN_DATE_FORMAT,
    DEFAULT_FASTCHECKIN_TIME_FORMAT)


class FastCheckin(models.Model):
    _name = 'fastcheckin.api'

    @api.model
    def fc_get_date(self):
        # FastCheckin API Gets the current business date/time. (MANDATORY)
        tz_hotel = self.env['ir.default'].sudo().get(
            'res.config.settings', 'tz_hotel')
        self_tz = self.with_context(tz=tz_hotel)
        mynow = fields.Datetime.context_timestamp(self_tz, datetime.now()).\
            strftime(DEFAULT_FASTCHECKIN_DATETIME_FORMAT)
        json_response = {
            'serverTime': mynow
            }
        json_response = json.dumps(json_response)
        return json_response

    @api.model
    def fc_get_reservation(self, reservation_code):
        # FastCheckin Gets a reservation ready for check-in
        # through the provided code. (MANDATORY)
        apidata = self.env['hotel.reservation']
        reservation_code = str(reservation_code) if not isinstance(
            reservation_code, str) else reservation_code
        return apidata.sudo().fc_get_reservation(reservation_code)

    @api.model
    def fc_set_partner(self, partner):
        # FastCheckin Sets a partner and assing a check-in

        apidata = self.env['res.partner']
        return apidata.sudo().fc_set_partner(partner)
