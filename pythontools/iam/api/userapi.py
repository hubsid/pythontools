import requests

from pythontools.iam import const
from pythontools.common.apibase import ApiBase
from pythontools.common import const as commonconst


class UserApi(ApiBase):
    def base_url(self):
        return const.V3_USERS_BASE_URL.format(host=self.pc_ip)

    def list_url(self):
        return const.V3_USERS_LIST_URL.format(host=self.pc_ip)

    def single_entity_url(self, uuid):
        return const.V3_USERS_SINGLE_ENTITY_URL.format(host=self.pc_ip,
                                                       uuid=uuid)

    def list(self):
        return requests.post(self.list_url(), json={}, **self.request_args)

    def get(self, uuid):
        return requests.get(self.single_entity_url(uuid), **self.request_args)

    def search(self, name, domain=commonconst.QA_DOMAIN):
        return requests.post(
            url=commonconst.V3_GROUPS_URL.format(host=self.pc_ip),
            json={
                "entity_type": "user",
                "group_member_attributes": [
                    {
                        "attribute": "directory_domain"
                    },
                    {
                        "attribute": "user_type"
                    },
                    {
                        "attribute": "user_principal_name"
                    },
                    {
                        "attribute": "username"
                    }
                ],
                "query_name": "prism:GroupsRequestModel",
                "filter_criteria": f"directory_domain=={domain};user_principal_name==.*{name}.*"
            }, **self.request_args)

    def create(self, name, actdir_uuid, domain='qa.nutanix.com'):
        return requests.post(self.base_url(), json={
            'metadata': {
                'kind': 'user'
            },
            'spec': {
                'resources': {
                    'directory_service_user': {
                        'user_principal_name': name + '@' + domain,
                        'directory_service_reference': {
                            'kind': 'directory_service',
                            'uuid': actdir_uuid}
                    }
                }
            }
        }, **self.request_args)
