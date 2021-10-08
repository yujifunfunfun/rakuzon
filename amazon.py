import os
from dotenv import load_dotenv
from logger import set_logger
load_dotenv() #環境変数のロード
from logger import set_logger
logger = set_logger(__name__)
from sp_api.api import Catalog
from sp_api.api import ProductFees
from sp_api.base.marketplaces import Marketplaces
import pandas as pd




def fetch_amazon_item_price(jan_list):
    amazon_item_list = []
    for jan in jan_list:
        jan = jan[0]
        res = Catalog(Marketplaces.JP).list_items(JAN=jan)
        item_list = res.payload.get('Items')
        item_count = len(item_list)
        for n in range(item_count):
            if n == 0:    
                price = item_list[n].get('AttributeSets')[0].get('ListPrice').get('Amount')
                asin = item_list[n].get('Identifiers').get('MarketplaceASIN').get('ASIN')
            elif price > item_list[n].get('AttributeSets')[0].get('ListPrice').get('Amount'):
                price = item_list[n].get('AttributeSets')[0].get('ListPrice').get('Amount')
                asin = item_list[n].get('Identifiers').get('MarketplaceASIN').get('ASIN')
        item_url = f'https://www.amazon.co.jp/gp/product/{asin}'
        fees_data = ProductFees(Marketplaces.JP).get_product_fees_estimate_for_asin(asin=asin,price=price,currency='JPY')
        fees = fees_data.payload.get('FeesEstimateResult').get('FeesEstimate').get('TotalFeesEstimate').get('Amount')
        price = price - fees
        





            
            
if __name__ == "__main__":
    fetch_amazon_item_price()