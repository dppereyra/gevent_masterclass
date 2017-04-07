import gevent.monkey
gevent.monkey.patch_all()

import click
import gevent
from gevent.pool import Pool, Semaphore

from demo.coroutines.data import addresses
from demo.coroutines.common import check_ip

max_threads = 10
semaphore = Semaphore(value=max_threads)


def check_ip_w_catch(ip):
    with semaphore:
        click.secho('Acquired semaphore.', bg='white', fg='black')
        result = check_ip(ip, True)
    click.secho('Release semaphore.', bg='white', fg='black')
    return result


def check_ip_wo_catch(ip):
    gevent.sleep(random.choice(delays))
    with semaphore:
        click.secho('Acquired semaphore.', bg='white', fg='black')
        result = check_ip(ip, False)
    click.secho('Release semaphore.', bg='white', fg='black')
    return result


def main(catch):

    fn = check_ip_w_catch if catch else check_ip_wo_catch

    pool = Pool()
    results = pool.map(fn, addresses)

    for result in results:
        if not result:
            continue
        click.secho(result, fg='magenta')
