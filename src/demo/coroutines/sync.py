import click

from demo.coroutines.data import addresses
from demo.coroutines.common import check_ip

def main(catch):
    results  = [check_ip(ip, catch) for ip in addresses]

    for result in results:
        if not result:
            continue
        click.secho(result, fg='magenta')
