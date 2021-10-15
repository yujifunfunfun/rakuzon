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
    cols = ['JAN','楽天価格-ポイント','Amazonカート価格-FBA手数料','Amazonカート価格','Amazonパッケージ数','利益','利益率','楽天URL','AmazonURL','カテゴリー']
    profit_df = pd.DataFrame(index=[], columns=cols)
    for rakuten_item,amazon_item in zip(rakuten_item_list,amazon_item_list):
        jan = rakuten_item[0]
        rakuten_purchase_price = rakuten_item[2]
        rakuten_url = rakuten_item[3]
        amazon_price = amazon_item[0]
        # アマゾンに無かった商品はスルー
        if amazon_price == 0:
            pass
        else:
            buybox_price = amazon_item[1]
            package_quantity = amazon_item[2]            
            amazon_url =amazon_item[3]
            category_list = amazon_item[4]
            # 利益計算
            profit = amazon_price - rakuten_purchase_price
            # 利益率計算
            profit_rate = profit / amazon_price * 100
            # 指定利益率以上のものだけを抽出
            if profit_rate > specified_profit and profit_rate < 50:
                profit_rate = round(profit_rate,2)
                record = pd.Series([jan,rakuten_purchase_price,amazon_price,buybox_price,package_quantity,profit,profit_rate,rakuten_url,amazon_url,category_list], index=profit_df.columns)
                profit_df = profit_df.append(record, ignore_index=True)
    profit_df.index = np.arange(1,len(profit_df)+1)
    profit_df.to_csv("profit.csv",encoding="shift-jis")

def make_janlist_by_rakuten_data(rakuten_item_list):
    jan_list = []
    for rakuten_item in rakuten_item_list:
        jan = rakuten_item[0]
        jan_list.append(jan)
    return jan_list
    



def load_csv():
    with open('jan.csv') as f:
        reader = csv.reader(f)
        header = next(reader)
        l = [row for row in reader]
    return l



def main(spu,add_rate,specified_profit,jan_list):
    try:
        eel.view_log_js('商品情報取得中…')
        # jan_list = load_csv()
        jan_list = jan_list.split()
        rakuten_item_list = []
        amazon_item_list = []
        for jan in jan_list:
            try:
                rakuten_item_data = fetch_rakuten_item_price(spu,add_rate,jan)
                if rakuten_item_data[2] == 0:
                    time.sleep(1)
                else:
                    rakuten_item_list.append(rakuten_item_data)
                    amazon_item_list.append(fetch_amazon_item_price(jan)) 
            except Exception as e:
                pass
        calc_profit(specified_profit,rakuten_item_list,amazon_item_list)
        logger.info("完了")
        eel.view_log_js('完了')
    except Exception as e:
        logger.info(e)
        eel.view_log_js('エラー発生 処理を中断します')

        


if __name__ == "__main__":
    main(15,0,-1000)