import redis
import json

redis_host = '172.31.22.154'
# redis_host = 'localhost'

exchanges = ["koinex", "unocoin", "zebpay", "coinome", "coindelta", "bitbns", "buyucoin"]

currencies = ["inr"]

coinIds = ["bch", "btc", "ltc", "eth", "xrp", "omg", "miota", "gnt", "req", "zrx", "bat", "ae", "trx", "xlm", "eos",
           "neo", "gas", "aion", "ncash", "xrb", 'dash', 'dgb', 'zec', 'qtum', 'btg', 'zil', 'knc', 
           'rpx', 'dbc', 'xmr', 'doge', 'sc', 'etn', 'ont', 'poly', 'ada', 'icx', 'ven', 'ark', 'bts', 'cloak', 'cvc',
           'dcn', 'etc', 'fct', 'lsk', 'nxt', 'pay', 'pivx', 'rep', 'steem', 'strat', 'xem'
           ]

coinNames = ["Bitcoin Cash", "Bitcoin", "Litecoin", "Ether", "Ripple", "Omisego", "IOTA", "Golem", "Request Network",
             "0x Protocol", "Basic Attention Token", "Aeternity", "TRON", "Stellar", "EOS", "NEO", "GAS", "AION",
             "Nucleus Vision", "Nano", "DASH", "dgb", "ZCash", "Qtum", "Bitcoin Gold", "Zilliqa", "Kyber Network",
             'Red Pulse', 'DeepBrain Chain', 'Monero', 'Dogecoin', 'Siacoin', 'Electroneum', 'Ontology', 'Polymath',
             'Cardano', 'ICON', 'VeChain', 'Ark', 'BitShares', 'CloakCoin', 'Civic', 'Dentacoin', 'Ethereum Classic',
             'Factom', 'Lisk', 'Nxt', 'TenX', 'PIVX', 'Augur', 'Steem', 'Stratis', 'NEM'
             ]

coinIdNameMapping = {'bch': 'Bitcoin Cash', 'btc': 'Bitcoin', 'ltc': 'Litecoin', 'eth': 'Ether', 'xrp': 'Ripple',
                     'omg': 'Omisego', 'miota': 'IOTA', 'gnt': 'Golem', 'req': 'Request Network', 'zrx': '0x Protocol',
                     'bat': 'Basic Attention Token', 'ae': 'Aeternity', "trx": "TRON", "xlm": "Stellar", 'eos': 'EOS',
                     'neo': 'NEO', 'gas': 'GAS', 'aion': 'AION', 'ncash': 'Nucleus Vision', 'xrb': 'Nano',
                     'dash': 'DASH', 'dgb': 'DigiByte', 'zec': "ZCash", 'qtum': "Qtum", "btg": "Bitcoin Gold",
                     'zil': 'Zilliqa', 'knc': 'Kyber Network', 'rpx': 'Red Pulse', 'dbc': 'DeepBrain Chain', 
                     'xmr': 'Monero', 'doge': 'Dogecoin', 'sc': 'Siacoin', 'etn': 'Electroneum', 'ont': 'Ontology', 
                     'poly': 'Polymath', 'ada': 'Cardano', 'icx': 'ICON', 'ven': 'VeChain', 'ark': 'Ark',
                     'bts': 'BitShares', 'cloak': 'CloakCoin', 'cvc': 'Civic', 'dcn': 'Dentacoin',
                     'etc': 'Ethereum Classic', 'fct': 'Factom', 'lsk': 'Lisk', 'nxt': 'Nxt', 'pay': 'TenX',
                     'pivx': 'PIVX', 'rep': 'Augur', 'steem': 'Steem', 'strat': 'Stratis', 'xem': 'NEM'
                     }

coinNameIdMapping = {'Bitcoin Cash': 'bch', 'Bitcoin': 'btc', 'Litecoin': 'ltc', 'Ether': 'eth', 'Ripple': 'xrp',
                     'Omisego': 'omg', 'IOTA': 'miota', 'Golem': 'gnt', 'Request Network': 'req', '0x Protocol': 'zrx',
                     'Basic Attention Token': 'bat', 'Aeternity': 'ae', 'TRON': 'trx', 'Stellar': 'xlm',
                     'EOS': 'eos', 'NEO': 'neo', 'GAS': 'gas', 'AION': 'aion', 'Nucleus Vision': 'ncash', 'Nano': 'xrb',
                     'DASH': 'dash', 'DigiByte': 'dgb', 'ZCash': 'zec', 'Qtum': 'qtum', 'Bitcoin Gold': 'btg',
                     'Zilliqa': 'zil', 'Kyber Network': 'knc', 'Red Pulse': 'rpx', 'DeepBrain Chain': 'dbc', 
                     'Monero': 'xmr', 'Dogecoin': 'doge', 'Siacoin': 'sc', 'Electroneum': 'etn', 'Ontology': 'ont', 
                     'Polymath': 'poly', 'Cardano': 'ada', 'ICON': 'icx', 'VeChain': 'ven', 'Ark': 'ark',
                     'BitShares': 'bts', 'CloakCoin': 'cloak', 'Civic': 'cvc', 'Dentacoin': 'dcn',
                     'Ethereum Classic': 'etc', 'Factom': 'fct', 'Lisk': 'lsk', 'Nxt': 'nxt', 'TenX': 'pay',
                     'PIVX': 'pivx', 'Augur': 'rep', 'Steem': 'steem', 'Stratis': 'strat', 'NEM': 'xem'
                     }

