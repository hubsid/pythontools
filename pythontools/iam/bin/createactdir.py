import click

from pythontools.categories import const
from pythontools.iam import actdir


@click.command()
@click.argument('host', default=const.PC, help='the vm ip, on which to create the active directory')
def main(host):
    """
    \b
    This creates an active directory on the host mentioned, based on the specifications
    defined in pythontools.iam.ACTDIR_SPEC
    """
    actdir.create(host)

