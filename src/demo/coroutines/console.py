import gevent.monkey
gevent.monkey.patch_all()

import click

from demo.coroutines import coros, actors, sem, sync


@click.group()
def commands():
    pass

@commands.command()
@click.option('--catch', is_flag=True)
@click.option('--pooled', is_flag=True)
def asynchronous(catch, pooled):
    click.secho('Async Demo', fg='green')
    if pooled:
        coros.main_pooled(catch)
    else:
        coros.main(catch)

@commands.command()
@click.option('--catch', is_flag=True)
def synchronous(catch):
    click.secho('Sync Demo', fg='green')
    sync.main(catch)

@commands.command()
@click.option('--catch', is_flag=True)
def semaphored(catch):
    click.secho('Semaphore Demo', fg='green')
    sem.main(catch)

@commands.command()
def actor():
    click.secho('Actors Demo', fg='green')
    actors.main()

def main():
    commands()
