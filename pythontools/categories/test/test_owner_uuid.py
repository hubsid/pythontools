import json
import os

from pythontools.categories import v4apihelper, util, const

api = v4apihelper.V4CategoriesApiHelper()

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

def test_update_without_owner_field_success():
    extId = api.create({'name': util.create_category_name()}).json()['data'][
        'extId']
    get_api_res = api.getone(extId)

    etag = get_api_res.headers['Etag']
    req_body = get_api_res.json()['data']
    desc = util.create_category_description()
    req_body['description'] = desc

    del req_body['ownerUuid']

    response = api.update(extId, etag, req_body)

    assert response.status_code == 200

    response = api.getone(extId)
    assert response.json()['data']['description'] == desc


def test_admin_updates_wrong_owner_uuid_fails():
    extId = api.create({'name': util.create_category_name()}).json()['data']['extId']

    response = api.getone(extId)
    category = response.json()['data']
    category['ownerUuid'] = util.AAA_UUID

    response = api.update(extId, response.headers['Etag'], category)

    print(json.dumps(response.text, indent=4))
    assert response.status_code == 400

def test_admin_updates_to_ca_user1_from_admin_success():
    ext_id = api.create_with_name().json()['data']['extId']

    res = api.getone(ext_id)

    assert res.status_code == 200
    assert res.json()['data']['ownerUuid'] == const.ADMIN_UUID

    rbacuser = os.environ.get('rbacuser')

    res = api.update_with_etag(ext_id, remove=['ownerUuid'], include={'ownerUuid': rbacuser})
    print(res.text)
    assert res.status_code == 200

    res = api.getone(ext_id)
    assert res.json()['data']['ownerUuid'] == rbacuser

def test_rbac_user_cant_update_owner_uuid():
    username = os.environ.get('username')
    password = os.environ.get('password')
    api_rbac = v4apihelper.V4CategoriesApiHelper(username=username, password=password)

    ext_id = api_rbac.create_with_name().json()['data']['extId']

    res = api_rbac.update_with_etag(ext_id, remove=['ownerUuid'], include={'ownerUuid': const.ADMIN_UUID})

    assert res.status_code == 403