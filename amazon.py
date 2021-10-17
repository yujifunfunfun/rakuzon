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


def fetch_amazon_item_price_ca_pa(asin,amazon_min_price,amazon_max_price,min_offer_count):
    try:
        amazon_min_price = int(amazon_min_price)
        amazon_max_price = int(amazon_max_price)
        min_offer_count = int(min_offer_count)

        item_data = Products(Marketplaces.JP).get_item_offers(asin=asin,ItemCondition='New')
        buybox_price = item_data.payload.get('Summary').get('BuyBoxPrices')[0].get('ListingPrice').get('Amount') 
        offer_count = item_data.payload.get('Summary').get('TotalOfferCount')
        if offer_count >= min_offer_count and buybox_price >= amazon_min_price and buybox_price < amazon_max_price:
            item_url = f'https://www.amazon.co.jp/gp/product/{asin}'
            category_list = fetch_category(asin)
            fba_fee = cal_fba_fee(asin,buybox_price)
            price = buybox_price - fba_fee
            package_quantity = Catalog(Marketplaces.JP).get_item(asin=asin).payload.get('AttributeSets')[0].get('PackageQuantity')
            amazon_item_data = [price,buybox_price,package_quantity,offer_count,item_url,category_list]
        else:
            amazon_item_data = [0,'None','None','None','None','None'] 
    except Exception as e:
        logger.info(e)
        amazon_item_data = [0,'None','None','None','None','None']
    return amazon_item_data
        
def fetch_amazon_item_price_ca(asin,amazon_min_price,amazon_max_price,min_offer_count):
    try:
        amazon_min_price = int(amazon_min_price)
        amazon_max_price = int(amazon_max_price)
        min_offer_count = int(min_offer_count)

        item_data = Products(Marketplaces.JP).get_item_offers(asin=asin,ItemCondition='New')
        buybox_price = item_data.payload.get('Summary').get('BuyBoxPrices')[0].get('ListingPrice').get('Amount') 
        offer_count = item_data.payload.get('Summary').get('TotalOfferCount')
        if offer_count >= min_offer_count and buybox_price >= amazon_min_price and buybox_price < amazon_max_price:
            item_url = f'https://www.amazon.co.jp/gp/product/{asin}'
            category_list = fetch_category(asin)
            fba_fee = cal_fba_fee(asin,buybox_price)
            price = buybox_price - fba_fee
            amazon_item_data = [price,buybox_price,'-',offer_count,item_url,category_list]
        else:
            amazon_item_data = [0,'None','None','None','None','None'] 
    except Exception as e:
        logger.info(e)
        amazon_item_data = [0,'None','None','None','None','None']
    return amazon_item_data


def fetch_amazon_item_price_pa(asin,amazon_min_price,amazon_max_price,min_offer_count):
    try:
        amazon_min_price = int(amazon_min_price)
        amazon_max_price = int(amazon_max_price)
        min_offer_count = int(min_offer_count)

        item_data = Products(Marketplaces.JP).get_item_offers(asin=asin,ItemCondition='New')
        buybox_price = item_data.payload.get('Summary').get('BuyBoxPrices')[0].get('ListingPrice').get('Amount') 
        offer_count = item_data.payload.get('Summary').get('TotalOfferCount')
        if offer_count >= min_offer_count and buybox_price >= amazon_min_price and buybox_price < amazon_max_price:
            item_url = f'https://www.amazon.co.jp/gp/product/{asin}'
            fba_fee = cal_fba_fee(asin,buybox_price)
            price = buybox_price - fba_fee
            package_quantity = Catalog(Marketplaces.JP).get_item(asin=asin).payload.get('AttributeSets')[0].get('PackageQuantity')
            amazon_item_data = [price,buybox_price,package_quantity,offer_count,item_url,'-']
        else:
            amazon_item_data = [0,'None','None','None','None','None'] 
    except Exception as e:
        logger.info(e)
        amazon_item_data = [0,'None','None','None','None','None']
    return amazon_item_data

def fetch_amazon_item_price(asin,amazon_min_price,amazon_max_price,min_offer_count):
    try:
        amazon_min_price = int(amazon_min_price)
        amazon_max_price = int(amazon_max_price)
        min_offer_count = int(min_offer_count)

        item_data = Products(Marketplaces.JP).get_item_offers(asin=asin,ItemCondition='New')
        buybox_price = item_data.payload.get('Summary').get('BuyBoxPrices')[0].get('ListingPrice').get('Amount') 
        offer_count = item_data.payload.get('Summary').get('TotalOfferCount')
        if offer_count >= min_offer_count and buybox_price >= amazon_min_price and buybox_price < amazon_max_price:
            item_url = f'https://www.amazon.co.jp/gp/product/{asin}'
            fba_fee = cal_fba_fee(asin,buybox_price)
            price = buybox_price - fba_fee
            amazon_item_data = [price,buybox_price,'-',offer_count,item_url,'-']
        else:
            amazon_item_data = [0,'None','None','None','None','None'] 
    except Exception as e:
        logger.info(e)
        amazon_item_data = [0,'None','None','None','None','None']
    return amazon_item_data


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