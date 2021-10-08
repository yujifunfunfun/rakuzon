import os
from dotenv import load_dotenv
from logger import set_logger
load_dotenv() #環境変数のロード
from logger import set_logger
logger = set_logger(__name__)
from sp_api.api import Catalog
from sp_api.base.marketplaces import Marketplaces
import pandas as pd




# jan_list = pd.read_csv('jan.csv',header=None).values.tolist()
# amazon_item_list = []

res = Catalog(Marketplaces.JP).list_items(JAN='4530107941624')

item_list = res.payload.get('Items')[0].get('Identifiers').get('MarketplaceASIN').get('ASIN')

item = res.payload.get('Items')


print(len(item))




[{'Identifiers': {'MarketplaceASIN': {'MarketplaceId': 'A1VC38T7YXB528', 'ASIN': 'B077QV8NXH'}}, 'AttributeSets': [{'Binding': 'ヘルスケア&ケア用品', 'Brand': 'OCEAN TRICO(オーシャントリコ)', 'Color': 'ブルー', 'Flavor': 'シャインオーバー ツヤ×キープ', 'ItemDimensions': {'Weight': {'value': 0.01, 'Units': 'pounds'}}, 'IsAdultProduct': False, 'Label': 'フィッツコーポレーション', 'ListPrice': {'Amount': 1650.0, 'CurrencyCode': 'JPY'}, 'Manufacturer': 'フィッツコーポレーション', 'PackageDimensions': {'Height': {'value': 2.2440944859, 'Units': 'inches'}, 'Length': {'value': 2.9527559025, 'Units': 'inches'}, 'Width': {'value': 2.2834645646, 'Units': 'inches'}, 'Weight': {'value': 0.2866009406, 'Units': 'pounds'}}, 'PackageQuantity': 1, 'PartNumber': '311232018', 'ProductGroup': 'Beauty', 'ProductTypeName': 'HAIR_STYLING_AGENT', 'Publisher': 'フィッツコーポ 
レーション', 'ReleaseDate': '2018-04-14', 'Size': '80グラム (x 1)', 'SmallImage': {'URL': 'https://m.media-amazon.com/images/I/41B428MEXuL._SL75_.jpg', 'Height': {'Units': 'pixels', 'value': 75}, 'Width': {'Units': 'pixels', 'value': 75}}, 'Studio': 'フィッツコーポレーション', 'Title': 'オーシャントリコ ヘアワックス(シャイ
ンオーバー) ツヤ×キープ'}], 'Relationships': [{'Identifiers': {'MarketplaceASIN': {'MarketplaceId': 'A1VC38T7YXB528', 'ASIN': 'B0822J5ZRZ'}}}], 'SalesRankings': [{'ProductCategoryId': 'beauty_display_on_website', 'Rank': 1347}, {'ProductCategoryId': '169739011', 'Rank': 27}]}, {'Identifiers': {'MarketplaceASIN': {'MarketplaceId': 'A1VC38T7YXB528', 'ASIN': 'B07ZTDB7PF'}}, 'AttributeSets': [{'Binding': 'セット買い', 'Brand': 'OCEAN TRICO(オーシャントリコ)', 'ProductGroup': 'Beauty', 'ProductTypeName': 'HAIR_STYLING_AGENT', 'Size': '2個 
アソート', 'SmallImage': {'URL': 'https://m.media-amazon.com/images/I/311KEgvM9AL._SL75_.jpg', 'Height': {'Units': 'pixels', 'value': 75}, 'Width': {'Units': 'pixels', 'value': 75}}, 'Title': '【セット買い】オーシャ 
ントリコ ヘアワックス(シャインオーバー) ツヤ×キープ & ヘアワックス(エアー) エアリー×キープ'}], 'Relationships': [{'Identifiers': {'MarketplaceASIN': {'MarketplaceId': 'A1VC38T7YXB528', 'ASIN': 'B0822J5ZRZ'}}}], 'SalesRankings': [{'ProductCategoryId': 'beauty_display_on_website', 'Rank': 1347}, {'ProductCategoryId': '169739011', 'Rank': 27}]}, {'Identifiers': {'MarketplaceASIN': {'MarketplaceId': 'A1VC38T7YXB528', 'ASIN': 'B07ZTDSVVS'}}, 'AttributeSets': [{'Binding': 'セット買い', 'Brand': 'OCEAN TRICO(オーシャントリコ)', 'ProductGroup': 'Beauty', 'ProductTypeName': 'HAIR_STYLING_AGENT', 'Size': '2個アソート', 'SmallImage': {'URL': 'https://m.media-amazon.com/images/I/31Kxt0OuHSL._SL75_.jpg', 'Height': {'Units': 'pixels', 'value': 75}, 'Width': {'Units': 'pixels', 'value': 75}}, 'Title': '【セット買い】オーシャントリコ ヘアワックス(シャインオーバー) ツ 
ヤ×キープ & ヘアワックス(クレイ) ボリューム×キープ'}], 'Relationships': [{'Identifiers': {'MarketplaceASIN': {'MarketplaceId': 'A1VC38T7YXB528', 'ASIN': 'B0822J5ZRZ'}}}], 'SalesRankings': [{'ProductCategoryId': 'beauty_display_on_website', 'Rank': 1347}, {'ProductCategoryId': '169739011', 'Rank': 27}]}, {'Identifiers': {'MarketplaceASIN': {'MarketplaceId': 'A1VC38T7YXB528', 'ASIN': 'B07ZTDYMLT'}}, 'AttributeSets': [{'Binding': 'セット買い', 'Brand': 'OCEAN TRICO(オーシャントリコ)', 'ProductGroup': 'Beauty', 'ProductTypeName': 'HAIR_STYLING_AGENT', 'Size': '2個アソート', 'SmallImage': {'URL': 'https://m.media-amazon.com/images/I/31ej9DU-QAL._SL75_.jpg', 'Height': {'Units': 'pixels', 'value': 75}, 'Width': {'Units': 'pixels', 'value': 75}}, 'Title': '【セット買い】オーシャントリコ ヘアワックス(シャインオーバー) ツヤ×キープ & ヘアワックス(エッジ) シャープ
×キープ'}], 'Relationships': [{'Identifiers': {'MarketplaceASIN': {'MarketplaceId': 'A1VC38T7YXB528', 'ASIN': 'B0822J5ZRZ'}}}], 'SalesRankings': [{'ProductCategoryId': 'beauty_display_on_website', 'Rank': 1347}, {'ProductCategoryId': '169739011', 'Rank': 27}]}, {'Identifiers': {'MarketplaceASIN': {'MarketplaceId': 'A1VC38T7YXB528', 'ASIN': 'B07ZTFLRNV'}}, 'AttributeSets': [{'Binding': 'セット買い', 'Brand': 'OCEAN TRICO(オーシャ
ントリコ)', 'ProductGroup': 'Beauty', 'ProductTypeName': 'HAIR_STYLING_AGENT', 'Size': '2個アソート', 'SmallImage': {'URL': 'https://m.media-amazon.com/images/I/31aSDvxE+XL._SL75_.jpg', 'Height': {'Units': 'pixels', 
'value': 75}, 'Width': {'Units': 'pixels', 'value': 75}}, 'Title': '【セット買い】オーシャントリコ ヘアワッ 
クス(シャインオーバー) ツヤ×キープ & OCEAN TRICO(オーシャントリコ) オーシャントリコ ヘアワックス(オーバード 
ライブ) マット×キープ オーバードライブ 単品 80g'}], 'Relationships': [{'Identifiers': {'MarketplaceASIN': {'MarketplaceId': 'A1VC38T7YXB528', 'ASIN': 'B0822J5ZRZ'}}}], 'SalesRankings': [{'ProductCategoryId': 'beauty_display_on_website', 'Rank': 1347}, {'ProductCategoryId': '169739011', 'Rank': 27}]}, {'Identifiers': {'MarketplaceASIN': {'MarketplaceId': 'A1VC38T7YXB528', 'ASIN': 'B07ZTDV3DS'}}, 'AttributeSets': [{'Binding': 'セ 
ット買い', 'Brand': 'OCEAN TRICO(オーシャントリコ)', 'ProductGroup': 'Beauty', 'ProductTypeName': 'HAIR_STYLING_AGENT', 'Size': '2個アソート', 'SmallImage': {'URL': 'https://m.media-amazon.com/images/I/31WIGbHyQVL._SL75_.jpg', 'Height': {'Units': 'pixels', 'value': 75}, 'Width': {'Units': 'pixels', 'value': 75}}, 'Title': 
'【セット買い】オーシャントリコ ヘアワックス(シャインオーバー) ツヤ×キープ & ヘアワックス(ナチュラル) ルーズ
×キープ'}], 'Relationships': [{'Identifiers': {'MarketplaceASIN': {'MarketplaceId': 'A1VC38T7YXB528', 'ASIN': 'B0822J5ZRZ'}}}], 'SalesRankings': [{'ProductCategoryId': 'beauty_display_on_website', 'Rank': 1347}, {'ProductCategoryId': '169739011', 'Rank': 27}]}]