Successful test.  stuff on clicksend dashboard copied here

https://dashboard.clicksend.com/home?user_preference=api

```shell
curl -X POST \
  'https://rest.clicksend.com//v3/sms/send' \
  -H 'Authorization: Bearer YOUR_API_TOKEN' \
  -H 'Content-Type: application/json' \
  -d '{
    "messages": [
      {
        "to": "0402022038",
        "body": "Testing, testing, 1, 2, 3"
      }
    ]
  }'
```



Response:

```
{
  "http_code": 200,
  "response_code": "SUCCESS",
  "response_msg": "Messages queued for delivery.",
  "data": {
    "total_price": 0.0792,
    "total_count": 1,
    "queued_count": 1,
    "messages": [
      {
        "direction": "out",
        "date": 1787791884,
        "to": "+61402022038",
        "body": "Testing, testing, 1, 2, 3",
        "from": "+61487074113",
        "schedule": 1787791884,
        "message_id": "1F1A1B16-DC22-6280-9B64-63AE3DFCFD43",
        "message_parts": 1,
        "message_price": "0.0792",
        "from_email": null,
        "list_id": null,
        "custom_string": "",
        "contact_id": null,
        "user_id": 720845,
        "subaccount_id": 823363,
        "is_shared_system_number": true,
        "country": "AU",
        "carrier": "Optus",
        "status": "SUCCESS"
      }
    ],
    "_currency": {
      "currency_name_short": "AUD",
      "currency_prefix_d": "$",
      "currency_prefix_c": "c",
      "currency_name_long": "Australian Dollars"
    },
    "blocked_count": 0
  }
}
```

