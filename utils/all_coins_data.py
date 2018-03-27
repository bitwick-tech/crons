import redis
import json

redis_host = '172.31.22.154'
# redis_host = 'localhost'

exchanges = ["koinex", "unocoin", "zebpay", "coinome", "coindelta"]
currencies = ["inr"]
coinIds = ["bch", "btc", "ltc", "eth", "xrp", "omg", "miota", "gnt", "req", "zrx", "bat", "ae", "trx", "xlm", "eos",
           "neo", "gas", "aion", "ncash", "xrb", 'dash', 'dgb', 'zec', 'qtum', 'btg', 'zil', 'knc']
coinNames = ["Bitcoin Cash", "Bitcoin", "Litecoin", "Ether", "Ripple", "Omisego", "IOTA", "Golem", "Request Network",
             "0x Protocol", "Basic Attention Token", "Aeternity", "TRON", "Stellar", "EOS", "NEO", "GAS", "AION",
             "Nucleus Vision", "Nano", "DASH", "dgb", "ZCash", "Qtum", "Bitcoin Gold", "Zilliqa", "Kyber Network"]

coinIdNameMapping = {'bch': 'Bitcoin Cash', 'btc': 'Bitcoin', 'ltc': 'Litecoin', 'eth': 'Ether', 'xrp': 'Ripple',
                     'omg': 'Omisego', 'miota': 'IOTA', 'gnt': 'Golem', 'req': 'Request Network', 'zrx': '0x Protocol',
                     'bat': 'Basic Attention Token', 'ae': 'Aeternity', "trx": "TRON", "xlm": "Stellar", 'eos': 'EOS',
                     'neo': 'NEO', 'gas': 'GAS', 'aion': 'AION', 'ncash': 'Nucleus Vision', 'xrb': 'Nano',
                     'dash': 'DASH', 'dgb': 'DigiByte', 'zec': "ZCash", 'qtum': "Qtum", "btg": "Bitcoin Gold",
                     'zil': 'Zilliqa', 'knc': 'Kyber Network'
                     }
coinNameIdMapping = {'Bitcoin Cash': 'bch', 'Bitcoin': 'btc', 'Litecoin': 'ltc', 'Ether': 'eth', 'Ripple': 'xrp',
                     'Omisego': 'omg', 'IOTA': 'miota', 'Golem': 'gnt', 'Request Network': 'req', '0x Protocol': 'zrx',
                     'Basic Attention Token': 'bat', 'Aeternity': 'ae', 'TRON': 'trx', 'Stellar': 'xlm',
                     'EOS': 'eos',
                     'NEO': 'neo', 'GAS': 'gas', 'AION': 'aion', 'Nucleus Vision': 'ncash', 'Nano': 'xrb',
                     'DASH': 'dash', 'DigiByte': 'dgb', 'ZCash': 'zec', 'Qtum': 'qtum', 'Bitcoin Gold': 'btg',
                     'Zilliqa': 'zil', 'Kyber Network': 'knc'
                     }

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
    newData["v"] = 4
    newData["coinsData"] = allCoinsHash
    r.set(key, json.dumps(newData))
    print(json.loads(r.get(key)))


if __name__ == '__main__':
    add_coins_static_data_to_redis()
