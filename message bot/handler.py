import json
import os
import sys
import time
here = os.path.dirname(os.path.realpath(__file__))
sys.path.append(os.path.join(here, "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

# REST API nicehash
NICEHASH_URL = "https://api.nicehash.com/api?method="
NICEHASH_BALANCE = "balance&id=<id>&key=<key>"
NICEHASH_PAYMENTS = "stats.provider.payments&addr=<addr>"
headers = {'Content-Type': 'application/json'}

COPAY_BALANCE = #...
COINBASE_BALANCE = #...

def hello(event, context):

    try:
        data = json.loads(event["body"])
        message = str(data["message"]["text"])
        chat_id = data["message"]["chat"]["id"]
        first_name = data["message"]["chat"]["first_name"]

        response = commandHandler(message)

        data = {"text": response.encode("utf8"), "chat_id": chat_id}
        url = BASE_URL + "/sendMessage"
        requests.post(url, data)

    except Exception as e:
        print(e)

    return {"statusCode": 200}

def commandHandler(message):
    if "/help" == message:
        return "/hello to say hi\n/balance to get the total balance\n/detailed_balance to get the distribution bewteen wallets\n/payments to get the last payments"
    if "/hello" == message:
        return "Hello {}".format(first_name)
    if "/balance" == message:
        balance = requests.get(NICEHASH_URL+NICEHASH_BALANCE, headers=headers)
        if balance.status_code == 200:
            string = json.loads(balance.content.decode('utf-8'))
            balance_nicehash = float(string["result"]["balance_confirmed"]) + float(string["result"]["balance_pending"])
            total = balance_nicehash + COPAY_BALANCE + COINBASE_BALANCE
            return '%.8f' % total + " BTC"
        else:
            return "erreur avec l'API nicehash"
    if "/detailed_balance" == message:
        balance = requests.get(NICEHASH_URL+NICEHASH_BALANCE, headers=headers)
        if balance.status_code == 200:
            string = json.loads(balance.content.decode('utf-8'))
            balance_nicehash = float(string["result"]["balance_confirmed"]) + float(string["result"]["balance_pending"])
            response = '%.8f' % balance_nicehash + " Nicehash\n" + '%.8f' % float(COPAY_BALANCE) + " copay\n" + '%.8f' % float(COINBASE_BALANCE) + " coinbase"
            return response
        else:
            return "erreur avec l'API nicehash"
    if "/payments" == message:
        payments = requests.get(NICEHASH_URL+NICEHASH_PAYMENTS, headers=headers)
        if payments.status_code == 200:
            string = json.loads(payments.content.decode('utf-8'))
            payments = string["result"]["payments"]
            response = ''
            for day_pay in payments:
                day = time.strftime("%d/%m/%y", time.localtime(int(day_pay["time"])))
                response += day_pay["amount"] + " BTC " + day + "\n"
            return response
        else:
            return "erreur avec l'API nicehash"
