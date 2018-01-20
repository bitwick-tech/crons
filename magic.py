import datetime
import json
import logging
# from selenium import webdriver
from threading import Thread

import pymongo
import requests
from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support import expected_conditions as expected
from selenium.webdriver.support.wait import WebDriverWait

# from selenium.webdriver.common.keys import Keys

apiUrlMapping = {"zebpay": "https://www.zebapi.com/api/v1/market/ticker/btc/inr",
                  "koinex": "https://koinex.in/api/ticker",
                  "unocoin": "https://www.unocoin.com/trade.php?all"}
logging.basicConfig(filename='magic.log', level=logging.DEBUG)
results = {"ts": datetime.datetime.now(datetime.timezone.utc)}


class GetDataThread(Thread):
    def __init__(self, com):
        self.com = com
        super(GetDataThread, self).__init__()

    def run(self):
        get_data(self.com)


def get_data(com):
    if com == "unocoin":
        options = Options()
        options.add_argument('-headless')
        driver = Firefox(firefox_options=options)
        wait = WebDriverWait(driver, timeout=10)
        driver.get(apiUrlMapping[com])
        wait.until(expected.visibility_of_element_located((By.TAG_NAME, 'body'))).send_keys(
            'headless firefox' + Keys.ENTER)
        x = driver.find_element_by_xpath("//html/body").get_attribute('innerHTML')
        x = json.loads(x)
        driver.quit()
        # logging.info((apiUrlMapping[com]) + "     " + str(x))
        results[com] = x
        # return x
    else:
        ret = (requests.get(apiUrlMapping[com]))
        # print(ret.headers)
        # logging.info((apiUrlMapping[com]) + "     " + str(ret))
        results[com] = ret.json()
        # return ret.json()


def get_final_data():
    threads = []
    for k in apiUrlMapping:
        t = GetDataThread(k)
        threads.append(t)
        t.start()
    for t in threads:
        t.join()

    # result = get_data(k)
    #    if result is not None:
    #        results[k] = result
    return results


def do_magic():
    # from pymongo import MongoClient

    client = pymongo.MongoClient()
    db = client.coinExchangeDB
    collection = db.coinInfo

    finalData = get_final_data()
    idd = collection.insert_one(finalData).inserted_id

    # logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
    # logging.info(finalData["ts"])
    logging.info(str(idd))


if __name__ == '__main__':
    do_magic()