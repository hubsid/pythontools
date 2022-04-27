from pythontools import common
import requests
from pythontools.categories import const

class V4CategoriesApi:
    def __init__(self, pc_ip, username=None, password=None):
        self.pc_ip = pc_ip
        if not username or not password:
            self.auth = common.ADMIN_AUTH
        else:
            self.auth = requests.auth.HTTPBasicAuth(username, password)
        self.request_args = {'auth': self.auth, 'verify': False}

    def single_entity_url(self, ext_id):
        return const.V4_API_SINGLE_ENTITY_URL.format(pc=self.pc_ip, ext_id=ext_id)

    def base_url(self):
        return const.V4_API_BASE_URL.format(pc=self.pc_ip)

    def getone(self, ext_id):
        return requests.get(self.single_entity_url(ext_id), **self.request_args)

    def getall(self, query_params=None):
        return requests.get(self.base_url(), params=query_params, **self.request_args)

    def create(self, body):
        return requests.post(self.base_url(), json=body, **self.request_args)

    def delete(self, ext_id):
        return requests.delete(self.single_entity_url(ext_id), **self.request_args)

    def update(self, ext_id, etag, body):
        etag_header = {'If-Match': etag}
        return requests.put(self.single_entity_url(ext_id), headers=etag_header, json=body, **self.request_args)
