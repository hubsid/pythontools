import click
from pythontools.rdm import rdmdeploy

@click.command()
@click.option('--name')
@click.option('--nodepool', type=click.Choice(['private', 'global']), default='private')
@click.option('--nocmsp', is_flag=True)
# @click.option('--pcbuildurl')
@click.option('--duration', type=int, default=24)
def main(name, nodepool, nocmsp, duration):
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