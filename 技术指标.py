def MACD(price, fastperiod=12, slowperiod=26, signalperiod=9):
    ewmafast = pd.ewma(price,span=fastperiod)
    ewmaslow = pd.ewma(price,span=slowperiod)
    dif = ewmafast-ewmaslow
    dea = pd.ewma(dif,span=signalperiod)
    bar = (dif-dea)
    bar = 2*(dif-dea)

    return dif,dea,bar