import logging
import multiprocessing as mp
import os
import time

import click
import yaml

from instacart_alerts import instacart
from instacart_alerts.notification import notify

logging.basicConfig(level=logging.DEBUG,
                format='%(asctime)s %(name)-12s %(levelname)-8s %(message)s',
                datefmt='%m-%d %H:%M',
                )

TEXT_FROM = {
    'user': os.environ['TXT_ALERT_ACCT_ID'],
    'password': os.environ['TXT_ALERT_API_KEY'],
    'number': os.environ['TXT_ALTERT_NUMBER'],
}

EMAIL_FROM = {
    'user': os.environ['EMAIL_SENDER'],
    'password': os.environ['EMAIL_SENDER_PASSWORD'],
}


WAIT_TIME = 600

def find_open_times(search_config):
    found = False
    found_locations = []

    while not found:

        for location in search_config['locations']:

            valid_service_options = instacart.service_options_for_location(search_config, location)

            if any(valid_service_options):
                logging.info('{} found NOW, GO GO GO!'.format(location['external']))
                found = True
                found_locations.append(location)

        if found:
            return found_locations
        logging.info('No times available for {}, continue looking in {} seconds'.format(', '.join([l['external'] for l in search_config['locations']]), WAIT_TIME))
        time.sleep(WAIT_TIME)


def work_for_location(loc_config, text_from=TEXT_FROM, email_from=EMAIL_FROM):

    found_wait_time = 14400 # 4 hours
    while True:
        try:
            locations = find_open_times(loc_config['search_info'])
            notify.send_email(
                _from=email_from,
                to=loc_config['users'],
                text_items=loc_config['message'],
                locations=locations,
            )
            notify.send_text(
                _from=text_from,
                to=loc_config['users'],
                text=loc_config['message']['text'],
                locations=locations,
            )
            logging.info('Done looking, waiting an 4 hours')
            time.sleep(found_wait_time)
        except Exception as e:
            logging.exception(e)
            return


@click.command('monitor')
@click.option('--file', '_file', required=True, help='path to config file')
def main(_file):

    config = yaml.load(open(_file))
    alert_config = config['geolocations']

    with mp.Pool(len(config)) as pool:
        pool.map(work_for_location, alert_config)

    logging.info('DONE PROCESSING')


if __name__ == '__main__':
    main()
