import click
import requests

from pythontools.common import const, util
from pythontools.iam.api.dirapi import DirApi
from pythontools.iam.api.userapi import UserApi


@click.command()
@click.argument('host', default=const.PC)
def main(host):
    create(host)


def create(host):
    try:
        res = DirApi().create()
        print(f'STATUS_CODE:{res.status_code}\nTEXT:{res.text}')

        if res.status_code / 100 == 2:
            print('\n\nSUCCESS')
            return True
        elif 'already exists' in res.text:
            print('ALREADY EXISTS')
            return True
        else:
            print('FAILURE')
            return False
    except requests.exceptions.ConnectionError:
        print(f'not able to connect to the host {host}')
        return False

# returns the first user that matches the parameter value: name
def search_user(host, name, domain='qa.nutanix.com'):
    res = UserApi(pc_ip=host).search(name, domain)
    util.check_api_invocation('search user in directory', res)

    res = res.json()
    group_results = res['api_response_list'][0]['api_response']['group_results']
    if not group_results:
        print(
            f'group results is empty during search user of : {name} in domain:{domain}')
        exit(1)
    entity_results = group_results[0]['entity_results']
    if not entity_results:
        print(
            f'entity results is empty during search user of : {name} in domain:{domain}')
        exit(1)
    entity = entity_results[0]
    return entity['entity_id']


# gets the uuid of the user from ldap active directory qa.nutanix.com
def get_actdir_details(host, actdirname):
    res = DirApi().list()
    util.check_api_invocation('list actdir', res)
    res = res.json()

    for actdir in res['entities']:
        if actdir['spec']['name'] == actdirname:
            return actdir
    print(f'no such active directory:{actdirname}')
    exit(1)


def search_actdir(host, actdir_uuid, username):
    res = DirApi(pc_ip=host).search(username, actdir_uuid)
    util.check_api_invocation('directory search', res)
    res = res.json()
    for user in res['search_result_list']:
        attr_objs = user['attribute_list']
        for attr_obj in attr_objs:
            if attr_obj['name'] == 'userPrincipalName' and username in attr_obj['value_list']:
                return user
    return None


def create_user(host, username, actdir_uuid, domain='qa.nutanix.com'):
    res = UserApi(pc_ip=host).create(name=username, actdir_uuid=actdir_uuid, domain=domain)
    util.check_api_invocation('create user', res, [202, 400])
    if res.status_code == 400:
        res = res.json()
        if 'DUPLICATE_ENTITY' not in [msg['reason'] for msg in
                                      res['message_list']]:
            print(
                f'create user failed with statuscode 400 and error response:{res}')


def get_user_uuid(host, username, actdir_uuid, actdirname, domain='qa.nutanix.com'):
    if not actdir_uuid:
        res = get_actdir_details(host, actdirname)
        actdir_uuid = res['metadata']['uuid']
    user = search_actdir(host, actdir_uuid, username)

    if not user:
        create_user(host, username, actdir_uuid, domain)
    return search_user(host, username, domain)


if __name__ == '__main__':
    # uuid = get_user_uuid(common.PC, 'ca_user1@qa.nutanix.com', '03d0e8e1-c53b-5900-a4cd-7b6114a2e63a', None)

    # print(f'success, uuid of user={uuid}')
    main()
