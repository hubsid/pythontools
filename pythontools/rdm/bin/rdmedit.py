import click
from pythontools.rdm import rdmedit

@click.command()
@click.option('--duration', type=int, default=24, help='duration to extend the deployment, in hours. If a deployment\n'
                                                       'currently has an expiry of 7 hours, and --duration is given as 3,\n'
                                                       'then the resulting expiry will be 10 hours')
@click.option('--deployment-id', 'deployment_id', help='extend the expiry of the deployment with a particular uuid.\n'
                                                       'if this option is given, then the option --nthlast is ignored')
@click.option('--nthlast', default=0, help='if the option --deployment-id is not given, then this option is used to select the nth active deployment\n'
                                           'in case of multiple active deployments')
def main(duration, deployment_id, nthlast):
    """
    \b
    A tool to extend the duration of an existing active rdm deployment.
    The deployments belonging to user as defined in pythontools.common.RDM_USER alone are considered.
    Either a deployment uuid can be given, or the most recently deployed active deployment is considered.
    If there are multiple active deployments, then option is given to select the particular ones in the list.
    If there is no active deployment, and no uuid is given as option, then the operation is aborted.
    \b
    Usage examples:
    1. extend the most recently deployed active deployment by 12 hours: rdmedit.py --duration 12
    2. extend the 2nd most recently deployed active deployment by 36 hours: rdmedit.py --duration 36 --nthlast 1
        considering that, there are more than 1 active deployments
    3. extend the expiry of a particular deployment with uuid 'adsf' by 7 hours: rdmedit.py --deployment-id asdf --duration 7
    """
    success, result = rdmedit.main(duration, deployment_id, nthlast)

    click.clear()
    if success:
        if result.status_code == 200:
            print('SUCCESS')
        else:
            print('FAILURE')
        print(result.text)
    else:
        print('FAILURE BEFORE INVOKING DEPLOYMENT EDIT API')
        print(result)


if __name__ == '__main__':
    main()
