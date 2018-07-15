# -*- coding: utf-8 -*-

import tushare as ts
import csv
import os
import time
import pandas as pd
import numpy as np

class 股市数据():

    def __init__(self):
        pass

    #=================================================================================#
    #                              下载各类市场数据方法                                 #
    #=================================================================================#
    def 下载基本信息(self):
        文件路径名 = './股票数据/基本信息/基本信息.csv'
        if not os.path.exists(文件路径名) or not self.是否收盘后数据(文件路径名):
            ts.get_stock_basics().to_csv('./股票数据/基本信息/基本信息.csv')

    def 下载收盘行情(self):
        """
        获取每日收盘行情
        DataFrame
        code 代码, name 名称, p_change 涨幅%,
        price 现价, change 涨跌, open 今开, high 最高,
        low 最低, preprice 昨收, pe 市盈(动),
        volratio 量比, turnover 换手%, range 振幅%%,
        volume 总量, selling 内盘, buying 外盘,
        amount 总金额, totals 总股本(万), industry 细分行业,
        area 地区, floats 流通股本(万), fvalues 流通市值,
        abvalues AB股总市值, avgprice 均价, strength 强弱度%,
        activity 活跃度, avgturnover 笔换手, attack 攻击波%,
        interval3 近3月涨幅 ，interval 近6月涨幅
        """
        文件路径名 = './股票数据/基本信息/收盘行情.csv'
        if not os.path.exists(文件路径名) or not self.是否收盘后数据(文件路径名):
            ts.get_day_all().to_csv(文件路径名)

    def 下载板块数据(self):
        # 获取不同分类数据
        ts.get_industry_classified().to_csv('./股票数据/基本信息/行业分类.csv')
        ts.get_concept_classified().to_csv('./股票数据/基本信息/概念分类.csv')
        ts.get_area_classified().to_csv('./股票数据/基本信息/地域分类.csv')
        ts.get_sme_classified().to_csv('./股票数据/基本信息/中小板.csv')
        ts.get_gem_classified().to_csv('./股票数据/基本信息/创业板.csv')
        ts.get_st_classified().to_csv('./股票数据/基本信息/风险警示板.csv')
        ts.get_hs300s().to_csv('./股票数据/基本信息/沪深300.csv')
        ts.get_sz50s().to_csv('./股票数据/基本信息/上证50.csv')
        ts.get_zz500s().to_csv('./股票数据/基本信息/中证500.csv')

    def 下载K线数据(self):
        pass

    #=================================================================================#
    #                            下载交易软件所需各类数据的方法                          #
    #=================================================================================#
    def 生成板块数据(self, 板块名, 股票列表):
        '''
            对输入板块文件中的所有股票，按照代码在收盘数据文件中进行查找，然后再将查找到的
        最新收盘数据写入新的文件。注意：新文件会覆盖原文件。
        '''
        收盘数据 = pd.read_csv('./股票数据/基本信息/收盘行情.csv', encoding="gbk")  #读收盘数据
        with open('./股票数据/板块分类/'+板块名+'.csv', 'w', newline='') as csvfile: #新建板块数据文件
            文件索引 = csv.writer(csvfile)
            文件索引.writerow(收盘数据.columns.values.tolist()[1:])  #在新建板块数据文件中写入列名
            for row in range(len(股票列表)):
                文件索引.writerow((收盘数据[收盘数据.code == 股票列表[row]]).iloc[0])

    def 获取板块分类(self, 板块文件名):
        # # 由于每个板块数据中的DataFrame数据索引名不同，不能用pd.read_csv的列索引读取文件
        # with open("./板块分类/" + 板块文件名 + ".csv", "r") as csvfile:
        #     文件索引 = csv.reader(csvfile)
        #     板块名 = []
        #     next(文件索引)
        #     for i in 文件索引:
        #         板块名.append(i[3])
        #     return list(set(板块名))
        板块数据 = pd.read_csv('./股票数据/板块分类/'+板块文件名+'.csv', encoding='gbk', names=['序号','代码','名称','分类'],skiprows=1)
        return list(set(板块数据.分类))

    def 获取板块数据(self, 板块文件名):
        板块数据 = pd.read_csv('./股票数据/板块分类/'+板块文件名+'.csv', encoding='gbk')[['code','name','p_change','price','industry','fvalues','abvalues','turnover','volratio','pe','activity','attack']]
        板块数据.columns = ['代码','名称','涨幅%','现价','行业','流值(亿)','总值(亿)','换手%','量比','市盈','活跃度','攻击波']
        return 板块数据


    def 获取板块股票代码(self, 板块名):
        文件路径名 = './股票数据/基本信息/' + 板块名 + '.csv'
        return pd.read_csv(文件路径名, encoding="gbk").code     #读板块数据

    #=================================================================================#
    #                                      其它方法                                    #
    #=================================================================================# 
    def 代码格式化(self, 股票代码):
        if len(股票代码) == 6:
            return 股票代码
        else:
            return '0'*(6-len(股票代码)) + 股票代码


    def 是否收盘后数据(self, 文件路径名):
        '''
            判断数扰文件是否是在收盘后下载的。判断方法是将文件创建时间与当时收盘
        时间相比，若晚于收盘时间，则为最新的文件。
        '''
        文件修改时间 = time.localtime(os.path.getmtime(文件路径名))
        当前时间 = time.localtime()
        收盘时间 = time.struct_time(当前时间[: 3]+(15, 00, 00)+当前时间[6 :])
        return time.mktime(文件修改时间) > time.mktime(收盘时间)       

if __name__ == "__main__":
    pass
    数据 = 股市数据()
    # 下载板块数据()
    # ts.get_day_all().to_csv('./股票数据/收盘行情.csv')
    # 下载收盘数据()
    数据.生成板块数据('自选股', 数据.获取板块股票代码('自选股'))
    数据.获取板块分类("概念分类")
        # 获取板块分类('概念分类')
