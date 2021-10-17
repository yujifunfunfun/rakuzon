import eel
from calc_profit import *


@eel.expose
def calc_profit(spu,add_rate,coupon,specified_profit,amazon_min_price,amazon_max_price,min_offer_count,arr1):
    main(spu,add_rate,coupon,specified_profit,amazon_min_price,amazon_max_price,min_offer_count,arr1)


eel.init("web")
eel.start("main.html",size=(600, 600))


