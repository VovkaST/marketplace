import os
import time

import environ
import requests

from marketplace.settings import BASE_DIR


def send_card():
    env = environ.Env()
    environ.Env.read_env(os.path.join(BASE_DIR.parent, ".env"))
    s = requests.Session()
    s.headers['Accept'] = 'application/json'
    s.headers['Content-Type'] = 'application/json'
    s.headers['authorization'] = 'Bearer ' + env('QIWI_API_ACCESS_TOKEN')
    postjson = {"id": f"{int(time.time() * 1000)}",
                "sum": {"amount": '10', "currency": "643"},
                "paymentMethod": {"type": "Account", "accountId": "643"},
                "fields": {"account": env('MY_CARD')}}
    prv_id = env('MY_CARD_PRV_ID')
    res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/' + prv_id + '/payments', json=postjson)
    return res.json()