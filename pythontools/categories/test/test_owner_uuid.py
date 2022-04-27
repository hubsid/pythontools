from pythontools.categories import v4api, util

api = v4api.V4CategoriesApi(pc_ip=util.get_pc_ip_from_env())

def test_owner_uuid_is_created():
    response = api.create({'name': util.create_category_name()})
    body = response.json()['data']

    assert body.get('ownerUuid', None)

def test_owner_uuid_in_get_api():
    extId = api.create({'name': util.create_category_name()}).json()['data']['extId']

    response_body = api.getone(extId).json()['data']

    assert response_body.get('ownerUuid', None)

def test_owner_uuid_in_list_api():
    extId = api.create({'name': util.create_category_name()}).json()['data']['extId']

    list_response = api.getall({
        '$filter': f"extId eq '{extId}'"
    })

    response_body = list_response.json()['data'][0]

    assert response_body.get('ownerUuid', None)

def test_admin_can_update_owner():
    extId = api.create({'name': util.create_category_name()}).json()['data']['extId']

    response = api.getone(extId)
    category = response.json()['data']
    category['ownerUuid'] = util.AAA_UUID

    response = api.update(extId, response.headers['Etag'], category)

    assert response.status_code == 200

    response = api.getone(extId)
    assert response.json()['data']['ownerUuid'] == util.AAA_UUID
