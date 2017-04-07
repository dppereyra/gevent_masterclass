import gevent.monkey
gevent.monkey.patch_all()

import click
import gevent
from gevent.pool import Pool

from demo.coroutines.data import addresses
from demo.coroutines.common import check_ip


def check_ip_w_catch(ip):
    return check_ip(ip, True)


def check_ip_wo_catch(ip):
    return check_ip(ip, False)


def main(catch):
    threads = [gevent.spawn(check_ip, ip, catch) for ip in addresses]
    gevent.joinall(threads)

    results = [thread.value for thread in threads if thread.successful()]

    for result in results:
        if not result:
            continue
        click.secho(result, fg='magenta')


def main_pooled(catch):
    fn = check_ip_w_catch if catch else check_ip_wo_catch

    max_threads = 10
    pool = Pool(size=max_threads)
    results = pool.map(fn, addresses)

    for result in results:
        if not result:
            continue
        click.secho(result, fg='magenta')
