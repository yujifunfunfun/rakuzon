import eel
from calc_profit import *


@eel.expose
def calc_profit(spu,add_rate,specified_profit,jan_list):
    main(spu,add_rate,specified_profit,jan_list)

eel.init("web")
eel.start("main.html",size=(600, 600))


