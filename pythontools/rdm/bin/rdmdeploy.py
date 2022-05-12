import click
from pythontools.rdm import rdmdeploy

@click.command()
@click.option('--name', help='unique name for the deployment, if not supplied, the '
                             '\nname will be calculated using the logged in user\'s name'
                             '\n appended with a random floating point number')
@click.option('--nodepool', type=click.Choice(['private', 'global']), default='private',
              help='the nodepool on which to deploy. by default deployed on prism-real-node'
                   '\n private node pool.')
@click.option('--nocmsp', is_flag=True, help='if this flag is provided, then the'
                                             '\ndeployed pc will not have cmsp')
# @click.option('--pcbuildurl')
@click.option('--duration', type=int, default=24, required=True, help='duration of the deployment.\n'
                                                       'maximum duration is subject to restrictions imposed by admins and rdm policies')
def main(name, nodepool, nocmsp, duration):
    """
    \b
    Deploy a latest master PE/PC using rdm on either global/private nodepools and with/without
    cmsp, and register the PE to the PC.
    The pc build will be one which is smoke passed. In case smoke passed builds are
    not available, the deployment will be aborted.
    The deployment status can be tracked using rdmstatus.py script
    \b
    Examples:
    1. On the prism-real-node private nodepool (which is by default), deploy a PE-PC with cmsp for a
    duration of 4 days: rdmdeploy.py --duration 96
    2. On the global nodepool, deploy a PE-PC without cmsp, for the default
    duration of 1 day: rdmdeploy.py --nodepool global --nocmsp
    """
    res = rdmdeploy.main(name, nodepool, nocmsp, duration)

    if res.status_code == 200:
        click.clear()
        print(f'SUCCESS!\n{res.text}')
        print(f'request headers:{res.request.headers}')
    else:
        print(
            f'\n\nFAILURE\nSTATUS_CODE: {res.status_code}\nMESSAGE: {res.text}')

if __name__ == '__main__':
    main()