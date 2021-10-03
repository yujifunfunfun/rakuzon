from rakuten import *
from amazon import *
import pandas as pd


def calc_profit(specified_profit,rakuten_item_list,amazon_item_list):

    cols = ['jan','profit','profit_rate','rakuten_url','amazon_url']
    profit_df = pd.DataFrame(index=[], columns=cols)

    for rakuten_item,amazon_item in zip(rakuten_item_list,amazon_item_list):
        jan = rakuten_item[0]
        rakuten_purchase_price = rakuten_item[2]
        rakuten_url = rakuten_item[3]
        amazon_price = amazon_item[2]

        # アマゾンに無かった商品はスルー
        if amazon_price == 0:
            pass
        else:
            amazon_url =amazon_item[3]
            # 利益計算
            profit = amazon_price - rakuten_purchase_price
            # 利益率計算
            profit_rate = profit / amazon_price * 100
            # 指定利益率以上のものだけを抽出
            if profit_rate > specified_profit:
                record = pd.Series([jan, profit,profit_rate,rakuten_url,amazon_url], index=profit_df.columns)
                profit_df = profit_df.append(record, ignore_index=True)
    profit_df.to_csv("profit.csv")

def make_janlist_by_rakuten_data(rakuten_item_list):
    jan_list = []
    for rakuten_item in rakuten_item_list:
        jan = rakuten_item[0]
        jan_list.append[jan]
    return jan_list


def main(spu,add_rate,specified_profit):
    rakuten_item_list = fetch_rakuten_item_price(spu,add_rate)
    jan_list = make_janlist_by_rakuten_data(rakuten_item_list)
    amazon_item_list = fetch_amazon_item_price(jan_list)
    calc_profit(specified_profit,rakuten_item_list,amazon_item_list)





