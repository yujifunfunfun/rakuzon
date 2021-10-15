import os
from dotenv import load_dotenv
from logger import set_logger
load_dotenv() #環境変数のロード
from logger import set_logger
logger = set_logger(__name__)
from sp_api.api import Catalog
from sp_api.api import ProductFees
from sp_api.api import CatalogItems

from sp_api.base.marketplaces import Marketplaces
import pandas as pd
import requests
import csv



# jan_list = pd.read_csv('jan.csv',header=None).values.tolist()
# amazon_item_list = []

# res = Catalog(Marketplaces.JP).list_items(JAN='6973271603802')

# item = res.payload.get('Items')[0].get('AttributeSets')[0].get('ListPrice').get('Amount')
# asin = res.payload.get('Items')[0].get('Identifiers').get('MarketplaceASIN').get('ASIN')

# category = res.payload.get('Items')[0].get('AttributeSets')[0].get('ProductGroup')

# res = Catalog(Marketplaces.JP).get_item(asin='B09GRPGMNG')

# fees_data = ProductFees(Marketplaces.JP).get_product_fees_estimate_for_asin(asin='B084HYHYHY',price=1600,currency='JPY')

# fees = fees_data.payload.get('FeesEstimateResult').get('FeesEstimate').get('TotalFeesEstimate').get('Amount')


# res = Catalog(Marketplaces.JP).list_items(QueryContextId='Beauty')
# res = CatalogItems(Marketplaces.JP).search_catalog_items(keywords='デジタル優品屋',pageSize=20)



with open('jan.csv') as f:
    reader = csv.reader(f)
    header = next(reader)
    l = [row for row in reader]



print(l)




