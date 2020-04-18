import logging
from pprint import pprint as pp

import requests


DEFAULT_HEADERS = {
    'content-type': 'application/json',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.132 Safari/537.36',
    'x-client-identifier': 'web',
}


def get_inline_delivery_data(all_content):
    logging.debug('checking inline')
    content = all_content.get('container',{})
    modules = content.get('modules',[])
    
    pp(modules)
    delivery_data = [module for module in modules if 'delivery_option_list' in module['id']]
    return delivery_data 

    
def get_checkout_delivery_data(all_content):
    logging.debug('checking checkout')
    pp(all_content.keys())
    return all_content.get('tracking_params', {}).get('delivery_options')


def get_service_options_for_days(days_data):
    all_service_options = []
    for day in days_data:
        for service_options in day.get('options',[]):
            all_service_options.append(service_options.get('option_type'))
    return set(all_service_options)

    
def get_service_options(delivery_data):
    service_options = set()
    for d in delivery_data:
        days_data = d.get('data',{}).get('service_options',{}).get('service_options',{}).get('days',[])
        service_options.update(get_service_options_for_days(days_data))

    return service_options


def service_options_for_location(search_config, location):

    params = search_config['params']
    headers = {**DEFAULT_HEADERS, **search_config['headers']}
    url_template = search_config['url']

    url = url_template.format(store=location['internal'])
    resp = requests.get(url, params=params, headers=headers)
    all_content = resp.json()

    delivery_data = (get_inline_delivery_data(all_content)
                    if search_config['type']== 'inline'
                    else get_checkout_delivery_data(all_content))

    service_options = get_service_options(delivery_data)

    valid_service_options = (service_options
                                if not search_config['delivery_filter']
                                else [s for s in service_options if s not in search_config['delivery_filter']])

    logging.debug('({}) service options. ({}) are valid'.format(','.join(service_options) or 'None', ','.join(valid_service_options) or 'None'))

    return valid_service_options
