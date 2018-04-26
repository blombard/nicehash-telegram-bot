import json
import os
import sys
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

# REST API nicehash
NICEHASH_URL = "https://api.nicehash.com/api?method=balance&id=<id>&key=<key>"
headers = {'Content-Type': 'application/json'}

COPAY_BALANCE = #...
COINBASE_BALANCE = #...

def hello(event, context):

    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]

        if "/help" == message:
            response = "/start to say hi \n/balance to get the total balance \n/detailed_balance to get the distribution bewteen wallets"
        if "/start" == message:
            response = "Hello {}".format(first_name)
        if "/balance" == message:
            balance = requests.get(NICEHASH_URL, headers=headers)
            if balance.status_code == 200:
                string = json.loads(balance.content.decode('utf-8'))
                balance_nicehash = float(string["result"]["balance_confirmed"]) + float(string["result"]["balance_pending"])
                total = balance_nicehash + COPAY_BALANCE + COINBASE_BALANCE
                response = '%.8f' % total + " BTC"
            else:
                response = "Nicehash API error"
        if "/detailed_balance" == message:
            balance = requests.get(NICEHASH_URL, headers=headers)
            if balance.status_code == 200:
                string = json.loads(balance.content.decode('utf-8'))
                balance_nicehash = float(string["result"]["balance_confirmed"]) + float(string["result"]["balance_pending"])
                response = '%.8f' % balance_nicehash + " Nicehash\n" + '%.8f' % float(COPAY_BALANCE) + " copay\n" + '%.8f' % float(COINBASE_BALANCE) + " coinbase"
            else:
                response = "Nicehash API error"

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

    except Exception as e:
        print(e)

    return {"statusCode": 200}
