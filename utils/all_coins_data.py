import redis
import json

redis_host = '172.31.22.154'
# redis_host = 'localhost'

exchanges = ["koinex", "unocoin", "zebpay"]
currencies = ["inr"]
coinIds = ["bch", "btc", "ltc", "eth", "xrp", "omg", "miota", "gnt", "req", "zrx", "bat", "ae", "trx", "xlm"]
coinNames = ["Bitcoin Cash", "Bitcoin", "Litecoin", "Ether", "Ripple", "Omisego", "IOTA", "Golem", "Request Network",
             "0x Protocol", "Basic Attention Token", "Aeternity", "TRON", "Stellar"]

coinIdNameMapping = {'bch': 'Bitcoin Cash', 'btc': 'Bitcoin', 'ltc': 'Litecoin', 'eth': 'Ether', 'xrp': 'Ripple',
                     'omg': 'Omisego', 'miota': 'IOTA', 'gnt': 'Golem', 'req': 'Request Network', 'zrx': '0x Protocol',
                     'bat': 'Basic Attention Token', 'ae': 'Aeternity', "trx": "TRON", "xlm": "Stellar"}
coinNameIdMapping = {'Bitcoin Cash': 'bch', 'Bitcoin': 'btc', 'Litecoin': 'ltc', 'Ether': 'eth', 'Ripple': 'xrp',
                     'Omisego': 'omg', 'IOTA': 'miota', 'Golem': 'gnt', 'Request Network': 'req', '0x Protocol': 'zrx',
                     'Basic Attention Token': 'bat', 'Aeternity': 'ae', 'TRON': 'trx', 'Stellar': 'xlm'}

allCoinsData = {'coinsData': [
    {'id': 'bch', 'name': 'Bitcoin Cash', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']}]},
    {'id': 'btc', 'name': 'Bitcoin',
     'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'unocoin', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']}]},
    {'id': 'ltc', 'name': 'Litecoin', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']}]},
    {'id': 'eth', 'name': 'Ether', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']}]},
    {'id': 'xrp', 'name': 'Ripple', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']}]},
    {'id': 'omg', 'name': 'Omisego', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'miota', 'name': 'IOTA', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'gnt', 'name': 'Golem', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'req', 'name': 'Request Network', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'zrx', 'name': '0x Protocol', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'bat', 'name': 'Basic Attention Token', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'ae', 'name': 'Aeternity', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'trx', 'name': 'TRON', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'xlm', 'name': 'Stellar', 'e': [{'eid': 'koinex', 'c': ['inr']}]}
    ]}
allCoinsHash = {'bch': {'name': 'Bitcoin Cash', 'e': {'koinex': ['inr'], 'zebpay': ['inr']}},
                'btc': {'name': 'Bitcoin', 'e': {'koinex': ['inr'], 'unocoin': ['inr'], 'zebpay': ['inr']}},
                'ltc': {'name': 'Litecoin', 'e': {'koinex': ['inr'], 'zebpay': ['inr']}},
                'eth': {'name': 'Ether', 'e': {'koinex': ['inr'], 'zebpay': ['inr']}},
                'xrp': {'name': 'Ripple', 'e': {'koinex': ['inr'], 'zebpay': ['inr']}},
                'omg': {'name': 'Omisego', 'e': {'koinex': ['inr']}},
                'miota': {'name': 'IOTA', 'e': {'koinex': ['inr']}}, 'gnt': {'name': 'Golem', 'e': {'koinex': ['inr']}},
                'req': {'name': 'Request Network', 'e': {'koinex': ['inr']}},
                'zrx': {'name': '0x Protocol', 'e': {'koinex': ['inr']}},
                'bat': {'name': 'Basic Attention Token', 'e': {'koinex': ['inr']}},
                'ae': {'name': 'Aeternity', 'e': {'koinex': ['inr']}},
                'trx': {'name': 'TRON', 'e': {'koinex': ['inr']}},
                'xlm': {'name': 'Stellar', 'e': {'koinex': ['inr']}}
                }


def generate_coinIdNameMapping_and_coinNameIdMapping():
    idNameMapping = {}
    nameIdMapping = {}
    for i, coin in enumerate(coinIds):
        idNameMapping[coin] = coinNames[i]
        nameIdMapping[coinNames[i]] = coin


def add_coins_static_data_to_redis():
    r = redis.Redis(host=redis_host, port=6379, db=0)
    key = "allCoinsStaticDataHash"
    newData = {}
    newData["v"] = 1
    newData["coinsData"] = allCoinsHash
    r.set(key, json.dumps(newData))
    print(json.loads(r.get(key)))


if __name__ == '__main__':
    add_coins_static_data_to_redis()
