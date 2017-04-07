import gevent.monkey
gevent.monkey.patch_all()

import random

import click
import gevent
import requests


delays = [1, 2, 3, 4, 5]


def ip2country(ip):
    url = 'https://api.ip2country.info/ip?{}'.format(ip)
    result = requests.get(url)
    click.secho('[C]  {} got: {}'.format(ip, result.status_code), fg='blue')
    return result.json()['countryCode3']


def ip2longlat(ip):
    url = 'https://ipvigilante.com/{}'.format(ip)
    result = requests.get(url)
    click.secho('[LL] {} got: {}'.format(ip, result.status_code), fg='cyan')
    result_json = result.json()
    longitude = float(result_json['data']['longitude'])
    latitude = float(result_json['data']['latitude'])
    gevent.sleep(random.choice(delays))
    return longitude, latitude


def check_ip(ip, catch):
    try:
        click.secho('Checking ip: {}'.format(ip), fg='yellow')
        gevent.sleep(random.choice(delays))
        click.secho('Getting country info: {}'.format(ip), fg='yellow')
        country = ip2country(ip)
        gevent.sleep(0)
        click.secho('Getting longlat info: {}'.format(ip), fg='yellow')
        longitude, latitude = ip2longlat(ip)
        result = '{}: {} ({}, {})'.format(ip, country, longitude, latitude)
        click.secho(result)
        return result
    except Exception as exc:
        if catch:
            click.secho('Error encountered: {}'.format(repr(exc)), fg='red')
        else:
            raise
