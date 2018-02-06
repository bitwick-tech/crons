import datetime
import logging
from threading import Thread
import pymongo
import requests

apiUrlMapping = {"zebpay": "https://www.zebapi.com/api/v1/market/ticker/btc/inr",
                  "koinex": "https://koinex.in/api/ticker",
                  "unocoin": "https://www.unocoin.com/api/v1/general/prices"}
logging.basicConfig(filename='magic.log', level=logging.DEBUG)
results = {"ts": datetime.datetime.now(datetime.timezone.utc)}


class GetDataThread(Thread):
    def __init__(self, com):
        self.com = com
        super(GetDataThread, self).__init__()

    def run(self):
        get_data(self.com)


def remove_fields(ret):
    redundantFields = ['buybtc', 'sellbtc', 'min_24_buy', 'max_24_buy']
    newRet = {}
    for r in redundantFields:
        newRet[r] = ret[r]
    return newRet


def get_data(com):
    url = apiUrlMapping[com]
    if com == "unocoin":
        headers = {"Content-Type": "application/json",
                   "Authorization": "Bearer " + "8ee2ac117dfd5ac86e7646841817460eff4e6f44"}
        ret = requests.post(url, headers=headers)
        if ret.status_code != 200:
            return
        ret = ret.json()
        ret = remove_fields(ret)
    else:
        ret = (requests.get(url))
        if ret.status_code != 200:
            return
        ret = ret.json()
    results[com] = ret


def get_final_data():
    threads = []
    for k in apiUrlMapping:
        t = GetDataThread(k)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()
    return results


def get_mongo_connection():
    client = pymongo.MongoClient()
    db = client.coinExchangeDB
    return db.coinInfo


def do_magic():
    collection = get_mongo_connection()
    finalData = get_final_data()
    idd = collection.insert_one(finalData).inserted_id
    logging.info(str(idd))


if __name__ == '__main__':
    do_magic()