V3_USERS_BASE_URL = 'https://{host}:9440/api/nutanix/v3/users'
V3_USERS_SINGLE_ENTITY_URL = V3_USERS_BASE_URL + '/{uuid}'
V3_USERS_LIST_URL = V3_USERS_BASE_URL + '/list'
ACTDIR_CREATE_URL= 'https://{host}:9440/PrismGateway/services/rest/v1/authconfig/directories'
ACTDIR_SPEC = {
    "name": "actdir",
    "domain": "qa.nutanix.com",
    "directoryUrl": "ldap://10.4.99.211:389",
    "groupSearchType": "NON_RECURSIVE",
    "directoryType": "ACTIVE_DIRECTORY",
    "connectionType": "LDAP",
    "serviceAccountUsername": "ssp_admin@qa.nutanix.com",
    "serviceAccountPassword": "nutanix/4u"
}
ACTDIR_BASE_URL = 'https://{host}:9440/api/nutanix/v3/directory_services'
ACTDIR_LIST_URL = ACTDIR_BASE_URL + '/list'
ACTDIR_SEARCH_URL = ACTDIR_BASE_URL + '/{uuid}/search'
