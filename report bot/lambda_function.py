import json
#import requests
from botocore.vendored import requests
import time
from time import sleep

#lambda_handler
def lambda_handler(event, context):

    BASE_URL = "https://api.telegram.org/bot{}".format('TELEGRAM_TOKEN')

    # 24H
    timeStamp = int(time.time()-86400)

    # REST API nicehash
    api_url = "https://api.nicehash.com/api?method=stats.provider.ex&addr=<nicehashAddress>&from=" + str(timeStamp)
    headers = {'Content-Type': 'application/json'}

    year, month, day, hour, minute = time.strftime("%Y,%m,%d,%H,%M").split(',')
    message = day+'/'+month+"/"+year+" : "

    # 10 tries to get an answer from nicehash
    for i in range(10):
        response = requests.get(api_url, headers=headers)
        if response.status_code == 200:
            string = json.loads(response.content.decode('utf-8'))

            chat_id = 'CHAT_ID'
            total = 0.0
            for algo in string["result"]["past"]:
                if float(algo["data"][0][2]) < float(algo["data"][len(algo["data"])-1][2]):
                    total += float(algo["data"][len(algo["data"])-1][2]) - float(algo["data"][0][2])
                elif float(algo["data"][0][2]) == float(algo["data"][len(algo["data"])-1][2]):
                    total += float(algo["data"][0][2])
                else:
                    total += float(algo["data"][len(algo["data"])-1][2]) + float(maxBeforePayment(algo["data"])) - float(algo["data"][0][2])

            message += '%.8f' % total + " BTC"
            data = {"text": message.encode("utf8"), "chat_id": chat_id}
            url = BASE_URL + "/sendMessage"

            try:
                # send the message to the telegram channel
                response = requests.post(url, data).content
            except Exception as e:
                return {"statusCode": 302}
            return {"statusCode": 200}
        else:
            sleep(120) # if we get no answer, we sleep during 2 minutes
    return {"statusCode": 302}

def maxBeforePayment(tab):
    a = '0'
    for i in tab:
        if i[2] < a:
            return a
        else:
            a = i[2]
    return a
