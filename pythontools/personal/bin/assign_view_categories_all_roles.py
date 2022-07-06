#!/usr/local/bin/python3
import copy
import json
import logging
import sys

import requests

USERPASS = ['admin', 'Nutanix.123']
PC_IP = '10.36.240.103'
ROLE_FILTER = ''
LOG_FILE = '/tmp/assign_view_categories_all_roles.log'


def make_rest_call(url, method='get', request_body=None, headers=None,params=None):
    response = requests.__getattribute__(method)(url=url,
                                                 json=request_body,
                                                 auth=requests.auth.HTTPBasicAuth(USERPASS[0],
                                                                                  USERPASS[1]),
                                                 verify=False)
    return response.status_code, response.json(), response.headers

def get_url():
    return 'https://' + PC_IP + ':9440'


def check_200_success(status, api_name):
    if status != 200:
        logging.info(f'{api_name} returned {status} http status, expected 200')
        sys.exit(1)


def check_202_success(status, api_name):
    if status != 202:
        logging.info(f'{api_name} returned {status} http status, expected 202')
        sys.exit(1)


def get_view_category_permission_ext_id():
    status, response_json, headers = make_rest_call(
        url=get_url() + '/api/nutanix/v3/permissions/list',
        method='post',
        request_body={
            'length': 1,
            'offset': 0,
            'filter': 'name==^View_Category$'
        })
    check_200_success(status, 'view category api')

    # logging.info()(status)
    # logging.info()('-----------')
    # logging.info()(response_json)
    # logging.info()('-----------')
    # logging.info()(headers)

    if (response_json['metadata']['total_matches'] == 0):
        logging.info('View_Category permission is not present in system')
        sys.exit(1)
    return response_json['entities'][0]


def get_all_roles():
    length = 20
    offset = 0
    entity_count = 100
    roles = []
    while entity_count > 0:
        status, response_json, headers = make_rest_call(
            url=get_url() + '//api/nutanix/v3/roles/list',
            method='post',
            request_body={
                'length': length,
                'offset': offset,
                'filter': ROLE_FILTER
            })
        check_200_success(status, f'get all roles with offset {offset}, length {length}')

        roles += response_json['entities']
        entity_count = len(response_json['entities'])
        offset += length

    return roles


def prepare_role_for_update(permission, role):
    role = copy.deepcopy(role)
    del role['status']
    role['metadata']['spec_version'] += 1
    role['spec']['resources']['permission_reference_list'].append({
        'kind': 'permission',
        'name': permission['spec']['name'],
        'uuid': permission['metadata']['uuid']
    })
    return role

def add_view_category_permission_to_role(permission, role):
    role = prepare_role_for_update(permission, role)

    status, response_json, headers = make_rest_call(
        url=get_url() + '/api/nutanix/v3/roles/{0}'.format(
            role['metadata']['uuid']),
        method='put',
        request_body=role)

    check_202_success(status, 'put role api for role {0}'.format(role['spec']['name']))

def already_contains_permission(permission, role):
    for permission_obj in role['spec']['resources']['permission_reference_list']:
        if permission_obj['name'] == permission:
            return True
    return False


def batch_update_roles(roles_to_update):
    request_body = {
        'action_on_failure': 'CONTINUE',
        'execution_order': 'NON_SEQUENTIAL',
        'api_request_list': []
    }
    for role in roles_to_update:
        api_request = {
            'operation': 'PUT',
            'path_and_params': '/api/nutanix/v3/roles/{0}'.format(role['metadata']['uuid']),
            'body': role
        }
        request_body['api_request_list'].append(api_request)

    status, response_json, headers = make_rest_call(url=get_url() + '/api/nutanix/v3/batch',
                   method='post',
                   request_body=request_body)

    check_200_success(status, 'batch role update')
    return response_json


def main():
    logging.basicConfig(filename=LOG_FILE, encoding='utf-8', level=logging.INFO)

    permission = get_view_category_permission_ext_id()
    logging.info('got View_Category permission: {0}'.format(permission['metadata']['uuid']))
    logging.info('getting all roles...')
    all_roles = get_all_roles()
    logging.info('got all roles in system:')
    for role in all_roles:
        logging.info('\t' + role['spec']['name'])

    roles_to_update = []
    for role in all_roles:
        if already_contains_permission('View_Category', role):
            logging.info('skipping role {0}; already contains View_Category permission'.format(role['spec']['name']))
            continue
        elif role['status']['is_system_defined']:
            logging.info('skipping role {0}; is system defined'.format(role['spec']['name']))
            continue

        role = prepare_role_for_update(permission, role)
        roles_to_update.append(role)

    logging.info('calling batch update for following roles:')
    for role in roles_to_update:
        logging.info('\t' + role['spec']['name'])

    update_result = batch_update_roles(roles_to_update)
    responses = update_result['api_response_list']

    failed_calls = []
    for response in responses:
        if response['status'] != '202' and response['status'] != 202:
            failed_calls.append(response)

    if failed_calls:
        for response in failed_calls:
            logging.info(json.dumps(response, indent=4))

    logging.info('---DONE')

if __name__ == '__main__':
    main()
