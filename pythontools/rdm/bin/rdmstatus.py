import json
import os
import click
from pythontools.rdm import rdmstatus

@click.command()
@click.option('--lastn')
@click.option('--active', is_flag=True)
@click.option('--user')
# @click.option('--show', type=Choice(list(FIELDS_MAP_PRIMARY)), multiple=True)
def main(lastn, active, user):
    results = rdmstatus.main(lastn=lastn, active=active, user=user)

    os.system('clear')
    click.echo(f'CALL SUCCESS\nRESULTS---\n')
    click.echo(json.dumps(results, indent=4))

if __name__ == '__main__':
    main()