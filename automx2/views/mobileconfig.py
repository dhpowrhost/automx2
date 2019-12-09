"""
App views: Autoconfigure mail, Apple-style.
"""
from flask import abort
from flask import request
from flask.views import MethodView

from automx2 import AutomxException
from automx2 import log
from automx2.generators.apple import AppleGenerator
from automx2.views import EMAIL_MOZILLA
from automx2.views import MailConfig

CONTENT_TYPE_APPLE = 'application/x-apple-aspen-config'


class AppleView(MailConfig, MethodView):
    @staticmethod
    def response_type() -> str:
        return CONTENT_TYPE_APPLE

    def get(self):
        """GET request is expected to contain ?emailaddress=user@example.com"""
        address = request.args.get(EMAIL_MOZILLA, '')
        realname = request.args.get('name', 'Not Specified')
        if not address:
            message = f'Missing request argument "{EMAIL_MOZILLA}"'
            log.error(message)
            return message, 400
        try:
            return self.config_from_address(address, realname)
        except AutomxException as e:
            log.exception(e)
            abort(400)

    def config_response(self, local_part, domain_part: str, realname: str, password: str) -> str:
        data = AppleGenerator().client_config(local_part, domain_part, realname, password)
        return data