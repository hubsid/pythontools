import json

import click
import requests

from pythontools.iam import findrole
from pythontools import common


@click.command()
@click.option('--host', default=common.PC)
@click.option('--name', 'key', flag_value=common.Identifier.NAME.name)
@click.option('--uuid', 'key', flag_value=common.Identifier.UUID.name)
@click.argument('values', nargs=-1)
def main(host, key, values):
	roles = getrole(host, key, list(values))

	for role_identifier in roles:
		roles[role_identifier] = common.clean_role_entity(roles[role_identifier])

	click.clear()
	print(json.dumps(roles, indent=4))

def getrole(host, key, values):
	uuids = values
	if key == common.Identifier.NAME.name:
		find_results_map = findrole.findrole(host, values)


		# print(f'FIND_RESULTS_MAP\n{find_results_map}')
		if not find_results_map:
			click.clear()
			print(f'roles by names {values} not found')
			exit(1)
		return find_results_map

	result = {}
	for uuid in uuids:
		response = requests.get(url=f'https://{host}:9440/api/nutanix/v3/roles/{uuid}',
							auth=common.ADMIN_AUTH,
							verify=False)
		if response.status_code == 200:
			result[uuid] = response.json()
		else:
			result[uuid] = None

	return result

if __name__ == '__main__':
	main()
