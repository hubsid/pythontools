import json
import os
import click
from pythontools.rdm import rdmstatus

@click.command()
@click.option('--lastn', type=int, help='The number of deployments of the user to fetch, ordered by most recently deployed. It defaults to 1')
@click.option('--active', is_flag=True, help='Fetch only active deployments. Active means all deployments that have not failed or released')
@click.option('--user', type=str, help='Whose deployment you want to fetch. The value should match the login name in RDM UI. When this option is not provided,'
                             '\n it defaults to the user defined by the variable RDM_USER in pythontools.common.__init__.py')
# @click.option('--show', type=Choice(list(FIELDS_MAP_PRIMARY)), multiple=True)
def main(lastn, active, user):
    """
    \b
    This script retreives the status of rdm deployment in json format.
    \b
    Common use cases:
    1. Check if my last deployment is successful or not: rdmstatus.py
    2. Fetch 5 of my recent deployments: rdmstatus.py --lastn 5
    3. Fetch only active deployments: rdmstatus.py --active --lastn 5
    4. Fetch another user's active deployment: rdmstatus.py --active --user ajay.kudale
    \b
    Fields shown in the output:
        rdm_link: (the url to the deployment in RDM UI),with_cmsp,expires_in,status
        secondary_deployments: individual details about NOS_CLUSTER, PC and PC_PE registration
        secondary_deployment fields:
            status,type,ip,resource_name
    """
    results = rdmstatus.main(lastn=lastn, active=active, user=user)

    os.system('clear')
    click.echo(f'CALL SUCCESS\nRESULTS---\n')
    click.echo(json.dumps(results, indent=4))

if __name__ == '__main__':
    main()