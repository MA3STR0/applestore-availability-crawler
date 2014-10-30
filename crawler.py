"""Crawler that sends notifications as soon as servers
on Kimsufi/OVH become available for purchase"""

import tornado.ioloop
import tornado.web
import json
import subprocess
from tornado.httpclient import AsyncHTTPClient
from tornado.gen import coroutine
import logging
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')
_logger = logging.getLogger(__name__)

with open('config.json', 'r') as configfile:
    config = json.loads(configfile.read())

URL = "https://reserve.cdn-apple.com/DE/de_DE/reserve/iPhone/availability.json"

PRODUCTS = {
    'iphone6': {
        '128gb': {
            'silver': "MG4C2ZD/A",
            'spacegray': "MG4A2ZD/A",
            'gold': "MG4E2ZD/A"
        },
        '64gb': {
            'silver': "MG4H2ZD/A",
            'spacegray': "MG4F2ZD/A",
            'gold': "MG4J2ZD/A"
        },
        '16gb': {
            'silver': "MG482ZD/A",
            'spacegray': "MG472ZD/A",
            'gold': "MG492ZD/A"
        }
    },
    'iphone6plus': {
        '128gb': {
            'silver': 'MGAE2ZD/A',
            'spacegray': 'MGAC2ZD/A',
            'gold': 'MGAF2ZD/A'
        },
        '64gb': {
            'silver': "MGAJ2ZD/A",
            'spacegray': "MGAH2ZD/A",
            'gold': "MGAK2ZD/A"
        },
        '16gb': {
            'silver': "MGA92ZD/A",
            'spacegray': "MGA82ZD/A",
            'gold': "MGAA2ZD/A"
        }
    }
}

STORES = {
    "MTZ": "R434",
    "OEZ": "R521",
    "Hannover": "R455",
    "Jungfernstieg": "R396",
    "Sindelfingen": "R519",
    "City-Galerie": "R431",
    "Alstertal": "R366",
    "Duesseldorf": "R331",
    "CentrO": "R403",
    "Rhein Center": "R520",
    "Kurfuerstendamm": "R358",
    "Grosse Bockenheimer Strasse": "R352",
    "Rosenstrasse": "R045",
    "Altmarkt-Galerie": "R430"
}

STATES = {}


def send_mail(title, text, url=False):
    """Send email notification using SMTP"""
    msg = MIMEMultipart()
    fromaddr = config['from_email']
    # smtp user may be different from email
    fromuser = config.get('from_user', fromaddr)
    frompwd = config['from_pwd']
    toaddr = config['to_email']
    msg = MIMEMultipart()
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = title
    body = text + '\nURL: ' + url
    msg.attach(MIMEText(body, 'plain'))
    server = smtplib.SMTP(config['from_smtp_host'], config['from_smtp_port'])
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(fromuser, frompwd)
    text = msg.as_string()
    server.sendmail(fromaddr, toaddr, text)


def send_osx_notification(title, text, url=False):
    """Send Mac-OS-X notification using terminal-notifier"""
    subprocess.call(['terminal-notifier',
                     '-title', title,
                     '-message', text,
                     '-open', url
                     ])


def update_state(state, value, message=False):
    """Update state of particular event"""
    # if new value is True and last saved was False
    if state not in STATES:
        STATES[state] = False
    if value is not STATES[state]:
        _logger.info("State change - %s:%s", state, value)
    if value and not STATES[state]:
        send_mail(**message)
    STATES[state] = value


@coroutine
def run_crawler():
    """Run a crawler iteration"""
    http_client = AsyncHTTPClient()
    # request OVH availablility API asynchronously
    response = yield http_client.fetch(URL)
    response_json = json.loads(response.body.decode('utf-8'))
    for store in config['stores']:
        availability = response_json[STORES[store]]
        for product in config['products']:
            for memory in config['memory']:
                for color in config['colors']:
                    model = PRODUCTS[product][memory][color]
                    state_id = '%s_%s_%s_available_in_%s' % (
                        product, memory, color, store)
                    message = {
                        'title': '%s is available' % product,
                        'text': '%s %s %s is available in %s' % (
                            product, memory, color, store),
                        'url': "https://reserve.cdn-apple.com/DE/de_DE/reserve/iPhone/availability"
                    }
                    update_state(state_id, availability[model], message)


if __name__ == "__main__":
    loop = tornado.ioloop.IOLoop.instance()
    tornado.ioloop.PeriodicCallback(run_crawler, 30000).start()
    loop.start()
