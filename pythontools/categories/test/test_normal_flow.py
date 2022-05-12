from pythontools.categories import v4api, util
import os

'''
Performs all tests using admin user.
This is not an rbac test.
'''
api = v4api.V4CategoriesApi()

def test_create_category_success():
    response = api.create({
        'name': util.create_category_name(),
    })

    assert response.status_code == 201


def test_get_category_by_ext_id_success():
    name = util.create_category_name()
    extId = api.create({
        'name': name,
    }).json()['data']['extId']

    response = api.getone(extId)

    assert response.status_code == 200

    body = response.json()
    assert body['data']['name'] == name


def test_create_child_category_success():
    parentCatName = util.create_category_name()
    parentCatId = api.create({'name': parentCatName}).json()['data']['extId']

    response = api.create({
        'name': parentCatName,
        'parentExtId': parentCatId
    })

    assert response.status_code == 201

    body = response.json()
    assert body['data']['parentExtId'] == parentCatId


def test_create_child_category_under_non_existent_parent_failure():
    response = api.create({
        'name': util.create_category_name(),
        'parentExtId': util.AAA_UUID
    })

    assert response.status_code == 400

    body = response.json()
    assert body['data']['error'][0]['code'] == 'CTGRS-50001'


def test_update_category_no_etag_failure():
    ext_id = api.create({'name': util.create_category_name()}).json()['data'][
        'extId']

    req_body = api.getone(ext_id).json()['data']

    response = api.update(ext_id, None, req_body)

    assert response.status_code == 428


def test_update_category_description_success():
    extId = api.create({'name': util.create_category_name()}).json()['data'][
        'extId']
    get_api_res = api.getone(extId)

    etag = get_api_res.headers['Etag']
    req_body = get_api_res.json()['data']
    desc = util.create_category_description()
    req_body['description'] = desc

    response = api.update(extId, etag, req_body)

    assert response.status_code == 200

    response = api.getone(extId)
    assert response.json()['data']['description'] == desc


def test_delete_category_success():
    extId = api.create({'name': util.create_category_name()}).json()['data']['extId']

    response = api.delete(extId)

    assert response.status_code == 204

def test_delete_non_existent_category_failure():
    response = api.delete(util.AAA_UUID)

    assert response.status_code == 404
    assert response.json()['data']['error'][0]['code'] == 'CTGRS-50006'
