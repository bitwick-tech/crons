import datetime
import logging
from threading import Thread
import pymongo
import requests
import pytz
import redis
from fake_useragent import UserAgent
import json

redis_host = '172.31.22.154'
# redis_host = 'localhost'

allCoinsData = {'coinsData': [
    {'id': 'bch', 'name': 'Bitcoin Cash', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']},
                                                {'eid': 'coinome', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']}]},
    {'id': 'btc', 'name': 'Bitcoin',
     'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'unocoin', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']},
           {'eid': 'coinome', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']}]},
    {'id': 'ltc', 'name': 'Litecoin', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']},
                                            {'eid': 'coinome', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']}]},
    {'id': 'eth', 'name': 'Ether', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']},
                                         {'eid': 'coindelta', 'c': ['inr']}]},
    {'id': 'xrp', 'name': 'Ripple', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']},
                                          {'eid': 'coindelta', 'c': ['inr']}]},
    {'id': 'omg', 'name': 'Omisego', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']}]},
    {'id': 'miota', 'name': 'IOTA', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'gnt', 'name': 'Golem', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'req', 'name': 'Request Network', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'zrx', 'name': '0x Protocol', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']}]},
    {'id': 'bat', 'name': 'Basic Attention Token', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'ae', 'name': 'Aeternity', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'trx', 'name': 'TRON', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'xlm', 'name': 'Stellar', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'eos', 'name': 'EOS', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']}]},
    {'id': 'neo', 'name': 'NEO', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'gas', 'name': 'GAS', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'aion', 'name': 'AION', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'ncash', 'name': 'Nucleus Vision', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'xrb', 'name': 'Nano', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'dash', 'name': 'DASH', 'e': [{'eid': 'coinome', 'c': ['inr']}]},
    {'id': 'dgb', 'name': 'DigiByte', 'e': [{'eid': 'coinome', 'c': ['inr']}]},
    {'id': 'zec', 'name': 'ZCash', 'e': [{'eid': 'coinome', 'c': ['inr']}]},
    {'id': 'qtum', 'name': 'Qtum', 'e': [{'eid': 'coinome', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']}]},
    {'id': 'btg', 'name': 'Bitcoin Gold', 'e': [{'eid': 'coinome', 'c': ['inr']}]},
    {'id': 'zil', 'name': 'Zilliqa', 'e': [{'eid': 'coindelta', 'c': ['inr']}]},
    {'id': 'knc', 'name': 'Kyber Network', 'e': [{'eid': 'coindelta', 'c': ['inr']}]}
    ]}
allCoinsHash = {'bch': {'name': 'Bitcoin Cash', 'e': {'koinex': ['inr'], 'zebpay': ['inr'], 'coinome': ['inr'],
                                                      'coindelta': ['inr']}},
                'btc': {'name': 'Bitcoin', 'e': {'koinex': ['inr'], 'unocoin': ['inr'], 'zebpay': ['inr'],
                                                 'coinome': ['inr'], 'coindelta': ['inr']}},
                'ltc': {'name': 'Litecoin', 'e': {'koinex': ['inr'], 'zebpay': ['inr'], 'coinome': ['inr'],
                                                  'coindelta': ['inr']}},
                'eth': {'name': 'Ether', 'e': {'koinex': ['inr'], 'zebpay': ['inr'], 'coindelta': ['inr']}},
                'xrp': {'name': 'Ripple', 'e': {'koinex': ['inr'], 'zebpay': ['inr'], 'coindelta': ['inr']}},
                'omg': {'name': 'Omisego', 'e': {'koinex': ['inr'], 'coindelta': ['inr']}},
                'miota': {'name': 'IOTA', 'e': {'koinex': ['inr']}},
                'gnt': {'name': 'Golem', 'e': {'koinex': ['inr']}},
                'req': {'name': 'Request Network', 'e': {'koinex': ['inr']}},
                'zrx': {'name': '0x Protocol', 'e': {'koinex': ['inr'], 'coindelta': ['inr']}},
                'bat': {'name': 'Basic Attention Token', 'e': {'koinex': ['inr']}},
                'ae': {'name': 'Aeternity', 'e': {'koinex': ['inr']}},
                'trx': {'name': 'TRON', 'e': {'koinex': ['inr']}},
                'xlm': {'name': 'Stellar', 'e': {'koinex': ['inr']}},
                'eos': {'name': 'EOS', 'e': {'koinex': ['inr'], 'coindelta': ['inr']}},
                'neo': {'name': 'NEO', 'e': {'koinex': ['inr']}},
                'gas': {'name': 'GAS', 'e': {'koinex': ['inr']}},
                'aion': {'name': 'AION', 'e': {'koinex': ['inr']}},
                'ncash': {'name': 'Nucleus Vision', 'e': {'koinex': ['inr']}},
                'xrb': {'name': 'Nano', 'e': {'koinex': ['inr']}},
                'dash': {'name': 'DASH', 'e': {'coinome': ['inr']}},
                'dgb': {'name': 'DigiByte', 'e': {'coinome': ['inr']}},
                'zec': {'name': 'ZCash', 'e': {'coinome': ['inr']}},
                'qtum': {'name': 'Qtum', 'e': {'coinome': ['inr'], 'coindelta': ['inr']}},
                'btg': {'name': 'Bitcoin Gold', 'e': {'coinome': ['inr']}},
                'zil': {'name': 'Zilliqa', 'e': {'coindelta': ['inr']}},
                'knc': {'name': 'Kyber Network', 'e': {'coindelta': ['inr']}}
                }

coinMapping = {'btc': 'Bitcoin', 'bch': 'Bitcoin Cash', 'xrp': 'Ripple', 'eth': 'Ether', 'ltc': 'Litecoin',
               'omg': 'Omisego', 'gnt': 'Golem', 'miota': 'IOTA', 'req': 'Request Network',
                'btc__zebpay': 'Bitcoin  zebpay', 'bch__zebpay': 'Bitcoin Cash  zebpay',
               'ltc__zebpay': 'Litecoin  zebpay',
               'xrp__zebpay': 'Ripple  zebpay', 'eth__zebpay': 'Ether  zebpay',
               'btc__unocoin': 'Bitcoin  unocoin', 'btc__koinex': 'Bitcoin  koinex', 'xrp__koinex': 'Ripple  koinex',
               'bch__koinex': 'Bitcoin Cash  koinex', 'eth__koinex': 'Ether  koinex',
               'ltc__koinex': 'Litecoin  koinex', 'omg__koinex': 'Omisego  koinex', 'miota__koinex': 'IOTA  koinex',
               'gnt__koinex': 'GOLEM  koinex', 'req__koinex': 'Request Network koinex',
               'zrx__koinex': '0x Protocol koinex', 'bat__koinex': "Basic Attention Token", 'ae__koinex': "Aeternity",
               'trx__koinex': 'TRON', "xlm": 'Stellar',
               'eos__koinex': 'EOS', 'neo__koinex': 'NEO', 'gas__koinex': 'GAS', 'aion__koinex': 'AION',
               'ncash__koinex': 'Nucleus Vision', 'xrb__koinex': 'Nano',
                'btc__coinome': 'Bitcoin  coinome', 'btg__coinome': 'Bitcoin Gold  coinome',
               'bch__coinome': 'Bitcoin Cash  coinome', 'dash__coinome': 'DASH  coinome',
               'ltc__coinome': 'Litecoin  coinome', 'dgb__coinome': 'DigiByte  coinome',
               'zec__coinome': 'ZCash  coinome', 'qtum__coinome': 'Qtum  coinome',
                'btc__coindelta': 'Bitcoin coindelta', 'bch__coindelta': 'Bitcoin Cash coindelta',
               'xrp__coindelta': 'Ripple coindelta', 'eth__coindelta': 'Ether coindelta',
               'omg__coindelta': 'Omisego coindelta', 'ltc__coindelta': 'Litecoin coindelta',
               'qtum__coindelta': 'Qtum coindelta', 'zil__coindelta': 'Zilliqa coindelta',
               'zrx__coindelta': '0x Protocol coindelta', 'knc__coindelta': 'Kyber Network coindelta',
               'eos__coindelta': 'EOS coindelta'
               }

apiUrlMapping = {'btc__zebpay': 'https://www.zebapi.com/api/v1/market/ticker-new/btc/inr',
                 'bch__zebpay': 'https://www.zebapi.com/api/v1/market/ticker-new/bch/inr',
                 'ltc__zebpay': 'https://www.zebapi.com/api/v1/market/ticker-new/ltc/inr',
                 'xrp__zebpay': 'https://www.zebapi.com/api/v1/market/ticker-new/xrp/inr',
                 'eth__zebpay': 'https://www.zebapi.com/api/v1/market/ticker-new/eth/inr',
                 'koinex': 'https://koinex.in/api/ticker',
                  'unocoin': 'https://www.unocoin.com/api/v1/general/prices',
                 'coinome': 'https://www.coinome.com/api/v1/ticker.json',
                 'coindelta': 'https://coindelta.com/api/v1/public/getticker/'
                 }

zebPayCoins = ["btc", "bch", "ltc", "xrp", "eth"]
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
        print(coin)
        if coin["id"] in openPrice:
            coin["op"] = openPrice[coin["id"]]
    #store ret to redis
    r = redis.Redis(host=redis_host, port=6379, db=0)
    key2 = "latestCoinData"
    r.set(key2, json.dumps(ret))

    ret2 = get_price_data_v1(ret["coinData"])
    pipe = r.pipeline()
    for key, coin in ret2.items():
        pipe.set(key, json.dumps(coin))
    pipe.execute()


def get_price_data_v1(ret):
    result = {}
    for coin in ret:
        tmp = {}
        tmp['cp'] = coin['cp']
        tmp['op'] = coin['op']
        result[coin['id'] + "__" + coin['currency']] = tmp
    return result


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
        elif "coinome" in key:
            ret["coinData"] = ret["coinData"] + (transform_coinome_data(values))
        elif "coindelta" in key:
            ret["coinData"] = ret["coinData"] + (transform_coindelta_data(values))

    ret["ts"] = res["ts"]
    return ret


def fill_coin_data(id):
    res = {}
    res["id"] = id
    if id in coinMapping:
        res["name"] = coinMapping[id]
    res["currency"] = "inr"
    res["op"] = "0.0"
    return res


def transform_koinex_data(res):
    ret = []
    for key, val in res.items():
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


def transform_coinome_data(res):
    ret = []
    for key, val in res.items():
        newkey = (key.lower().split('-')[0] + "__coinome")
        tmp = {}
        tmp = fill_coin_data(newkey)
        tmp['currency'] = key.lower().split('-')[1]
        tmp["cp"] = str(val['last'])
        ret.append(tmp)
    return ret


def transform_coindelta_data(res):
    ret = []
    for key in res:
        newkey = (key["MarketName"].lower().split('-')[0] + "__coindelta")
        tmp = {}
        tmp = fill_coin_data(newkey)
        tmp['currency'] = key["MarketName"].lower().split('-')[1]
        tmp["cp"] = str(key["Last"])
        ret.append(tmp)
    return ret


def get_open_price_data_from_redis():
    r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)
    key = "coinsOP"
    global openPrice
    openPrice = r.hgetall(key)


if __name__ == '__main__':
    do_magic()
