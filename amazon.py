import os
from dotenv import load_dotenv
from logger import set_logger
load_dotenv() #環境変数のロード
from logger import set_logger
logger = set_logger(__name__)
from sp_api.api import Catalog
from sp_api.base.marketplaces import Marketplaces
import pandas as pd




def fetch_amazon_item_price(jan_list):
    amazon_item_list = []
    for jan in jan_list:
        jan = jan[0]
        res = Catalog(Marketplaces.JP).list_items(jan=jan)
    print(res)

if __name__ == "__main__":
    fetch_amazon_item_price()