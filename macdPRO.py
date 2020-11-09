import tushare as ts
import talib as tb
import pandas as pd
from time import sleep
global ts
ts.set_token("8245313cabb6239a4dce3591e2c64fa199611ee7ade564cf9e437b61")
pro = ts.pro_api("8245313cabb6239a4dce3591e2c64fa199611ee7ade564cf9e437b61")


def get_all_list():
    df = pd.read_excel("C:\\Users\\Administrator\\Desktop\\test03.xlsx")
    list1 = df["ts_code"].tolist()
    # pro = ts.pro_api("8245313cabb6239a4dce3591e2c64fa199611ee7ade564cf9e437b61")
    # df = pro.fund_basic(market='E')
    # df2 = df[df['name'].str.contains('ETF')]
    # list1 = df2["ts_code"].tolist()
    # pd.set_option('display.max_rows',None)
    return list1

def get_all_stock():
    pro = ts.pro_api("8245313cabb6239a4dce3591e2c64fa199611ee7ade564cf9e437b61")
    data = pro.query('stock_basic', exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')
    list1 = data["ts_code"].tolist()
    return list1

def info_buy_first(info,df,j):
    info["trade_number"] += 1
    info["trade_date"] = str(df["trade_date"].iloc[j])
    info["price"] = float(df["close"].iloc[j])

    info["balance"] = 0
    info["asset"] = info["position"] * info["price"] + info["balance"]
    info["position"] = info["position"] + 100


def info_sell(info,df,j):
    info["trade_number"] += 1
    info["trade_date"] = str(df["trade_date"].iloc[j])

    info["profit"] = info["position"] *(float(df["close"].iloc[j])-info["price"]) + info["profit"]
    info["price"] = float(df["close"].iloc[j])

    info["position"] = 0


def info_buy(info,df,j):
    info["trade_number"] += 1
    info["trade_date"] = str(df["trade_date"].iloc[j])
    info["price"] = float(df["close"].iloc[j])
    info["position"] = info["position"] + 100


list_30 = get_all_stock()
list_para = []
start_date = ""
for i in range(len(list_30)):
    info = {"balance":0,"position": 0,"trade_date":None,"trade_number":0,"price":0,
            "profit":0,"max_profit":-1000,"asset":0}
    # h = ts.pro_bar(ts_code=list_30[i],asset="FD",start_date='20200101', end_date='20201029',ma=[1,20]).iloc[::-1]
    h = ts.pro_bar(ts_code=list_30[i], asset="E", start_date='20180401', end_date='20201026', ma=[1, 20]).iloc[::-1]
    for j in range(h.shape[0]):
        if h.shape[0]!=0:
            slowk, slowd = tb.STOCH(h['high'].values,
                                   h['low'].values,
                                   h['close'].values,
                                   fastk_period=9,
                                   slowk_period=3,
                                   slowk_matype=0,
                                   slowd_period=3,
                                   slowd_matype=0)
            slowj = 3 * slowk - 2 * slowd

            if info["trade_number"] == 0 and info["position"] == 0 and slowj[j-1] < 20 < slowj[j] and slowj[j] > slowk[j] > slowd[j]:
                info_buy_first(info,h,j)
            if info["position"] == 0 and slowj[j-1] < 20 < slowj[j] and slowj[j] > slowk[j] > slowd[j] and info["trade_number"] !=0:
                info_buy(info,h,j)
            if info["position"] == 100 and slowj[j] < 80 < slowj[j-1] and slowj[j]<slowk[j]<slowd[j]:
                info_sell(info,h,j)
            if info["position"]!=0 and slowj[j-1] > 20 > slowj[j] and slowj[j] < slowk[j] < slowd[j]:
                info_sell(info, h, j)
            if info["position"] ==0 and slowj[j] > 80 > slowj[j-1] and slowj[j] > slowk[j] > slowd[j]:
                info_buy(info, h, j)
    print(list_30[i],info["trade_number"],info["price"],info["profit"],h.shape[0])

# for i in range(len(list_30)):
#     info = {"balance":0,"position": 0,"trade_date":None,"trade_number":0,"price":0,
#             "profit":0,"max_profit":-1000,"asset":0}
#     df = ts.pro_bar(ts_code=list_30[i],asset="FD",start_date='20190101', end_date='20200129',ma=[4,10]).iloc[::-1]
#     for j in range(df.shape[0]):
#         if df["ma4"].iloc[j] > df["ma10"].iloc[j] and info["position"]==0:
#             if info["trade_number"]==0:
#                 info_buy_first(info,df,j)
#             else:
#                 info_buy(info,df,j)
#         if df["ma4"].iloc[j] < df["ma10"].iloc[j] and info["position"]!=0:
#             info_sell(info,df,j)
#     print(list_30[i],info["profit"])
    # print(list_30[i],info["profit"])


# for i in range(len(list_30)):
#     for freq in ["15min", "30min", "60min"]:
#         print(list_30[i],freq)
#         df = ts.pro_bar(ts_code=list_30[i], start_date='2019-04-01 9:00:00', end_date='2020-4-30 9:00:00', freq=freq,ma=[5,10]).iloc[::-1]
#         if df.shape[0]>2:
#             list_close = df["open"]
#             for day in range(3, 15):
#                 for move_day in range(4, 12):
#                     info = {"balance":0,"position": 0,"trade_date":None,"trade_number":0,"price":0,
#                             "profit":0,"max_profit":0,"asset":0}
#                     dif, dea, macd = tb.MACD(list_close, fastperiod=day, slowperiod=2*day, signalperiod=move_day)
#                     for j in range(len(macd)):
#                         if j > 3:
#                             # buy
#                             if df["ma5"].iloc[j]>df["ma10"].iloc[j] and info["position"] == 0:
#                             # if macd[j-2] < macd[j-1] < macd[j] < 0 and macd[j-2] < macd[j-3] < macd[j-4] and info["position"] == 0:
#                             # if dif[j] < dif[j-1] < 0 and dif[j-1] < dif[j-2] < dif[j-3] and info["position"] == 0:
#                                     if info["trade_number"] == 0:
#                                         info_buy_first(info, df, j)
#                                     if info["trade_number"] != 0:
#                                         info_buy(info, df, j)
#                             # sell
#                             # if 0 < dif[j] < dif[j-1]  and dif[j-1] > dif[j-2] > dif[j-3] and info["position"] == 100:
#                             if macd[j-2] > macd[j-1] > macd[j] > 0 and macd[j-2] > macd[j-3] > macd[j-4] and info["position"] == 100 and str(df["trade_date"].iloc[j]) != info["trade_date"]:
#                                 info_sell(info, df, j)
#                     if info["profit"] > info["max_profit"]:
#                         list_para = [list_30[i],freq,day,move_day,info["profit"]]
#                         info["max_profit"] = info["profit"]
#     print(list_para)

# for i in range(len(list_30)):
#
#         h = ts.pro_bar(ts_code=list_30[i],start_date="20190401",end_date="2020430",asset="FD",freq="D").iloc[::-1]
#         # h = ts.pro_bar(ts_code=list_30[i], start_date='2019-04-01 9:00:00', end_date='2020-4-30 9:00:00', freq="60min",ma=[5,10]).iloc[::-1]
#         info = {"balance":0,"position": 0,"trade_date":None,"trade_number":0,"price":0,
#                 "profit":0,"max_profit":-1000,"asset":0}
#         for j in range(h.shape[0]) :
#             if h.shape[0]!=0:
#                 slowk, slowd = tb.STOCH(h['high'].values,
#                                    h['low'].values,
#                                    h['close'].values,
#                                    fastk_period=9,
#                                    slowk_period=3,
#                                    slowk_matype=0,
#                                    slowd_period=3,
#                                    slowd_matype=0)
#
#                 if (slowk[j] > 90 or slowd[j] > 90) and info["position"] == 0:
#                     if info["trade_number"] == 0:
#                         info_buy_first(info,h,j)
#
#                     else:
#                         info_buy(info,h,j)
#
#                 if (slowk[j] < 10 or slowd[j] < 10) and info["position"] == 100 and h["trade_date"].iloc[j]!=info["trade_date"]:
#                     info_sell(info,h,j)
#
#         print(list_30[i],info["trade_number"],info["price"],info["profit"])
