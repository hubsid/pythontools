import time

import click
import requests



from pythontools import common
from pythontools.common import const
from pythontools.iam import getpermission, getrole


@click.command()
@click.option('--host', default=const.PC)
@click.option('--operation', type=click.Choice([e.name for e in
												common.const.Operation]))
@click.option('--uuid')
@click.argument('modify_permission_names', nargs=-1)
def main(host, uuid, operation, modify_permission_names):
	if editrole(host, uuid, operation, list(modify_permission_names), False):
		click.clear()
		print('SUCCESS')

def editrole(host, uuid, operation, modify_permission_names, verify):
	rolemap = getrole.getrole(host, 'uuid', [uuid])

	if not rolemap or rolemap.get(uuid, None) is None:
		print(f'no such role with uuid:{uuid}')
		exit(1)

	role = rolemap[uuid]

	role = form_update_request(role)

	uuid_name_map = {}
	for permission in rolemap[uuid]['status']['resources']['permission_reference_list']:
		uuid_name_map[permission['uuid']] = permission['name']

	modify_permissions(role, uuid_name_map, operation, modify_permission_names, host)

	# print('role update request:')
	# print(json.dumps(role, indent=4))

	response = update_role_api(host, uuid, role)

	if response.status_code != 202:
		click.clear()
		print(f'FAILURE,update api returned status code : {response.status_code} with message:\n{response.text}')
		exit(1)

	response_json = response.json()
	task_uuid = response_json['status']['execution_context']['task_uuid']

	# verify that the update has happened by invoking get role api again and checking the task uuid and permissions
	if verify:
		time.sleep(2)
		rolemap = getrole.getrole(host, 'uuid', [uuid])

		role_for_update = role
		role_after_update = rolemap[uuid]

		if role_after_update['status']['execution_context']['task_uuid'][0] != task_uuid:
			click.clear()
			print(f'the task uuids dont match. please verify manually if the update has happened or not')

		permissions_uuids_before = [p['uuid'] for p in role_for_update['spec']['resources']['permission_reference_list']]

		for p in role_after_update['status']['resources']['permission_reference_list']:
			if p['uuid'] not in permissions_uuids_before:
				click.clear()
				print(f'update unsuccessful, the permission by uuid:{p[uuid]} is not updated')
				exit(1)
			permissions_uuids_before.remove(p['uuid'])

	return True

def update_role_api(host, uuid, newrole):
	return requests.put(url=f'https://{host}:9440/api/nutanix/v3/roles/{uuid}',
						json=newrole,
						auth=const.ADMIN_AUTH,
						verify=False)

def form_update_request(role):
	return {
		'spec': role['spec'],
		'metadata': {
			'kind': 'role',
			'spec_version': role['metadata']['spec_version']
		}
	}

def modify_permissions(role, uuid_name_map, operation, modify_permission_names, host):

	role_permissions = role['spec']['resources']['permission_reference_list']

	if operation == common.const.Operation.CLEAR.name:
		role_permissions.clear()

	elif operation == common.const.Operation.REMOVE.name:
		permissions_to_retain = []
		for permission in role_permissions:
			if uuid_name_map[permission['uuid']] not in modify_permission_names:
				permissions_to_retain.append(permission)

		role_permissions.clear()
		role_permissions += permissions_to_retain

	elif operation == common.const.Operation.ADD.name:
		# remove duplicates
		modify_permission_names = [name for name in modify_permission_names if name not in uuid_name_map.values()]

		name_permission_map = getpermission.fetch(host, modify_permission_names)

		for permission in name_permission_map.values():
			role_permissions.append(common.make_permission_obj(permission['metadata']['uuid']))

	elif operation == common.const.Operation.SET.name:
		role_permissions.clear()

		name_permission_map = getpermission.fetch(host, modify_permission_names)

		for permission in name_permission_map.values():
			role_permissions.append(common.make_permission_obj(permission['metadata']['uuid']))


if __name__ == '__main__':
	main()