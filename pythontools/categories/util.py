import os
from random import random

from pythontools.categories import v4api

AAA_UUID = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa'

def create_category_name():
    return 'cat_' + str(random())

def create_category_description():
    return 'cat_desc_' + str(random())
def create_category_userspecifiedname():
    return 'uname_' + str(random())

def get_pc_ip_from_env():
    try:
        return os.environ['PC']
    except KeyError:
        print('please provide the PC IP in the environment variable \'PC\'')
        exit(1)


def delete_bulk(name_matches, failureLimit, failurecount):
    api = v4api.V4CategoriesApi(pc_ip=get_pc_ip_from_env())
    failureLimit = 10
    failurecount = 0
    while True:
        print('*' * 100)
        response = api.getall(query_params={
            '$filter': 'contains(name, \'cat_\')',
            '$limit': 100
        })

        if response.status_code == 200:
            body = response.json()
            print(body)
            categories = body['data']
            print(f'{len(categories)} results obtained')
            if len(categories) == 0:
                print('no more results, exiting')
                break
            print(f'deleting {len(categories)}')
            for category in categories:
                api.delete(category['extId'])

        else:
            if failurecount > failureLimit:
                break
            failurecount += 1
            print(response.status_code)
            print(response.text)

    print('=' * 100)
    if failurecount > failureLimit:
        print('broke loop due to continuous failure')
    else:
        print('success')
