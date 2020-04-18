# instacart-alerts

Supply a config file in the shape of the following, after extracting the required Instacart Request info from a vaild session. 

```yaml
geolocations:
  - id: <string location identifier Town, State>
    message:
      link: https://www.instacart.com/store/{store}/info?tab=delivery
      text: Open times available for InstaCart
    search_info:
      delivery_filter:
      - AsapDeliveryOption
      headers:
        cookie: _instacart_session=<session cookie>
        x-csrf-token: <token>
      locations:
      - external: Weggies
        internal: wegmans
      params:
        cache_key: <cache key>
        source: web
      type: inline
      url: https://www.instacart.com/v3/containers/{store}/next_gen/retailer_information/content/delivery
    users:
      - !!python/object:instacart_alerts.notification.notify.Person
        email: <email to>
        name: <User Friendly Name>
        phone: <Text To>
```

## Run with the following

`monitor --file config.py`


## Environment Variables for Sending Notifications

`EMAIL_SENDER` - you@email.com

`EMAIL_SENDER_PASSWORD` - password for you@email.com

`TXT_ALERT_ACCT_ID` - Twilio Acct ID

`TXT_ALERT_API_KEY` - Twilio API Key

`TXT_ALTERT_NUMBER` - Twilio Phone Number
