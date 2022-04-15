import click
from pythontools.rdm import rdmedit

@click.command()
@click.option('--duration', type=int, default=24)
@click.option('--deployment-id', 'deployment_id')
@click.option('--nthlast', default=0)
def main(duration, deployment_id, nthlast):
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