allCoinsData = {'coinsData': [
    {'id': 'bch', 'name': 'Bitcoin Cash', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']},
                                                {'eid': 'coinome', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']},
                                                {'eid': 'bitbns', 'c': ['inr']}, {'eid': 'buyucoin', 'c': ['inr']},
                                                {'eid': 'wazirx', 'c': ['inr']}]},
    {'id': 'btc', 'name': 'Bitcoin',
     'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'unocoin', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']},
           {'eid': 'coinome', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']},
           {'eid': 'buyucoin', 'c': ['inr']}, {'eid': 'wazirx', 'c': ['inr']}]},
    {'id': 'ltc', 'name': 'Litecoin', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']},
                                            {'eid': 'coinome', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']},
                                            {'eid': 'bitbns', 'c': ['inr']}, {'eid': 'buyucoin', 'c': ['inr']},
                                            {'eid': 'wazirx', 'c': ['inr']}]},
    {'id': 'eth', 'name': 'Ether', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']},
                                         {'eid': 'coindelta', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']},
                                         {'eid': 'buyucoin', 'c': ['inr']}, {'eid': 'wazirx', 'c': ['inr']}]},
    {'id': 'xrp', 'name': 'Ripple', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']},
                                          {'eid': 'coindelta', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']},
                                          {'eid': 'buyucoin', 'c': ['inr']}, {'eid': 'wazirx', 'c': ['inr']}]},
    {'id': 'omg', 'name': 'Omisego', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']}, 
                                            {'eid': 'bitbns', 'c': ['inr']}, {'eid': 'buyucoin', 'c': ['inr']},
                                           {'eid': 'zebpay', 'c': ['inr']}]},
    {'id': 'miota', 'name': 'IOTA', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'gnt', 'name': 'Golem', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'buyucoin', 'c': ['inr']},
                                         {'eid': 'zebpay', 'c': ['inr']}]},
    {'id': 'req', 'name': 'Request Network', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']}]},
    {'id': 'zrx', 'name': '0x Protocol', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']}]},
    {'id': 'bat', 'name': 'Basic Attention Token', 'e': [{'eid': 'koinex', 'c': ['inr']},
                                                         {'eid': 'buyucoin', 'c': ['inr']},
                                                         {'eid': 'wazirx', 'c': ['inr']}
                                                         ]},
    {'id': 'ae', 'name': 'Aeternity', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'trx', 'name': 'TRON', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']},
                                        {'eid': 'wazirx', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']}]},
    {'id': 'xlm', 'name': 'Stellar', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']}]},
    {'id': 'eos', 'name': 'EOS', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']},
                                       {'eid': 'bitbns', 'c': ['inr']}, {'eid': 'zebpay', 'c': ['inr']},
                                       {'eid': 'wazirx', 'c': ['inr']}]},
    {'id': 'neo', 'name': 'NEO', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']},
                                       {'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'gas', 'name': 'GAS', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']}]},
    {'id': 'aion', 'name': 'AION', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'ncash', 'name': 'Nucleus Vision', 'e': [{'eid': 'koinex', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']}]},
    {'id': 'xrb', 'name': 'Nano', 'e': [{'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'dash', 'name': 'DASH', 'e': [{'eid': 'coinome', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']},
                                         {'eid': 'buyucoin', 'c': ['inr']}, {'eid': 'wazirx', 'c': ['inr']}]},
    {'id': 'dgb', 'name': 'DigiByte', 'e': [{'eid': 'coinome', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']},
                                            {'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'zec', 'name': 'ZCash', 'e': [{'eid': 'coinome', 'c': ['inr']}, {'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'qtum', 'name': 'Qtum', 'e': [{'eid': 'coinome', 'c': ['inr']}, {'eid': 'coindelta', 'c': ['inr']},
                                         {'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'btg', 'name': 'Bitcoin Gold', 'e': [{'eid': 'coinome', 'c': ['inr']}]},
    {'id': 'zil', 'name': 'Zilliqa', 'e': [{'eid': 'coindelta', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']},
                                           {'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'knc', 'name': 'Kyber Network', 'e': [{'eid': 'coindelta', 'c': ['inr']}]},
    {'id': 'rpx', 'name': 'Red Pulse', 'e': [{'eid': 'bitbns', 'c': ['inr']}]}, 
    {'id': 'dbc', 'name': 'DeepBrain Chain', 'e': [{'eid': 'bitbns', 'c': ['inr']}]}, 
    {'id': 'xmr', 'name': 'Monero', 'e': [{'eid': 'bitbns', 'c': ['inr']}, {'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'doge', 'name': 'Dogecoin', 'e': [{'eid': 'bitbns', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']},
                                             {'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'sc', 'name': 'Siacoin', 'e': [{'eid': 'bitbns', 'c': ['inr']}, {'eid': 'bitbns', 'c': ['inr']},
                                          {'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'etn', 'name': 'Electroneum', 'e': [{'eid': 'bitbns', 'c': ['inr']}]}, 
    {'id': 'ont', 'name': 'Ontology', 'e': [{'eid': 'bitbns', 'c': ['inr']}, {'eid': 'koinex', 'c': ['inr']}]},
    {'id': 'poly', 'name': 'Polymath', 'e': [{'eid': 'bitbns', 'c': ['inr']}]}, 
    {'id': 'ada', 'name': 'Cardano', 'e': [{'eid': 'bitbns', 'c': ['inr']}]}, 
    {'id': 'icx', 'name': 'ICON', 'e': [{'eid': 'bitbns', 'c': ['inr']}]}, 
    {'id': 'ven', 'name': 'VeChain', 'e': [{'eid': 'bitbns', 'c': ['inr']}]},
    {'id': 'ark', 'name': 'Ark', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'bts', 'name': 'BitShares', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'cloak', 'name': 'CloakCoin', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'cvc', 'name': 'Civic', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'dcn', 'name': 'Dentacoin', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'etc', 'name': 'Ethereum Classic', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'fct', 'name': 'Factom', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'lsk', 'name': 'Lisk', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'nxt', 'name': 'Nxt', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'pay', 'name': 'TenX', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'pivx', 'name': 'PIVX', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'rep', 'name': 'Augur', 'e': [{'eid': 'buyucoin', 'c': ['inr']}, {'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'steem', 'name': 'Steem', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'strat', 'name': 'Stratis', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]},
    {'id': 'xem', 'name': 'NEM', 'e': [{'eid': 'buyucoin', 'c': ['inr']}]}
    ]}
allCoinsHash = {'bch': {'name': 'Bitcoin Cash', 'e': {'koinex': ['inr'], 'zebpay': ['inr'], 'coinome': ['inr'],
                                                      'coindelta': ['inr'], 'bitbns': ['inr'], 'buyucoin': ['inr'],
                                                      'wazirx': ['inr']}},
                'btc': {'name': 'Bitcoin', 'e': {'koinex': ['inr'], 'unocoin': ['inr'], 'zebpay': ['inr'],
                                                 'coinome': ['inr'], 'coindelta': ['inr'], 'bitbns': ['inr'],
                                                 'buyucoin': ['inr'], 'wazirx': ['inr']}},
                'ltc': {'name': 'Litecoin', 'e': {'koinex': ['inr'], 'zebpay': ['inr'], 'coinome': ['inr'],
                                                  'coindelta': ['inr'], 'bitbns': ['inr'],
                                                  'buyucoin': ['inr'], 'wazirx': ['inr']}},
                'eth': {'name': 'Ether', 'e': {'koinex': ['inr'], 'zebpay': ['inr'], 'coindelta': ['inr'],
                                               'bitbns': ['inr'], 'buyucoin': ['inr'], 'wazirx': ['inr']}},
                'xrp': {'name': 'Ripple', 'e': {'koinex': ['inr'], 'zebpay': ['inr'], 'coindelta': ['inr'],
                                                'bitbns': ['inr'], 'buyucoin': ['inr'], 'wazirx': ['inr']}},
                'omg': {'name': 'Omisego', 'e': {'koinex': ['inr'], 'coindelta': ['inr'], 'bitbns': ['inr'],
                                                 'buyucoin': ['inr'], 'zebpay': ['inr']}},
                'miota': {'name': 'IOTA', 'e': {'koinex': ['inr']}},
                'gnt': {'name': 'Golem', 'e': {'koinex': ['inr'], 'buyucoin': ['inr'], 'zebpay': ['inr']}},
                'req': {'name': 'Request Network', 'e': {'koinex': ['inr'], 'bitbns': ['inr']}},
                'zrx': {'name': '0x Protocol', 'e': {'koinex': ['inr'], 'coindelta': ['inr']}},
                'bat': {'name': 'Basic Attention Token', 'e': {'koinex': ['inr'], 'buyucoin': ['inr'],
                                                               'wazirx': ['inr']}},
                'ae': {'name': 'Aeternity', 'e': {'koinex': ['inr']}},
                'trx': {'name': 'TRON', 'e': {'koinex': ['inr'], 'bitbns': ['inr'], 'wazirx': ['inr'],
                                              'zebpay': ['inr']}},
                'xlm': {'name': 'Stellar', 'e': {'koinex': ['inr'], 'bitbns': ['inr']}},
                'eos': {'name': 'EOS', 'e': {'koinex': ['inr'], 'coindelta': ['inr'], 'bitbns': ['inr'],
                                             'zebpay': ['inr'], 'wazirx': ['inr']}},
                'neo': {'name': 'NEO', 'e': {'koinex': ['inr'], 'bitbns': ['inr'], 'buyucoin': ['inr']}},
                'gas': {'name': 'GAS', 'e': {'koinex': ['inr'], 'bitbns': ['inr']}},
                'aion': {'name': 'AION', 'e': {'koinex': ['inr']}},
                'ncash': {'name': 'Nucleus Vision', 'e': {'koinex': ['inr'], 'bitbns': ['inr']}},
                'xrb': {'name': 'Nano', 'e': {'koinex': ['inr']}},
                'dash': {'name': 'DASH', 'e': {'coinome': ['inr'], 'bitbns': ['inr'], 'buyucoin': ['inr'],
                                               'wazirx': ['inr']}},
                'dgb': {'name': 'DigiByte', 'e': {'coinome': ['inr'], 'bitbns': ['inr'], 'buyucoin': ['inr']}},
                'zec': {'name': 'ZCash', 'e': {'coinome': ['inr'], 'buyucoin': ['inr']}},
                'qtum': {'name': 'Qtum', 'e': {'coinome': ['inr'], 'coindelta': ['inr'], 'buyucoin': ['inr']}},
                'btg': {'name': 'Bitcoin Gold', 'e': {'coinome': ['inr']}},
                'zil': {'name': 'Zilliqa', 'e': {'coindelta': ['inr'], 'bitbns': ['inr'], 'koinex': ['inr']}},
                'knc': {'name': 'Kyber Network', 'e': {'coindelta': ['inr']}},
                'rpx': {'name': 'Red Pulse', 'e': {'bitbns': ['inr']}}, 
                'dbc': {'name': 'DeepBrain Chain', 'e': {'bitbns': ['inr']}}, 
                'xmr': {'name': 'Monero', 'e': {'bitbns': ['inr'], 'buyucoin': ['inr']}},
                'doge': {'name': 'Dogecoin', 'e': {'bitbns': ['inr'], 'buyucoin': ['inr']}},
                'sc': {'name': 'Siacoin', 'e': {'bitbns': ['inr'], 'buyucoin': ['inr']}},
                'etn': {'name': 'Electroneum', 'e': {'bitbns': ['inr']}}, 
                'ont': {'name': 'Ontology', 'e': {'bitbns': ['inr'], 'koinex': ['inr']}},
                'poly': {'name': 'Polymath', 'e': {'bitbns': ['inr']}}, 
                'ada': {'name': 'Cardano', 'e': {'bitbns': ['inr']}}, 
                'icx': {'name': 'ICON', 'e': {'bitbns': ['inr']}}, 
                'ven': {'name': 'VeChain', 'e': {'bitbns': ['inr']}},
                'ark': {'name': 'Ark', 'e': {'buyucoin': ['inr']}},
                'bts': {'name': 'BitShares', 'e': {'buyucoin': ['inr']}},
                'cloak': {'name': 'CloakCoin', 'e': {'buyucoin': ['inr']}},
                'cvc': {'name': 'Civic', 'e': {'buyucoin': ['inr']}},
                'dcn': {'name': 'Dentacoin', 'e': {'buyucoin': ['inr']}},
                'etc': {'name': 'Ethereum Classic', 'e': {'buyucoin': ['inr']}},
                'fct': {'name': 'Factom', 'e': {'buyucoin': ['inr']}},
                'lsk': {'name': 'Lisk', 'e': {'buyucoin': ['inr']}},
                'nxt': {'name': 'Nxt', 'e': {'buyucoin': ['inr'], 'buyucoin': ['inr']}},
                'pay': {'name': 'TenX', 'e': {'buyucoin': ['inr']}},
                'pivx': {'name': 'PIVX', 'e': {'buyucoin': ['inr']}},
                'rep': {'name': 'Augur', 'e': {'buyucoin': ['inr']}},
                'steem': {'name': 'Steem', 'e': {'buyucoin': ['inr']}},
                'strat': {'name': 'Stratis', 'e': {'buyucoin': ['inr']}},
                'xem': {'name': 'NEM', 'e': {'buyucoin': ['inr']}}
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
