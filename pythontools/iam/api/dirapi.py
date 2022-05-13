import requests

from pythontools.common.apibase import ApiBase
from pythontools.iam import const


class DirApi(ApiBase):
    def create(self):
        return requests.post(
            url=const.ACTDIR_CREATE_URL.format(host=self.pc_ip),
            json=const.ACTDIR_SPEC, **self.request_args)

    def list(self):
        return requests.post(url=const.ACTDIR_LIST_URL.format(host=self.pc_ip),
                             json={}, **self.request_args)

    def search(self, username, actdir_uuid):
        return requests.post(url=const.ACTDIR_SEARCH_URL.format(host=self.pc_ip,
                                                                uuid=actdir_uuid),
                             json={
                                 "query": username,
                                 "returned_attribute_list": [
                                     "userPrincipalName"
                                 ],
                                 "searched_attribute_list": [
                                     "userPrincipalName"
                                 ]
                             }, **self.request_args)
