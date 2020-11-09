import pandas as pd
import tushare as ts
import talib as tb
import time
import easyquotation as eq
global ts
ts.set_token("8245313cabb6239a4dce3591e2c64fa199611ee7ade564cf9e437b61")
pro = ts.pro_api("8245313cabb6239a4dce3591e2c64fa199611ee7ade564cf9e437b61")


def get_choose_etf_list():
    df = pd.read_excel("D:\\fileNeed\\test03.xlsx")
    list1 = df["ts_code"].tolist()
    list2 = df["name"].tolist()
    return list1,list2


def get_all_etf_list():
    pro = ts.pro_api("8245313cabb6239a4dce3591e2c64fa199611ee7ade564cf9e437b61")
    df = pro.fund_basic(market='E')
    df2 = df[df['name'].str.contains('ETF')]
    list1 = df2["ts_code"].tolist()
    list2 = df2["name"].tolist()
    return list1,list2


def get_now_time():
    now_time = (time.strftime("%Y%m%d", time.localtime()))
    return now_time


def if_slowj_big_slowkd(slowj,slowk,slowd):
    info = ""
    if slowj[-1]>80:
        if slowj[-2]>80:
            return "j持续>80"
        if slowj[-2]<80:
            return "j增长>80"
    if slowj[-1]<20:
        if slowj[-2]<20:
            return "j持续<20"
        if slowj[-2]>20:
            return "j增长至>20"
    else:
        return "KDJ无异常"
    # if 20<slowj[-1]<80:
    #     if slowj[-2]>80:
    #         return "kdj下降至80以下,SELL--"
    #     if slowj[-2]<20:
    #         return "kdj上升至20以上，BUY++"
    #     if slowj[-1]>65 and slowj[-2]<slowj[-1]:
    #         return "kdj上升，可能上涨"
    #     if slow[-1]<


def if_ma5_big_ma10(ma5,ma10):
    if ma5[-1]>ma10[-1]:
        return "ma5>ma10"
    else:
        return "ma5<ma10"


def if_macd_increase(macd):
    if macd[-1]<0:
        if macd[-3]>=macd[-2]>macd[-1]:
            return "macd <0:持续下降"
        if macd[-3]>=macd[-2]<macd[-1]:
            return "macd <0:开始上升"
        if macd[-3]<=macd[-2]>macd[-2]:
            return "macd <0:开始下降"
        if macd[-3]<=macd[-2]<macd[-1]:
            return "macd <0:持续上升"
        else:
            return "macd<0:保持持平"
    if macd[-1] > 0:
        if macd[-3] >= macd[-2] > macd[-1]:
            return "macd >0:持续下降"
        if macd[-3] >= macd[-2] < macd[-1]:
            return "macd >0:开始上升"
        if macd[-3] <= macd[-2] > macd[-2]:
            return "macd >0:开始下降"
        if macd[-3] <= macd[-2] < macd[-1]:
            return "macd >0:持续上升"
        else:
            return "macd>0:保持持平"
    else:
        if macd[-3] >= macd[-2] > macd[-1]:
            return "macd =0:持续下降"
        if macd[-3] >= macd[-2] < macd[-1]:
            return "macd =0:开始上升"
        if macd[-3] <= macd[-2] > macd[-2]:
            return "macd =0:开始下降"
        if macd[-3] <= macd[-2] < macd[-1]:
            return "macd =0:持续上升"
        else:
            return "macd=0:保持持平"


def if_price_increase(price):
    if price[-3]>price[-2]>=price[-1]:
        return "price:持续下降"
    if price[-3]>price[-2]<=price[-1]:
        return "price:开始上升"
    if price[-3]<price[-2]>=price[-1]:
        return "price:开始下降"
    if price[-3]<price[-2]<=price[-1]:
        return "price:持续上升"


def etf_should_buy(li,l2):
    for i in range(len(li)):
        h = ts.pro_bar(li[i],asset="FD",start_date="20200101",end_date=get_now_time(),ma=[5,10]).iloc[::-1]

        n = h.shape[0]
        if n > 33:
            # -----------    获取kdj值      ---------------#
            slowk, slowd = tb.STOCH(h['high'].values,
                                    h['low'].values,
                                    h['close'].values,
                                    fastk_period=9,
                                    slowk_period=3,
                                    slowk_matype=0,
                                    slowd_period=3,
                                    slowd_matype=0)
            slowj = 3 * slowk - 2 * slowd

            # -------------   获取ma5 ma10 --------------- #
            ma5 = h["ma5"].tolist()
            ma10 = h["ma10"].tolist()

            # --------------  获取macd值  ----------------- #
            macd,signal,hist = tb.MACD(h["close"].values, 12, 26, 9)

            # --------------  获取adx值  ----------------- #
            adx = tb.ADX(h["high"].values,
                         h["low"].values,
                         h["close"].values,
                         timeperiod=14)

            # --------------  获取当前价格  ----------------- #
            price = h["close"].tolist()

            # ----------------  格式化数据 ---------------------#

            slowj[-1] = round(slowj[-1],3)
            ma5[-1] = round(ma5[-1], 3)
            ma10[-1] = round(ma10[-1],3)
            macd[-1] = round(macd[-1],3)
            adx[-1] = round(adx[-1],3)

            if slowj[-1] > slowk[-1] > slowd[-1] and \
                        macd[-2] < macd[-1]:
                if price[-1] < 10:
                    print(li[i],if_price_increase(price),if_ma5_big_ma10(ma5,ma10),if_macd_increase(macd),if_slowj_big_slowkd(slowj,slowk,slowd))

            # 56#符合特征的
            # if slowj[n-2] < 20 < slowj[n-1] and slowj[n-1] > slowk[n-1] > slowd[n-1]:
            #     print(li[i],"BUY++",get_now_time())
            # if slowj[n-2] > 80 > slowj[n-1] and slowj[n-1] < slowk[n-1] < slowd[n-1] and slowj[n-2] > slowk[n-2] > slowd[n-2]:
            #     print(li[i],"SELL--",get_now_time())
            #
            # if slowj[n-1] > 80 > slowj[n - 2] and slowj[n-1] > slowk[n-1] > slowd[n-1] and slowj[n-2] < slowk[n-2] > slowd[n-2]:
            #     print(li[i],"BUY+",get_now_time())
            #
            # if 50 > slowj[n-1] and slowj[n-1] < slowk[n-1] < slowd[n-1] and slowj[n-2] > slowk[n-2] > slowd[n-2]:
            #     print(li[i], "SELL--",get_now_time())
            time.sleep(0.2)


list1,list2 = get_choose_etf_list()

etf_should_buy(list1,list2)
