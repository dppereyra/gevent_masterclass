import gevent.monkey
gevent.monkey.patch_all()

import random

import click
from pykka.gevent import GeventActor
import gevent

from demo.coroutines.common import ip2country, ip2longlat
from demo.coroutines.data import addresses


delays = [1, 2, 3, 4, 5]


class CountryChecker(GeventActor):

    def on_start(self):
        click.secho('Country check invoked.', fg='blue', bg='yellow')

    def on_receive(self, message):
        ip = message['ip']
        click.secho('Processing country info of {}'.format(ip), fg='blue')
        return ip2country(ip)

    def on_failure(self, exc_type, exc_value, trace):
        click.secho(repr(exc_type), fg='red')


class LongLatChecker(GeventActor):

    def on_start(self):
        click.secho('Country check invoked.', fg='cyan', bg='white')

    def on_receive(self, message):
        ip = message['ip']
        click.secho('Processing longlat info of {}'.format(ip), fg='blue')
        return ip2longlat(ip)

    def on_failure(self, exc_type, exc_value, trace):
        click.secho(repr(exc_type), fg='red')


class IPChecker(GeventActor):

    def on_start(self):
        click.secho('IP check invoked.', fg='yellow', bg='blue')

    def on_receive(self, message):
        ip = message['ip']
        click.secho('Processing ip: {}'.format(ip), fg='cyan', bg='blue')

        country_checker = CountryChecker.start()
        country = country_checker.ask(message)
        country_checker.stop(block=False)

        longlat_checker = LongLatChecker.start()
        longitude, latitude = longlat_checker.ask(message)
        longlat_checker.stop(block=False)

        result = '{}: {} ({}, {})'.format(ip, country, longitude, latitude)
        click.secho(result)
        return result


def main():
    results = []
    for ip in addresses:
        checker = IPChecker.start()
        results.append(checker.ask({'ip': ip}, block=False))
        checker.stop(block=False)

    for result in results:
        try:
            result.get()
        except Exception as exc:
            click.secho(repr(exc), fg='red')
