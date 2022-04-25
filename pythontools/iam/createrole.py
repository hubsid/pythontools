import click
import requests

from pythontools import common


@click.command()
@click.option('--host', default=common.PC)
@click.argument('name')
def main(host, name):

	result = create_role(host, name)

	click.clear()

	if result.status_code == 202:
		print('SUCCESS')
	else:
		print(f'FAILURE\nstatus code:{result.status_code}\nresponse:{result.text}')

def create_role(host, name):

	reqbody = {
	  "spec": {
	    "name": name,
	    "resources": {
	      "permission_reference_list": []
	    }
	  },
	  "metadata": {
	    "kind": "role"
	  },
	  "api_version": "3.1.0"
	}

	res = requests.post(url=f'https://{host}:9440/api/nutanix/v3/roles',
						json=reqbody,
						auth=common.ADMIN_AUTH,
						verify=False)

	return res

if __name__ == '__main__':
	main()