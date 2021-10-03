import csv
import sys
import codecs
import math
import random
import requests
from time import sleep
import re
import pandas as pd
import requests
from bs4 import BeautifulSoup



def calc_purchase_price(price,point_rate):
    # 十の位切り捨て
    round_price = re.sub("[0123456789]$","", str(price))
    round_price = re.sub("[0123456789]$","", round_price)
    round_price = int(round_price +'00')
    # 獲得ポイント計算
    point = round_price * point_rate / 100
    # 仕入れ値(価格-ポイント)
    purchase_price = price - point
    return purchase_price


def fetch_rakuten_item_price(spu,add_rate):
    jan_list = pd.read_csv('jan.csv',header=None).values.tolist()
    rakuten_item_list = []
    for jan in jan_list:
        jan = jan[0]
        url = f'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?applicationId=1066714723520618130&keyword={jan}&sort=%2BitemPrice&pointRateFlag=1&pointRate&postageFlag=1'
        r = requests.get(url)
        resp = r.json()
        if len(resp["Items"]) >= 1:
            sleep(1)
            item = resp['Items'][0]['Item']
            name = item['itemName']
            price = item['itemPrice']
            item_url = item['itemUrl']
            point_rate = item['pointRate']
            point_rate = spu + (point_rate-1) + add_rate
            # 仕入れ値計算
            purchase_price = calc_purchase_price(price,point_rate)
            rakuten_item_list.append([jan,name,purchase_price,item_url])
        else:            
            sleep(1)
            url = f'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?applicationId=1066714723520618130&keyword={jan}&sort=%2BitemPrice&postageFlag=1'
            r = requests.get(url)
            resp = r.json()
            if len(resp["Items"]) >= 1:
                sleep(1)
                r = requests.get(url)
                resp = r.json()
                item = resp['Items'][0]['Item']
                name = item['itemName']
                price = item['itemPrice']
                item_url = item['itemUrl']     
                point_rate = spu + add_rate
                # 仕入れ値計算
                purchase_price = calc_purchase_price(price,point_rate)
                rakuten_item_list.append([jan,name,purchase_price,item_url])
    return rakuten_item_list


if __name__ == "__main__":
    fetch_rakuten_item_price(3,2)