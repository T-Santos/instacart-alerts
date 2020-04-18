import logging
import os

from twilio.rest import Client
import yagmail


class Person(object):
    def __init__(self, name, phone=None, email=None):
        self.name = name
        self.phone = phone
        self.email = email


def send_email(_from, to, text_items, locations=None):
    logging.info('Sending Email now')
    link = text_items.get('link','')
    link = '\n'.join([link.format(store=location['internal']) for location in locations]) if (locations and link) else link

    locs = locations if locations else []
    locations_str = ', '.join([l['external'] for l in locs])

    yag = yagmail.SMTP(_from['user'], _from['password'])
    yag.send([p.email for p in to if p.email], 'InstaCart Deliveries Open for {}'.format(locations_str), 'Log into InstaCart.\n {}'.format(link))


def send_text(_from, to, text, locations=None):

    # Your Account Sid and Auth Token from twilio.com/console
    # DANGER! This is insecure. See http://twil.io/secure
    account_sid = _from['user']
    auth_token = _from['password']
    number = _from['number']

    client = Client(account_sid, auth_token)

    locs = locations if locations else []
    locations_str = ', '.join([l['external'] for l in locs])

    body_text = '\n'.join([text, "Locations: {}".format(locations_str)])

    for recipient in [p.phone for p in to if p.phone]:
        client.messages.create(
             body=body_text,
             from_=number,
             to=recipient,
         )
