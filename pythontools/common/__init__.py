def make_permission_obj(uuid):
	return {
		"kind": "permission",
		"uuid": uuid
	}


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

