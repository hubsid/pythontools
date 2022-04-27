import json
import os
from pythontools.categories import v4api

api = v4api.V4CategoriesApi(pc_ip=os.environ.get('PC_BUG'))


def print_response(response):

    print(f'status:{response.status_code}\ncontent:{json.dumps(response.text, indent=4)}')

# response = api.getall(query_params={'$limit': 1})
# response = api.getone('7dd6f403-5ad2-59ca-ac6f-2d18379735de')
#
# res_json = response.json()
# etag = response.headers.get('Etag')
# categories_req_body = res_json['data']
# categories_req_body['description'] = 'newdesc'
#
# response = api.update('7dd6f403-5ad2-59ca-ac6f-2d18379735de', etag, categories_req_body)
# response = api.create({
#     'name': 'testcat0',
#     'parentExtId': "277338c3-94ce-3727-adee-e4567e890a4d"
# })
# response = api.getone("d998d8a4-d041-3788-9111-07a735298333")
# response = api.getall({
#     '$limit': 10
# })
# rj = response.json()
# body = rj['data']
# print(f'length:{len(body)}')
response = api.getall({
    '$filter': 'contains(name, \'cat\')'
})
print_response(response)
