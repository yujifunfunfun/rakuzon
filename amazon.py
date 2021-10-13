import os
from dotenv import load_dotenv
from logger import set_logger
load_dotenv() #環境変数のロード
from logger import set_logger
logger = set_logger(__name__)
from sp_api.api import Catalog
from sp_api.api import ProductFees
from sp_api.api import Products

from sp_api.base.marketplaces import Marketplaces
import pandas as pd
import time


def fetch_amazon_item_price(jan):
    amazon_item_data = []
    res = Catalog(Marketplaces.JP).list_items(JAN=jan)
    item_list = res.payload.get('Items')
    item_count = len(item_list)
    # JAN検索でamzonに商品がない場合
    if item_count == 0:
        amazon_item_data.append([0,'None','None','None','None'])
        print('A')
    # JAN検索でamzonに商品が1つの場合
    elif item_count == 1:
        # 商品情報を1つでも取れなければスルー
        try:
            asin = item_list[0].get('Identifiers').get('MarketplaceASIN').get('ASIN')
            item_price_data = Products(Marketplaces.JP).get_item_offers(asin=asin,ItemCondition='New')
            buybox_price = item_price_data.payload.get('Summary').get('BuyBoxPrices')[0].get('ListingPrice').get('Amount')
            item_url = f'https://www.amazon.co.jp/gp/product/{asin}'
            category_list = fetch_category(asin)
            fba_fee = cal_fba_fee(asin,buybox_price)
            price = buybox_price - fba_fee
            amazon_item_data.append([price,buybox_price,1,item_url,category_list])
        except Exception as e:
            amazon_item_data.append([0,'None','None','None','None'])
            print('B')
    else:
        # JANの検索結果が１つ以上
        asin_list = []
        # 検索結果の全商品のASINを取得
        for n in range(item_count):
            try:   
                asin = item_list[n].get('Identifiers').get('MarketplaceASIN').get('ASIN')
                asin_list.append(asin)
            except Exception as e:
                pass
        # 一個あたりの価格を取得
        for count ,asin in zip(range(len(asin_list)),asin_list):
            time.sleep(1)
            if count == 0:
                try:
                    item_url = f'https://www.amazon.co.jp/gp/product/{asin}'
                    buybox_price = Products(Marketplaces.JP).get_competitive_pricing_for_asins(asin_list=asin_list,ItemCondition='New').payload[count].get('Product').get('CompetitivePricing').get('CompetitivePrices')[0].get('Price').get('ListingPrice').get('Amount')
                    package_quantity = Catalog(Marketplaces.JP).get_item(asin=asin).payload.get('AttributeSets')[0].get('PackageQuantity')
                    category_list = fetch_category(asin)
                    fba_fee = cal_fba_fee(asin,buybox_price)
                    # カート価格-FBA手数料
                    price = buybox_price - fba_fee
                    price_ea = price/package_quantity 
                except Exception as e:
                    price_ea = 0
                    buybox_price = 0
                    package_quantity = 0
                    item_url = 'None'
                    category_list = 'None'
            else:
                try:
                    buybox_price2 = Products(Marketplaces.JP).get_competitive_pricing_for_asins(asin_list=asin_list,ItemCondition='New').payload[count].get('Product').get('CompetitivePricing').get('CompetitivePrices')[0].get('Price').get('ListingPrice').get('Amount')
                    package_quantity2 = Catalog(Marketplaces.JP).get_item(asin=asin).payload.get('AttributeSets')[0].get('PackageQuantity')
                    fba_fee = cal_fba_fee(asin,buybox_price2)
                    # カート価格-FBA手数料
                    price = buybox_price2 - fba_fee
                    price_ea2 = price/package_quantity2
                    if price_ea < price_ea2:
                        price_ea = price_ea2
                        item_url = f'https://www.amazon.co.jp/gp/product/{asin}'
                        buybox_price = buybox_price2
                        package_quantity = package_quantity2
                except Exception as e:
                    pass
        amazon_item_data.append([price_ea,buybox_price,package_quantity,item_url,category_list])
    return amazon_item_data[0]
        
def cal_fba_fee(asin,price):
    try:
        fees_data = ProductFees(Marketplaces.JP).get_product_fees_estimate_for_asin(asin=asin,price=price,currency='JPY',is_fba=True)
        fba_fee = fees_data.payload.get('FeesEstimateResult').get('FeesEstimate').get('TotalFeesEstimate').get('Amount')
    except Exception as e:
        fba_fee = 999999
    return fba_fee

def fetch_category(asin):
    res = Catalog(Marketplaces.JP).list_categories(ASIN=asin).payload[0]
    cat_list = []
    for i in range(100):
        try:
            if i == 0:
                cat = res.get('ProductCategoryName')
                cat_list.append(cat)
            else:
                res = res.get('parent')
                cat = res.get('ProductCategoryName')
                cat_list.append(cat)
        except Exception as e:
            break
    return cat_list

if __name__ == "__main__":
    fetch_amazon_item_price()