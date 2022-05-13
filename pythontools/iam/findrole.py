import json

import click
import requests

import common.util
from pythontools.common import const
from pythontools import common


@click.command()
@click.option('--host', default=const.PC)
@click.argument('names', nargs=-1)
def main(host, names):
	find_results_map = findrole(host, list(names))

	click.clear()
	if find_results_map:
		display_map = {}
		for key in find_results_map.keys():
			display_map[key] = find_results_map[key]['metadata']['uuid']
		print(json.dumps(display_map, indent=4))
	else:
		print('not found')

def findrole(host, names):

	def api_caller(offset):
		response = list_roles_api(host, offset)
		common.util.check_api_invocation('list roles', response)
		return response.json()

	def total_finder(response_json):
		return response_json['metadata']['total_matches']

	def offset_finder(response_json):
		return len(response_json['entities'])

	def entities_path_finder(response_json):
		return response_json['entities']

	def attribute_path_finder(entity):
		return entity['status']['name']

	find_results_map = common.util.v3_api_searcher(api_caller, total_finder, offset_finder, entities_path_finder, attribute_path_finder, names)

	return find_results_map

def list_roles_api(host, offset=0):
	return requests.post(url=f'https://{host}:9440/api/nutanix/v3/roles/list',
						auth=const.ADMIN_AUTH,
						json={'offset': offset},
						verify=False)

if __name__ == '__main__':
	main()