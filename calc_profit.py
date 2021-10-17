from rakuten import *
from amazon import *
import pandas as pd
import eel
from logger import *
import time
logger = set_logger(__name__)
import numpy as np
import csv

def calc_profit(specified_profit,rakuten_item_list,amazon_item_list):
    specified_profit = int(specified_profit)
    cols = ['JAN','楽天価格-ポイント','クーポン適用価格','Amazonカート価格-FBA手数料','Amazonカート価格','Amazonパッケージ数','出品者数','利益','利益(クーポン使用)','利益率','利益率(クーポン使用)','楽天URL','AmazonURL','カテゴリー']
    profit_df = pd.DataFrame(index=[], columns=cols)
    for rakuten_item,amazon_item in zip(rakuten_item_list,amazon_item_list):
        jan = rakuten_item[0]
        rakuten_purchase_price = rakuten_item[2]
        rakuten_purchase_price_coupon = rakuten_item[3]
        rakuten_url = rakuten_item[4]
        amazon_price = amazon_item[0]
        # アマゾンに無かった商品はスルー
        if amazon_price == 0:
            pass
        else:
            buybox_price = amazon_item[1]
            package_quantity = amazon_item[2]            
            offer_count = amazon_item[3]
            amazon_url =amazon_item[4]
            category_list = amazon_item[5]
            # 利益計算
            profit = amazon_price - rakuten_purchase_price
            profit_coupon = amazon_price - rakuten_purchase_price_coupon
            # 利益率計算
            profit_rate = profit / amazon_price * 100
            profit_rate_coupon = profit_coupon / amazon_price * 100
            # 指定利益率以上のものだけを抽出
            if profit_rate > specified_profit and profit_rate < 50:
                profit_rate = round(profit_rate,2)
                record = pd.Series([jan,rakuten_purchase_price,rakuten_purchase_price_coupon,amazon_price,buybox_price,package_quantity,offer_count,profit,profit_coupon,profit_rate,profit_rate_coupon,rakuten_url,amazon_url,category_list], index=profit_df.columns)
                profit_df = profit_df.append(record, ignore_index=True)
    profit_df.index = np.arange(1,len(profit_df)+1)
    profit_df.to_csv("profit.csv",encoding="shift-jis",errors='ignore')
    
def load_csv():
    with open('asin_jan.csv') as f:
        reader = csv.reader(f)
        l = [row for row in reader]
    return l

def main(spu,add_rate,coupon,specified_profit,amazon_min_price,amazon_max_price,min_offer_count,filter):
    try:
        eel.view_log_js('商品情報取得中…')
        if 'category' and 'package' in filter:
            asin_jan_list = load_csv()
            rakuten_item_list = []
            amazon_item_list = []
            for asin_jan in asin_jan_list:
                if asin_jan[1] == '':
                    pass
                else:
                    try:
                        rakuten_item_data = fetch_rakuten_item_price(spu,add_rate,coupon,asin_jan[1])
                        if rakuten_item_data[2] == 0:
                            time.sleep(1)
                        else:
                            rakuten_item_list.append(rakuten_item_data)
                            amazon_item_list.append(fetch_amazon_item_price_ca_pa(asin_jan[0],amazon_min_price,amazon_max_price,min_offer_count)) 
                    except Exception as e:
                        print(e)
            calc_profit(specified_profit,rakuten_item_list,amazon_item_list)
        elif 'category' in filter:
            asin_jan_list = load_csv()
            rakuten_item_list = []
            amazon_item_list = []
            for asin_jan in asin_jan_list:
                if asin_jan[1] == '':
                    pass
                else:
                    try:
                        rakuten_item_data = fetch_rakuten_item_price(spu,add_rate,coupon,asin_jan[1])
                        if rakuten_item_data[2] == 0:
                            time.sleep(1)
                        else:
                            rakuten_item_list.append(rakuten_item_data)
                            amazon_item_list.append(fetch_amazon_item_price_ca(asin_jan[0],amazon_min_price,amazon_max_price,min_offer_count)) 
                    except Exception as e:
                        print(e)
            calc_profit(specified_profit,rakuten_item_list,amazon_item_list)
        elif 'package' in filter:
            asin_jan_list = load_csv()
            rakuten_item_list = []
            amazon_item_list = []
            for asin_jan in asin_jan_list:
                if asin_jan[1] == '':
                    pass
                else:
                    try:
                        rakuten_item_data = fetch_rakuten_item_price(spu,add_rate,coupon,asin_jan[1])
                        if rakuten_item_data[2] == 0:
                            time.sleep(1)
                        else:
                            rakuten_item_list.append(rakuten_item_data)
                            amazon_item_list.append(fetch_amazon_item_price_pa(asin_jan[0],amazon_min_price,amazon_max_price,min_offer_count)) 
                    except Exception as e:
                        print(e)
            calc_profit(specified_profit,rakuten_item_list,amazon_item_list)
        else:
            asin_jan_list = load_csv()
            rakuten_item_list = []
            amazon_item_list = []
            for asin_jan in asin_jan_list:
                if asin_jan[1] == '':
                    pass
                else:
                    try:
                        rakuten_item_data = fetch_rakuten_item_price(spu,add_rate,coupon,asin_jan[1])
                        if rakuten_item_data[2] == 0:
                            time.sleep(1)
                        else:
                            rakuten_item_list.append(rakuten_item_data)
                            amazon_item_list.append(fetch_amazon_item_price(asin_jan[0],amazon_min_price,amazon_max_price,min_offer_count)) 
                    except Exception as e:
                        print(e)
            calc_profit(specified_profit,rakuten_item_list,amazon_item_list)            
        logger.info("完了")
        eel.view_log_js('完了')
    except Exception as e:
        logger.info(e)
        eel.view_log_js('エラー発生 処理を中断します')


if __name__ == "__main__":
    main(15,0,-1000)