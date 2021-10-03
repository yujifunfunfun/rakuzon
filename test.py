import os
from dotenv import load_dotenv
from logger import set_logger
load_dotenv() #環境変数のロード
from logger import set_logger
logger = set_logger(__name__)
from sp_api.api import Catalog
from sp_api.base.marketplaces import Marketplaces
import pandas as pd




jan_list = pd.read_csv('jan.csv',header=None).values.tolist()
amazon_item_list = []

res = Catalog(Marketplaces.JP).list_items(jan='4530107941624')
print(res)