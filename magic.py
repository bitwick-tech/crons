import requests
import pymongo
import datetime
import logging


def get_data(com):
    url = ""
    if com == "zebpay":
        url = "https://www.zebapi.com/api/v1/market/ticker/btc/inr"

    r = requests.get(url)
    res = {com: r.json(), "ts": datetime.datetime.now(datetime.timezone.utc)}
    return res


def do_magic():
    # from pymongo import MongoClient
    client = pymongo.MongoClient()
    db = client.coinExchangeDB
    collection = db.coinInfo
    finalData = get_data("zebpay")
    idd = collection.insert_one(finalData).inserted_id
    logging.basicConfig(filename='magic.log', level=logging.DEBUG)
    # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    # logging.info(finalData["ts"])
    logging.info(str(idd))


if __name__ == '__main__':
    doMagic()