from pythontools.categories import v4api, util

api = v4api.V4CategoriesApi()

def test_remove_description_update_add_description_again_update_success():
    description = util.create_category_description()
    res = api.create({'name': util.create_category_name(), 'description': description})
    ext_id = res.json()['data']['extId']

    print(f'ext_id:{ext_id}')

    res = api.getone(ext_id)
    cat = res.json()['data']
    print(f'body:{cat}')
    assert cat['description'] == description
    etag = res.headers['Etag']

    cat.pop('description')
    res = api.update(ext_id, etag, cat)
    assert res.status_code == 200

    res = api.getone(ext_id)
    cat = res.json()['data']
    assert cat.get('description', None) is None
    etag = res.headers['Etag']

    cat['description'] = 'newdesc'
    res = api.update(ext_id, etag, cat)
    assert res.status_code == 200

    res = api.getone(ext_id)
    cat = res.json()['data']
    assert cat['description'] == 'newdesc'
