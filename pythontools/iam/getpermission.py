
import json

import click
import requests

import common.util
from pythontools.common import const
from pythontools import common


@click.command()
@click.option('--host', default=const.PC)
@click.argument('permission_names', nargs=-1)
def main(host, permission_names):
	permission_map = fetch(host, list(permission_names))

	if not permission_map:
		print('not found')
		exit(1)
	click.clear()

	for permission_identifier in permission_map:
		permission_map[permission_identifier] = common.clean_permission_entity(permission_map[permission_identifier])

	print(json.dumps(permission_map, indent=4))

def fetch(host=const.PC, permission_names=[]):
	def api_caller(offset):
		print(f'making call with offset:{offset}')
		response = listallapi(host, offset)
		common.util.check_api_invocation('list permissions', response)
		return response.json()

	return common.util.v3_api_searcher(api_caller,
									   lambda r: r['metadata']['total_matches'],
									   lambda r: len(r['entities']),
									   lambda r: r['entities'],
									   lambda p: p['status']['name'],
									   permission_names)

def listallapi(host, offset=0):
	return requests.post(url=f'https://{host}:9440/api/nutanix/v3/permissions/list',
						auth=const.ADMIN_AUTH,
						json={'offset': offset, 'length': 500},
						verify=False)

if __name__ == '__main__':
	main()