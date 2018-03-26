import redis
import json

redis_host = '172.31.22.154'
# redis_host = 'localhost'

def run_cron():
    data = get_data_from_redis()
    set_data_in_redis(data["coinData"])


def get_data_from_redis():
    r = redis.Redis(host=redis_host, port=6379, db=0)
    key = "latestCoinData"
    garbage = r.get(key)
    if garbage is not None:
        garbage = json.loads(garbage)
    return garbage


def set_data_in_redis(coinarray):
    ret = {}
    for coin in coinarray:
        ret[coin["id"]] = coin["cp"]
    r = redis.Redis(host=redis_host, port=6379, db=0, decode_responses=True)
    key = "coinsOP"
    r.hmset(key, ret)


if __name__ == '__main__':
    run_cron()
