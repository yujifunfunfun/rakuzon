import requests
from time import sleep
import re
import pandas as pd
import requests
from dotenv import load_dotenv
import os
from os.path import join, dirname
from logger import set_logger

load_dotenv(verbose=True)
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)
logger = set_logger(__name__)
rakuten_app_id = os.environ.get("RAKUTEN_APP_ID")
rakuten_app_id2 = os.environ.get("RAKUTEN_APP_ID2")


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


def fetch_rakuten_item_price(spu,add_rate,coupon,jan):
    spu = int(spu)
    add_rate = int(add_rate)
    coupon = int(coupon)
    url = f'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?applicationId={rakuten_app_id}&keyword={jan}&sort=%2BitemPrice&pointRateFlag=1&pointRate&postageFlag=1'
    r = requests.get(url)
    resp = r.json()
    item_counts = len(resp["Items"])
    # 商品がヒットすれば続行
    if item_counts >= 1:
        # 検索結果からポイント率を加味し一番安い商品を取得
        for count in range(item_counts):
            if count == 0:
                item = resp['Items'][count]['Item']
                name = item['itemName']
                if '中古' in name:
                    purchase_price = 999999
                else:
                    price = item['itemPrice']
                    item_url = item['itemUrl']
                    point_rate = item['pointRate']
                    price_coupon = price - coupon
                    point_rate = spu + (point_rate-1) + add_rate
                    # 仕入れ値計算
                    purchase_price = calc_purchase_price(price,point_rate)
                    # クーポン適用後の価格
                    purchase_price_coupon = calc_purchase_price(price_coupon,point_rate)
            else:
                item = resp['Items'][count]['Item']
                name_2 = item['itemName']
                if '中古' in name_2:
                    purchase_price_2 = 999999
                else:
                    price_2 = item['itemPrice']
                    point_rate_2 = item['pointRate']
                    price_coupon_2 = price_2 - coupon
                    point_rate_2 = spu + (point_rate_2-1) + add_rate
                    # 仕入れ値計算
                    purchase_price_2 = calc_purchase_price(price_2,point_rate_2) 
                    # クーポン適用後の価格
                    purchase_price_coupon_2 = calc_purchase_price(price_coupon_2,point_rate_2)
                if purchase_price > purchase_price_2:
                    purchase_price = purchase_price_2
                    purchase_price_coupon = purchase_price_coupon_2
                    item_url = item['itemUrl']
                    name = name_2
    else:
        purchase_price = 999999
    url2 = f'https://app.rakuten.co.jp/services/api/IchibaItem/Search/20170706?applicationId={rakuten_app_id2}&keyword={jan}&sort=%2BitemPrice&postageFlag=1'
    r2= requests.get(url2)
    resp2 = r2.json()
    if len(resp2["Items"]) >= 1:
        item2 = resp2['Items'][0]['Item']
        name2 = item2['itemName']
        if '中古' in name2:
            purchase_price2 = 999999
        else:
            price2 = item2['itemPrice']
            item_url2 = item2['itemUrl']
            price_coupon2 = price2 - coupon
            point_rate2 = spu + add_rate
            # 仕入れ値計算
            purchase_price2= calc_purchase_price(price2,point_rate2)
            # クーポン適用後の価格
            purchase_price_coupon2 = calc_purchase_price(price_coupon2,point_rate2)
            half_price = purchase_price / 2
            if purchase_price != 999999 and purchase_price2 < half_price:
                purchase_price2 = 999999
    else:
        purchase_price2 = 999999
    
    if len(resp["Items"]) == len(resp2["Items"]) == 0:
        rakuten_item_data = ['None','None',0,0,'None']
    elif purchase_price <= purchase_price2:
        rakuten_item_data = [jan,name,purchase_price,purchase_price_coupon,item_url]
    else:
        rakuten_item_data = [jan,name2,purchase_price2,purchase_price_coupon2,item_url2]
    return rakuten_item_data


    
if __name__ == "__main__":
    fetch_rakuten_item_price(3,2,0,)