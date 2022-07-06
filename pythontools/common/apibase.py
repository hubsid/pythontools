import requests

import pythontools.common.util
from pythontools.common import const
from pythontools import common


class ApiBase:
    def __init__(self, pc_ip=None, username=None, password=None):
        self.pc_ip = pc_ip or common.util.get_pc_ip_from_env()
        if not username or not password:
            self.auth = const.ADMIN_AUTH
        else:
            self.auth = requests.auth.HTTPBasicAuth(username, password)
        self.request_args = {'auth': self.auth, 'verify': False}
