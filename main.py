import eel
from calc_profit import *


@eel.expose
def calc_profit(spu,add_rate,specified_profit):
    main(spu,add_rate,specified_profit)

eel.init("web")
eel.start("main.html",size=(600, 600))


