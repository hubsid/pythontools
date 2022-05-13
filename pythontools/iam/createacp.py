
import click
import requests

from pythontools.common import const
from pythontools import common
from pythontools.iam import actdir, findrole


@click.command()
@click.option('--host', default=const.PC)
@click.option('--role', 'role_name', required=True)
@click.option('--actdir', 'actdirname', default='actdir')
@click.option('--user', 'user_name', default='ca_user1')
@click.option('--domain', default='qa.nutanix.com')
def main(host, role_name, actdirname, user_name, domain):
	uuid = create(host, role_name, actdirname, user_name, domain)

	click.clear()
	print('SUCCESS')
	print('UUID:' + uuid)

def create(host, role_name, actdirname='actdir', user_name='ca_user1', domain='qa.nutanix.com',verify=False):
	acp_name = 'acp ' + role_name + '_' + user_name
	acp_desc = 'desc-' + acp_name

	role_map = findrole.findrole(host, [role_name])

	if not role_map:
		print(f'no such role by name:{role_name}')
		exit(1)

	role = role_map[role_name]
	role_uuid = role['metadata']['uuid']

	user_uuid = actdir.get_user_uuid(host, user_name, None, actdirname, domain)

	if not user_uuid:
		print(f'no such user by the name {user_name} found in the domain {domain}')
		exit(1)

	res = requests.post(url=f'https://{host}:9440/api/nutanix/v3/access_control_policies',
						json={
						    'spec': {
						        'name': acp_name,
						        'description': acp_desc,
						        'resources': {
						            'role_reference': {
						                'kind': 'role',
						                'name': role_name,
						                'uuid': role_uuid
						            },
						            'filter_list': {
						                'context_list': []
						            },
						            'user_reference_list': [
						                {
						                    'kind': 'user',
						                    'name': f'{user_name}@{domain}',
						                    'uuid': user_uuid
						                }
						            ],
						            'user_group_reference_list': []
						        }
						    },
						    'metadata': {
						        'kind': 'access_control_policy'
						    }
						},
						auth=const.ADMIN_AUTH,
						verify=False)
	if res.status_code != 202:
		print(f'failed creating acp, status_code:{res.status_code}\nresponse:{res.text}')
		exit(1)

	res = res.json()
	acp_uuid = res['metadata']['uuid']

	if not verify:
		return acp_uuid


if __name__ == '__main__':
	main()