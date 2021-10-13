from rakuten import *
from amazon import *
import pandas as pd
import eel
from logger import *
logger = set_logger(__name__)


def calc_profit(specified_profit,rakuten_item_list,amazon_item_list):
    specified_profit = int(specified_profit)
    cols = ['jan','rakuten_purchase_price','amazon_price','buybox_price','package_quantity','profit','profit_rate','rakuten_url','amazon_url','category_list']
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
            if profit_rate > specified_profit:
                record = pd.Series([jan,rakuten_purchase_price,amazon_price,buybox_price,package_quantity,profit,profit_rate,rakuten_url,amazon_url,category_list], index=profit_df.columns)
                profit_df = profit_df.append(record, ignore_index=True)
    profit_df.to_csv("profit.csv")

def make_janlist_by_rakuten_data(rakuten_item_list):
    jan_list = []
    for rakuten_item in rakuten_item_list:
        jan = rakuten_item[0]
        jan_list.append(jan)
    return jan_list
    
def main2(spu,add_rate,specified_profit):
    try:
        jan_list = pd.read_csv('jan.csv',header=None,dtype=object).values.tolist()
        rakuten_item_list = fetch_rakuten_item_price(spu,add_rate)
        jan_list = make_janlist_by_rakuten_data(rakuten_item_list)
        print(jan_list)
        amazon_item_list = fetch_amazon_item_price(jan_list)
        calc_profit(specified_profit,rakuten_item_list,amazon_item_list)
        logger.info("完了")
        eel.view_log_js('完了')
    except Exception as e:
        logger.info(e)
        eel.view_log_js('エラー発生 処理を中断します')


def main(spu,add_rate,specified_profit):
    eel.view_log_js('商品情報取得中…')
    jan_list = pd.read_csv('jan.csv',header=None,dtype=object).values.tolist()
    rakuten_item_list = []
    amazon_item_list = []
    for jan in jan_list:
        eel.view_log_js(f'{jan[0]}')
        try:
            jan = jan[0]
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
    


if __name__ == "__main__":
    main(15,0,-1000)