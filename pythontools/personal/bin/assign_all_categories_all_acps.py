#!/usr/local/bin/python3
import copy
import json
import logging
import sys

import requests

USERPASS = ['admin', 'Nutanix.123']
PC_IP = '10.36.240.103'
ROLE_FILTER = ''
ACPS_TO_EXCLUDE = ['Super Admin_acp', 'Prism Admin_acp', 'Prism Viewer_acp']
LOG_FILE = '/tmp/assign_all_categories_all_acps.log'

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
        logging.error(f'{api_name} returned {status} http status, expected 200')
        sys.exit(1)

def list_all_acps():
    length = 20
    offset = 0
    entity_count = 100
    acps = []
    while entity_count > 0:
        status, response_json, headers = make_rest_call(
            url=get_url() + '/api/nutanix/v3/access_control_policies/list',
            method='post',
            request_body={
                'length': length,
                'offset': offset
            })
        check_200_success(status, f'get all acps with offset {offset}, length {length}')

        acps += response_json['entities']
        entity_count = len(response_json['entities'])
        offset += length

    return acps

def add_all_categories_filter_to_acp(acp):
    acp = copy.deepcopy(acp)
    del acp['status']
    filters = acp['spec']['resources']['filter_list']['context_list']
    filters.append({
        'entity_filter_expression_list': [
            {
                'operator': 'IN',
                'left_hand_side': {
                    'entity_type': 'category'
                },
                'right_hand_side': {
                    'collection': 'ALL'
                }
            }
        ]
    })
    return acp

def invoke_acp_update_batch(acps_for_batch_call):
    request_body = {
        'action_on_failure': 'CONTINUE',
        'execution_order': 'NON_SEQUENTIAL',
        'api_request_list': []
    }
    for acp in acps_for_batch_call:
        api_request = {
            'operation': 'PUT',
            'path_and_params': '/api/nutanix/v3/access_control_policies/{0}'.format(acp['metadata']['uuid']),
            'body': acp
        }
        request_body['api_request_list'].append(api_request)

    status, response_json, headers = make_rest_call(url=get_url() + '/api/nutanix/v3/batch',
                                                    method='post',
                                                    request_body=request_body)

    check_200_success(status, 'batch acp update')
    return response_json
def get_acp_name(acp):
    resources = acp['spec']['resources']
    x = resources['user_reference_list']
    return resources['role_reference']['name'] + ' => ' + (x[0]['name'] if x else '')

def main():
    logging.basicConfig(filename=LOG_FILE, encoding='utf-8', level=logging.INFO)

    all_acps = list_all_acps()
    logging.info('got all acps:')
    for acp in all_acps:
        logging.info('\t' + get_acp_name(acp))

    acps_for_batch_call = []
    for acp in all_acps:
        if acp['spec']['name'] in ACPS_TO_EXCLUDE:
            continue
        acps_for_batch_call.append(add_all_categories_filter_to_acp(acp))

    logging.info('invoking batch call to update all acps')
    batch_result = invoke_acp_update_batch(acps_for_batch_call)

    failed_acps = []
    for result in batch_result['api_response_list']:
        if result['status'] != '202' and result['status'] != 202:
            failed_acps.append(result)

    if failed_acps:
        logging.info('failed updating following acps:')
        logging.info(json.dumps(failed_acps, indent=4))

    logging.info('---DONE')
if __name__ == '__main__':
    main()