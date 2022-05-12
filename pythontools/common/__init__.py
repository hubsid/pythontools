import os
import subprocess
import requests
from enum import Enum

PC = os.environ.get('PC')
UBVM = os.environ.get('UBVM')
PC_PASS = 'nutanix/4u'
OKTA_PASS = subprocess.run(['sh', '-c', 'oktapswd.sh | base64 -d'], capture_output=True).stdout.decode('utf-8')[0:-1]
ADMIN_AUTH = requests.auth.HTTPBasicAuth('admin', 'Nutanix.123')
RDM_USERNAME='sidharth.r'
RDM_AUTH=requests.auth.HTTPBasicAuth(RDM_USERNAME, OKTA_PASS)

class Identifier(Enum):
	UUID = 1
	NAME = 2

class Operation(Enum):
	ADD = 1
	REMOVE = 2
	SET = 3
	CLEAR = 4

def printfile(file):
	for line in file:
		print(line, end='')

def make_permission_obj(uuid):
	return {
		"kind": "permission",
		"uuid": uuid
	}

def check_api_invocation(apiname, response, status_codes=None):
	if status_codes is None:
		status_codes = [200]
	if response.status_code not in status_codes:
		print(f'{apiname} api invocation failed:status_code:{response.status_code},\nresponse:{response.text}')
		exit(1)

def v3_api_searcher(api_caller, total_finder, offset_finder, entities_path_finder, attribute_path_finder, match_values):
	offset = 0
	response_json = api_caller(offset=0)

	entity_map = {}
	match_values_mutable = match_values.copy()

	search(response_json, entities_path_finder, attribute_path_finder, match_values_mutable, entity_map)
	if not match_values_mutable:
		return entity_map

	count = total_finder(response_json)
	offset = offset_finder(response_json)
	while offset < count:
		response_json = api_caller(offset=offset)

		search(response_json, entities_path_finder, attribute_path_finder, match_values_mutable, entity_map)
		if not match_values_mutable:
			return entity_map

		offset += offset_finder(response_json)

	return entity_map

def search(response_json, entities_path_finder, attribute_path_finder, match_values_mutable, entity_map):
	if not match_values_mutable:
		return
	entities = entities_path_finder(response_json)

	for entity in entities:
		attribute_value = attribute_path_finder(entity)

		if attribute_value in match_values_mutable:
			entity_map[attribute_value] = entity
			match_values_mutable.remove(attribute_value)

		if not match_values_mutable:
			return

def clean_role_entity(role):
	newrole = {}
	newrole['name'] = role['status']['name']
	newrole['uuid'] = role['metadata']['uuid']
	newrole['permissions'] = []

	for permission in role['status']['resources']['permission_reference_list']:
		newrole['permissions'].append(permission['name'])
	return newrole

def clean_permission_entity(permission):
	return permission['metadata']['uuid']

def get_pc_ip_from_env():
	try:
		return os.environ['PC']
	except KeyError:
		print('please provide the PC IP in the environment variable \'PC\'')
		exit(1)
