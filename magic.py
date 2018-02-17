import datetime
import logging
from threading import Thread
import pymongo
import requests
import pytz
import redis
from fake_useragent import UserAgent
import json


coinMapping = {}
coinMapping["btc"]="Bitcoin"
coinMapping["bch"]="Bitcoin Cash"
coinMapping["xrp"]="Ripple"
coinMapping["eth"]="Ether"
coinMapping["ltc"]="Litecoin"
coinMapping["omg"]="Omisego"
coinMapping["gnt"]="Golem"
coinMapping["miota"]="IOTA"
coinMapping["btc__zebpay"]="Bitcoin  zebpay"
coinMapping["bch__zebpay"]="Bitcoin Cash  zebpay"
coinMapping["ltc__zebpay"]="Litecoin  zebpay"
coinMapping["xrp__zebpay"]="Ripple  zebpay"
coinMapping["btc__unocoin"]="Bitcoin  unocoin"
coinMapping["btc__koinex"]="Bitcoin  koinex"
coinMapping["xrp__koinex"]="Ripple  koinex"
coinMapping["bch__koinex"]="Bitcoin Cash  koinex"
coinMapping["eth__koinex"]="Ether  koinex"
coinMapping["ltc__koinex"]="Litecoin  koinex"
coinMapping["omg__koinex"]="Omisego  koinex"
coinMapping["miota__koinex"]="IOTA  koinex"
coinMapping["gnt__koinex"]="GOLEM  koinex"


apiUrlMapping = {'btc__zebpay': 'https://www.zebapi.com/api/v1/market/ticker-new/btc/inr',
                 'bch__zebpay': 'https://www.zebapi.com/api/v1/market/ticker-new/bch/inr',
                 'ltc__zebpay': 'https://www.zebapi.com/api/v1/market/ticker-new/ltc/inr',
                 'xrp__zebpay': 'https://www.zebapi.com/api/v1/market/ticker-new/xrp/inr',
                  "koinex": "https://koinex.in/api/ticker",
                  "unocoin": "https://www.unocoin.com/api/v1/general/prices"}

zebPayCoins = ["btc", "bch", "ltc", "xrp"]
logging.basicConfig(filename='magic.log', level=logging.DEBUG)
results = {}
openPrice = {}


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
        ua = UserAgent()
        headers = {'User-Agent': str(ua.random)}
        ret = (requests.get(url, headers=headers))
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


def get_mongo_connection():
    client = pymongo.MongoClient()
    db = client.coinExchangeDB
    return db.coinInfo


def do_magic():
    global results
    results = {}
    global openPrice
    openPrice = {}
    results = {"ts": datetime.datetime.now(datetime.timezone.utc)}
    collection = get_mongo_connection()
    get_final_data()
    #print(results)
    idd = collection.insert_one(results).inserted_id
    logging.info(str(idd))
    #pymongo.MongoClient().close()

    get_open_price_data_from_redis()

    ret = transform_res(results)

    #insert open price to coin data
    for coin in ret["coinData"]:
        coin["op"] = openPrice[coin["id"]]

    #store ret to redis
    r = redis.Redis(host='localhost', port=6379, db=0)
    key = "latestCoinData"
    r.set(key, json.dumps(ret))


def transform_res(res):
    res["ts"] = res["ts"].replace(tzinfo=pytz.utc).timestamp()
    ret = {}
    ret["coinData"] = []
    for key, values in res.items():
        if key == "koinex":
            ret["coinData"] = ret["coinData"] + (transform_koinex_data(values["prices"]))
        elif key == "unocoin":
            ret["coinData"].append(transform_unocoin_data(values))
        elif "zebpay" in key:
            ret["coinData"].append(transform_zebpay_data(key, values))

    ret["ts"] = res["ts"]
    return ret


def fill_coin_data(id):
    res = {}
    res["id"] = id
    res["name"] = coinMapping[id]
    res["currency"] = "inr"
    res["op"] = "0.0"
    return res


def transform_koinex_data(res):
    ret = []
    for key, val in res.items():
        tmp = {}
        newkey = (key.lower() + "__koinex")
        tmp = {}
        tmp = fill_coin_data(newkey)
        tmp["cp"] = str(val)
        ret.append(tmp)
    return ret


def transform_unocoin_data(res):
    ret = {}
    ret = fill_coin_data("btc__unocoin")
    ret["cp"] = str(res["buybtc"])
    return ret


def transform_zebpay_data(key, res):
    ret = {}
    ret = fill_coin_data(key)
    ret["cp"] = str(res["buy"])
    return ret


def get_open_price_data_from_redis():
    r = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
    key = "coinsOP"
    global openPrice
    openPrice = r.hgetall(key)


if __name__ == '__main__':
    do_magic()
