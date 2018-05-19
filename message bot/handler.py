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
NICEHASH_PROVIDER = "stats.provider.payments&addr=<addr>"
COINMAKETCAP_CONV_RATE_URL="https://api.coinmarketcap.com/v2/ticker/1/?convert=EUR"
headers = {'Content-Type': 'application/json'}

COPAY_BALANCE = 0 # ...
COINBASE_BALANCE = 0 # ...

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
    return {
        '/help' : helper(),
        '/balance' : balance(),
        '/detailed_balance' : detailed_balance(),
        '/payments' : payments(),
        '/euro' : euro()
    }.get(message, default())

def default():
    return 'Hello, how are you?\nIf you want to ask me something press /help !'

def helper():
    return "/balance to get the total balance\n/detailed_balance to get the distribution bewteen wallets\n/payments to get the last payments\n/euro to get the balance in EURO"

def balance():
    total = balanceNicehash() + COPAY_BALANCE + COINBASE_BALANCE
    return '%.8f' % total + " BTC"

def detailed_balance():
    response = '%.8f' % balanceNicehash() + " Nicehash\n" + '%.8f' % float(COPAY_BALANCE) + " copay\n" + '%.8f' % float(COINBASE_BALANCE) + " coinbase"
    return response

def payments():
    string = decode(NICEHASH_URL+NICEHASH_PROVIDER, headers)
    if "erreur avec l'API" in string:
        return string
    payments = string["result"]["payments"]
    response = ''
    for day_pay in payments:
        response += day_pay["amount"] + " BTC " + day_pay["time"][:10] + "\n"
    return response

def euro():
    balance_tot = balanceNicehash() + COPAY_BALANCE + COINBASE_BALANCE

    string = decode(COINMAKETCAP_CONV_RATE_URL, headers)
    if "erreur avec l'API" in string:
        return string
    rate = float(string["data"]["quotes"]["EUR"]["price"])

    reponse = balance_tot*rate
    return '%.2f' % reponse + " EUR"

###########################
###### HELPER METHOD ######
###########################

def decode(url, headers):
    request = requests.get(url, headers)
    if request.status_code == 200:
        return json.loads(request.content.decode('utf-8'))
    else:
        return "erreur avec l'API : {}".format(request.status_code)

def balanceNicehash():
    string = decode(NICEHASH_URL+NICEHASH_BALANCE, headers)
    if "erreur avec l'API" in string:
        return string
    balance_confirmed = float(string["result"]["balance_confirmed"]) + float(string["result"]["balance_pending"])

    string2 = decode(NICEHASH_URL+NICEHASH_PROVIDER, headers)
    balance_unconfirmed = 0
    if "erreur avec l'API" in string2:
        return string2
    for balance in string2["result"]["stats"]:
        balance_unconfirmed += float(balance["balance"])

    return balance_confirmed + balance_unconfirmed
