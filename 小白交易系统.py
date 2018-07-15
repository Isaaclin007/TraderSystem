# -*- coding: UTF-8 -*-
import sys,os,csv,time,datetime,urllib,wx,wx.grid
import pandas as pd
import numpy as np
import tushare as ts

from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib.finance as mpf
from matplotlib.widgets import AxesWidget

# 全程初始化
sys._enablelegacywindowsfsencoding()

# 定义主菜单类
class 小白交易系统框架(wx.Frame):
    def __init__(self):
        wx.Frame.__init__(self, None, -1, "小白交易系统", size=(-1, -1),
                          style=wx.DEFAULT_FRAME_STYLE ^ (wx.RESIZE_BORDER | wx.MAXIMIZE_BOX
                                                          ) | wx.MAXIMIZE)
        # 增加菜单
        self.菜单条 = wx.MenuBar()
        菜单 = wx.Menu()
        菜单项 = 菜单.Append(-1, "& 退出")
        self.菜单条.Append(菜单, "& 文件")
        self.SetMenuBar(self.菜单条)
        self.Bind(wx.EVT_MENU, self.OnCloseMe, self.菜单条)
        self.__数据 = 股市数据()
        self.列排序标志号 = [0, 0]

        #=========================================================================#
        #                        生成交易系统所需各控件                           #
        #=========================================================================#
        #====================生成交系统主面板Panel===================
        self.交易系统Panel = wx.Panel(self, -1, size=(-1, -1))

        # =================生成交易系统主面板快捷键Button============
        self.数据下载Button = wx.BitmapButton(
            self.交易系统Panel, -1, bitmap=wx.Bitmap("下载.ico", wx.BITMAP_TYPE_ICO))
        self.前进Button = wx.BitmapButton(
            self.交易系统Panel, -1, bitmap=wx.Bitmap("test3.ico", wx.BITMAP_TYPE_ICO))
        self.后退Button = wx.BitmapButton(
            self.交易系统Panel, -1, bitmap=wx.Bitmap("test3.ico", wx.BITMAP_TYPE_ICO))
        self.播放Button = wx.BitmapButton(
            self.交易系统Panel, -1, bitmap=wx.Bitmap("test3.ico", wx.BITMAP_TYPE_ICO))
        self.暂停Button = wx.BitmapButton(
            self.交易系统Panel, -1, bitmap=wx.Bitmap("test3.ico", wx.BITMAP_TYPE_ICO))

        #==============生成左侧股票板块与选股策略TreeCtrl============
        self.选股策略树TreeCtrl = wx.TreeCtrl(self.交易系统Panel, -1, (0, 0), (300, -1),
                                         wx.TR_HIDE_ROOT | wx.TR_HAS_BUTTONS | wx.TR_LINES_AT_ROOT)
        # self.选股策略树TreeCtrl = wx.TreeCtrl(self.交易系统Panel, -1,  wx.DefaultPosition, wx.DefaultSize, wx.TR_HIDE_ROOT | wx.TR_HAS_BUTTONS | wx.TR_LINES_AT_ROOT)
        # 设置树颜色
        self.选股策略树TreeCtrl.SetForegroundColour(wx.YELLOW)  # 设置字体颜色
        self.选股策略树TreeCtrl.SetBackgroundColour(wx.BLACK)  # 设置背景颜色
        self.选股策略树TreeCtrl.SetFont(
            wx.Font(10, 70, 90, 90, False, wx.EmptyString))
        self.选股策略TreeCtrl初始化()

        #==========================生成数据浏览区Grid=========================
        self.数据浏览Grid = wx.grid.Grid(self.交易系统Panel, -1, (-1, -1), (1200, 400))
        self.显示数据 = 数据表('自选股')
        self.数据浏览Grid.SetTable(self.显示数据, True)
        self.数据浏览Grid.EnableEditing(False)
        self.数据浏览Grid.HideRowLabels()
        self.数据浏览Grid.HideColLabels ()
        self.数据浏览Grid.EnableGridLines(False)
        # self.数据浏览Grid.SetDefaultCellAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTER)
        self.数据浏览Grid.SetDefaultCellBackgroundColour(wx.BLACK)
        self.数据浏览Grid.SetDefaultCellFont(
            wx.Font(10, 70, 90, 90, False, wx.EmptyString))
        self.数据浏览Grid.SetDefaultCellTextColour(wx.WHITE)

        #========================生成信息提示窗口TextCtrl=========================
        self.信息提示TextCtrl = wx.TextCtrl(
            self.交易系统Panel, -1, size=(-1, -1), style=wx.TE_LEFT | wx.TE_MULTILINE | wx.TE_READONLY)
        self.信息提示TextCtrl.SetBackgroundColour(wx.BLACK)
        self.信息提示TextCtrl.SetForegroundColour(wx.YELLOW)  # 设置字体颜色
        self.信息提示TextCtrl.SetFont(
            wx.Font(12, 70, 90, 90, False, wx.EmptyString))

        #===========================生成图形窗口=============================
        # 生成图形窗口1
        self.图形窗口1 = 图形显示面板(self.交易系统Panel)
        # 生成图形1控制按键
        self.分时线1Button = wx.Button(
            self.交易系统Panel, wx.ID_ANY, u"分时线", wx.DefaultPosition, size=(-1, 25))
        self.五分钟线1Button = wx.Button(
            self.交易系统Panel, wx.ID_ANY, u"5分钟线", wx.DefaultPosition, size=(-1, 25))
        self.十五分钟线1Button = wx.Button(
            self.交易系统Panel, wx.ID_ANY, u"15分钟线", wx.DefaultPosition, size=(-1, 25))
        self.日线1Button = wx.Button(
            self.交易系统Panel, wx.ID_ANY, u"日线", wx.DefaultPosition, size=(-1, 25))
        self.历史涨幅分布1Button = wx.Button(
            self.交易系统Panel, wx.ID_ANY, u"历史涨幅", wx.DefaultPosition, size=(-1, 25))

        # 生成图形窗口2
        self.图形窗口2 = 图形显示面板(self.交易系统Panel)
        # self.图形窗口1Fig = Figure(facecolor = '0.6')
        # self.图形窗口2 = FigureCanvas(self.交易系统Panel, -1, self.图形窗口1Fig)
        # 生成图形2控制按键
        self.分时线2Button = wx.Button(
            self.交易系统Panel, wx.ID_ANY, u"分时线", wx.DefaultPosition, size=(-1, 25))
        self.五分钟线2Button = wx.Button(
            self.交易系统Panel, wx.ID_ANY, u"5分钟线", wx.DefaultPosition, size=(-1, 25))
        self.十五分钟线2Button = wx.Button(
            self.交易系统Panel, wx.ID_ANY, u"15分钟线", wx.DefaultPosition, size=(-1, 25))
        self.日线2Button = wx.Button(
            self.交易系统Panel, wx.ID_ANY, u"日线", wx.DefaultPosition, size=(-1, 25))
        self.历史涨幅分布2Button = wx.Button(
            self.交易系统Panel, wx.ID_ANY, u"历史涨幅", wx.DefaultPosition, size=(-1, 25))

        #=========================================================================#
        #                        生成交易系统所需各Sizer                          #
        #=========================================================================#
        #===========================生成快捷键Sizer============================#
        self.快捷键Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.快捷键Sizer.Add((10, -1), 0)
        self.快捷键Sizer.Add(self.数据下载Button, 0, wx.RIGHT, 5)
        self.快捷键Sizer.Add(self.前进Button, 0, wx.RIGHT, 5)
        self.快捷键Sizer.Add(self.后退Button, 0, wx.RIGHT, 5)
        self.快捷键Sizer.Add(self.播放Button, 0, wx.RIGHT, 5)
        self.快捷键Sizer.Add(self.暂停Button, 0, wx.RIGHT, 5)

        #=========================生成图形显示区Sizer===========================#
        # 生成图形1控制按键Sizer
        self.图形1控制按键Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.图形1控制按键Sizer.Add(self.分时线1Button, 0, wx.RIGHT, 0)
        self.图形1控制按键Sizer.Add(self.五分钟线1Button, 0, wx.RIGHT, 0)
        self.图形1控制按键Sizer.Add(self.十五分钟线1Button, 0, wx.RIGHT, 0)
        self.图形1控制按键Sizer.Add(self.日线1Button, 0, wx.RIGHT, 0)
        self.图形1控制按键Sizer.Add(self.历史涨幅分布1Button, 0, wx.RIGHT, 0)
        # 生成图形2控制按键Sizer
        self.图形2控制按键Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.图形2控制按键Sizer.Add(self.分时线2Button, 0, wx.RIGHT, 0)
        self.图形2控制按键Sizer.Add(self.五分钟线2Button, 0, wx.RIGHT, 0)
        self.图形2控制按键Sizer.Add(self.十五分钟线2Button, 0, wx.RIGHT, 0)
        self.图形2控制按键Sizer.Add(self.日线2Button, 0, wx.RIGHT, 0)
        self.图形2控制按键Sizer.Add(self.历史涨幅分布2Button, 0, wx.RIGHT, 0)

        # 生成图形显示区1Sizer
        self.图形显示区1Sizer = wx.BoxSizer(wx.VERTICAL)
        self.图形显示区1Sizer.Add(self.图形1控制按键Sizer, 0, wx.EXPAND)
        self.图形显示区1Sizer.Add(self.图形窗口1, 1, wx.EXPAND | wx.ALL)
        # 生成图形显示区2Sizer
        self.图形显示区2Sizer = wx.BoxSizer(wx.VERTICAL)
        self.图形显示区2Sizer.Add(self.图形2控制按键Sizer, 0, wx.EXPAND)
        self.图形显示区2Sizer.Add(self.图形窗口2, 1, wx.EXPAND | wx.ALL)
        # 生成图形显示区Sizer
        self.图形显示区Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.图形显示区Sizer.Add(self.图形显示区1Sizer, 1, wx.EXPAND | wx.ALL, 2)
        self.图形显示区Sizer.Add(self.图形显示区2Sizer, 1, wx.EXPAND | wx.ALL, 2)

        #=========================生成设置与列表区Sizer===========================#
        # 生成设置与列表区Sizer
        self.生成设置与列表区Sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.生成设置与列表区Sizer.Add(self.选股策略树TreeCtrl, 0, wx.EXPAND | wx.LEFT, 2)
        self.生成设置与列表区Sizer.Add(self.数据浏览Grid, 1, wx.EXPAND)
        self.生成设置与列表区Sizer.Add(self.信息提示TextCtrl, 1, wx.EXPAND)

        #=========================将生成交易系统Sizer===========================#
        # 生成交易系统Sizer
        self.交易系统Sizer = wx.BoxSizer(wx.VERTICAL)
        self.交易系统Sizer.Add(self.快捷键Sizer, 0, wx.EXPAND)
        self.交易系统Sizer.Add(self.生成设置与列表区Sizer, 0, wx.EXPAND)
        self.交易系统Sizer.Add(self.图形显示区Sizer, 1, wx.EXPAND)

        # 将生成交易系统Sizer
        self.交易系统Panel.SetSizer(self.交易系统Sizer)
        self.交易系统Panel.Fit()

        #=========================================================================#
        #                              绑定按键事件                               #
        #=========================================================================#
        self.数据下载Button.Bind(wx.EVT_LEFT_DOWN, self.数据下载ButtonOnLeftDown)


        self.选股策略树TreeCtrl.Bind(wx.EVT_LEFT_DCLICK, self.选股策略树OnLeftDClick)
        self.数据浏览Grid.Bind(wx.grid.EVT_GRID_SELECT_CELL,self.数据浏览GridOnLeftClick)
        self.数据浏览Grid.Bind(wx.grid.EVT_GRID_CELL_LEFT_DCLICK,self.数据浏览GridOnLeftDClick)
        # ==============绑定图形框上的按键事件==============
        self.十五分钟线2Button.Bind(wx.EVT_LEFT_DCLICK,self.十五分钟线2ButtonLeftDClick)



    #=================================定义其它函数=======================================#
    def 选股策略TreeCtrl初始化(self):
        root = self.选股策略树TreeCtrl.AddRoot("选股池与策略")
        板块分类 = self.选股策略树TreeCtrl.AppendItem(root, "板块分类")
        技术指标 = self.选股策略树TreeCtrl.AppendItem(root, "技术指标")
        选股策略 = self.选股策略树TreeCtrl.AppendItem(root, "选股策略")

        # 增加板块数据
        板块项 = ["自选股", "策略选股", "创业板", "中小板", "主板", "概念分类", "地域分类"]
        for s in 板块项:
            col_temp = self.选股策略树TreeCtrl.AppendItem(板块分类, s)
            if s == "概念分类":
                概念分类项 = self.__数据.获取板块分类("概念分类")
                for s1 in 概念分类项:
                    self.选股策略树TreeCtrl.AppendItem(col_temp, s1)
            if s == "地域分类":
                地域分类项 = self.__数据.获取板块分类("地域分类")
                for s1 in 地域分类项:
                    self.选股策略树TreeCtrl.AppendItem(col_temp, s1)
        self.选股策略树TreeCtrl.Expand(板块分类)

        # 增加技术指标类型
        技术指标项 = ["MACD", "KDJ", "趋势线"]
        for s in 技术指标项:
            self.选股策略树TreeCtrl.AppendItem(技术指标, s)
        self.选股策略树TreeCtrl.Expand(技术指标)

        选股策略项 = ["底背离", "均线多头排列", "底部放量突破"]
        # 增加选股策略
        for s in 选股策略项:
            选股略分时 = self.选股策略树TreeCtrl.AppendItem(选股策略, s)
            self.选股策略树TreeCtrl.AppendItem(选股略分时, "15F线")
            self.选股策略树TreeCtrl.AppendItem(选股略分时, "日线")
        self.选股策略树TreeCtrl.Expand(选股策略)

    #============================定义事件函数=================================#
    def 选股策略树OnLeftDClick(self, event):
        选中条目 = self.选股策略树TreeCtrl.GetItemText(self.选股策略树TreeCtrl.GetSelection())
        self.信息提示TextCtrl.AppendText('选择   ' + 选中条目 + '\n')
        self.__数据.生成板块数据(选中条目,self.__数据.获取板块股票代码(选中条目))
        self.显示数据 = 数据表(选中条目)
        self.数据浏览Grid.SetTable(self.显示数据, True)
        self.数据浏览Grid.Refresh()

    def 数据浏览GridOnLeftClick(self, event):
        self.显示数据.HihgtLight(event.GetRow())
        self.数据浏览Grid.Refresh()

    def 数据浏览GridOnLeftDClick(self, event):
        选中行 = event.GetRow()
        选中列 = event.GetCol()

        self.信息提示TextCtrl.AppendText(str(选中列) + '\n')
        #双击列标签时，按照双击的列值进行排序
        if 选中行 == 0:
            if  选中列 in range(3,13):
                if self.列排序标志号[0] == 选中列:
                   self.列排序标志号[1] = (self.列排序标志号[1] + 1) % 3
                else:
                    self.列排序标志号[0] = 选中列
                    self.列排序标志号[1] = 1
                self.显示数据.SortCol(选中列,self.列排序标志号[1])
                self.msg = wx.grid.GridTableMessage(self.显示数据, wx.grid.GRIDTABLE_REQUEST_VIEW_GET_VALUES)
                self.数据浏览Grid.ProcessTableMessage(self.msg)
                self.数据浏览Grid.Refresh()
        #双击股票列表时，按照显示股票K线值
        else:
            self.选中代吗 = self.显示数据.GetValue(选中行, 1)
            self.个股数据 = self.__数据.获取日线数据(self.选中代吗)
            self.图形窗口1.设置股票数据(self.个股数据)
            self.图形窗口1.画K线图()
            self.图形窗口1.显示数据框()
            self.图形窗口1.画成交量()
            self.图形窗口1.显示定位线()
            self.图形窗口1.刷新窗口()
            # self.画K线图(self.图形窗口2Fig,'窗口2')

    def 十五分钟线2ButtonLeftDClick(self,event):
        self.个股数据 = self.__数据.获取个股分时数据(self.选中代吗,'15')
        self.图形窗口2.设置股票数据(self.个股数据)
        self.图形窗口2.画K线图()
        self.图形窗口2.显示数据框()
        self.图形窗口2.画成交量()
        self.图形窗口2.显示定位线()
        self.图形窗口2.刷新窗口()

    def 数据下载ButtonOnLeftDown(self,event):
        # self.信息提示TextCtrl.AppendText('very good!\n')

        开始时间 = time.time()
        StockCode = list(__数据.下载股市基本信息().index)

        # 产生序列
        下载队列 = multiprocessing.Queue()
        self.信息提示TextCtrl.AppendText('全部下载数共有%i条:'%下载队列.qsize())

        for code in StockCode:
            下载队列.put(code)

        下载进程队列 = []
        for i in range(10):
            data_qeue = 下载队列.get()
            print("正在获取%s;数据还有%s条:" %(data_qeue,下载队列.qsize()))
            下载进程 = threading(target=__数据.下载股票数据,args=(data_qeue,))
            # 下载进程 = multiprocessing.Process(target=下载股票数据,args=data_qeue)
            下载进程.start()
            下载进程队列.append(下载进程)

        for p in 下载进程队列:
            p.join()

        结束时间 = time.time()
        self.信息提示TextCtrl.AppendText('下载共用时%f秒'%(结束时间-开始时间))



    def OnCloseMe(self, event):
        self.Close(True)

class 图形显示面板(wx.Panel):
    def __init__(self,parent):  
        # wx.Panel.__init__(self,parent=parent, id=-1,size=(600, 1800)) 
        wx.Panel.__init__(self,parent=parent, id=-1) 
        self.Figure = Figure(facecolor = '0.6',figsize=(9.8,5.5))
        # =====================================生成K线Axe并设置属性======================================#
        self.K线ax = self.Figure.add_axes([0.05, 0.255, 0.95, 0.73], label='K线图', facecolor = 'k')

        # =====================================生成成交量窗口并设置属性======================================#
        self.指标ax = self.Figure.add_axes([0.05, 0.05, 0.95, 0.2], label='成交量', facecolor = 'k')
        self.FigureCanvas = FigureCanvas(self,-1,self.Figure)
        self.上涨颜色 = 'red'
        self.下跌颜色 = 'deepskyblue'
        self.平盘颜色 = '0.7'
        self.透明度 = 1
        cid = self.FigureCanvas.mpl_connect('button_press_event', self.鼠标单击)

    def 设置股票数据(self, 个股数据):
        数据长度 = min(200,len(个股数据.date))
        self.个股数据 = 个股数据[0:数据长度]
        self.行情长度 = len(self.个股数据.date)       # 所有数据的长度，就是天数
        # ==========================================生成涨跌序列============================================#
        self.上涨= np.array( [ True if po < pc and po != None else False for po, pc in zip(self.个股数据.open, self.个股数据.close)] )        # 标示出该天股价日内上涨的一个序列
        self.下跌= np.array( [ True if po > pc and po != None else False for po, pc in zip(self.个股数据.open, self.个股数据.close)] )        # 标示出该天股价日内下跌的一个序列
        self.平盘= np.array( [ True if po == pc and po != None else False for po, pc in zip(self.个股数据.open, self.个股数据.close)] )      # 标示出该天股价日内走平的一个序列
        self.横坐标序列= np.arange(self.行情长度,0,-1)    # X 轴上的 index，一个辅助数据

    def 画K线图(self):
        self.K线ax .cla()
        # =========================================设置K线窗口属性=========================================#
        self.K线ax.set_xlim(0,self.行情长度+20)
        self.K线ax.get_xaxis().set_visible(False)   #设置K线图X轴不可见
        self.K线ax.yaxis.grid(True, 'major', color='white', linestyle='--', linewidth=0.3)
        # ============================================读数据============================================#
        开盘价= list(self.个股数据.open)
        收盘价= list(self.个股数据.close)
        最高价= list(self.个股数据.high)
        最低价= list(self.个股数据.low)

        mpf.candlestick2_ohlc(self.K线ax,开盘价,最高价,最低价,收盘价,width=1,colorup='red',colordown='green')

    def 画成交量(self):
        # ============================================读成交量数据============================================#
        成交量= np.array(self.个股数据.volume)
        成交量起点= np.zeros(self.行情长度)
        # ============================================画成交量图============================================#
        if True in self.上涨:
            self.指标ax.vlines(self.横坐标序列[self.上涨], 成交量起点[self.上涨], 成交量[self.上涨], color=self.上涨颜色, linewidth=2, label='_nolegend_', alpha = self.透明度)
        if True in self.下跌:
            self.指标ax.vlines(self.横坐标序列[self.下跌], 成交量起点[self.下跌], 成交量[self.下跌], color=self.下跌颜色, linewidth=2, label='_nolegend_', alpha = self.透明度)
        if True in self.平盘:
            self.指标ax.vlines(self.横坐标序列[self.平盘], 成交量起点[self.平盘], 成交量[self.平盘], color=self.平盘颜色, linewidth=2, label='_nolegend_', alpha = self.透明度)
        self.指标ax.set_xlim(0,self.行情长度+2)

    def 显示数据框(self):
        # =================================设置显示字体=================================
        plt.rcParams['font.sans-serif']=['Microsoft YaHei'] #用来正常显示中文标签
        plt.rcParams['axes.unicode_minus']=False #用来正常显示负号
        显示文本 = '时间\n%s\n%s\n开盘\n%3.2f\n收盘\n%3.2f\n最高\n%3.2f\n最低\n%3.2f\n涨幅\n%3.2f\n换手\n%3.2f%%' % ('0000','00-00',0,0,0,0,0,0)

        self.数据框 = self.K线ax.text(0.008, 0.985,显示文本, horizontalalignment='left',verticalalignment='top',transform=self.K线ax.transAxes,bbox=dict(facecolor='0.6', alpha=0.8))

    def 鼠标单击(self,event):
        数值 = self.个股数据.loc[(self.行情长度-int(event.xdata)),:]
        显示文本 = '时间\n%s\n%s\n开盘\n%3.2f\n收盘\n%3.2f\n最高\n%3.2f\n最低\n%3.2f\n涨幅\n%3.2f%%\n换手\n%3.2f%%' % (数值.date[0:4],数值.date[5::],数值.open,数值.close,数值.high,数值.low,float(数值.p_change),数值.turnover)
        self.数据框.set_text(显示文本)
        self.FigureCanvas.draw()

    def 显示定位线(self):
        self.定位线 = 画十字光标((self.K线ax, self.指标ax), useblit=True, color='yellow', lw = 0.8)

    def 刷新窗口(self):
        self.FigureCanvas.draw()

class 数据表(wx.grid.GridTableBase):
    __选中行 = []
    __排序标志 = {0:'原始', 1:'涨幅' ,2:'跌幅'}
    __配色方案 = {'黄渐变':[[90,255,114],[255,231,17],[255,161,21], [255,62,21],[217,24,193]],
                '红绿渐变':[[26,219,49],[185,229,26],[207,168,21],[229,126,21],[219,47,25]],
                '红':[[255,156,17],[255,52,20],[243,23,255]],
                '绿':[[22,255,244],[31,255,41],[24,69,255]]}

    def __init__(self, 板块文件名):
        wx.grid.GridTableBase.__init__(self)
        self.__数据 = 股市数据()
        #从文件中读取数据并改列名
        self.__数据表原始 = self.__数据.获取板块数据(板块文件名)

        #新生成数据表内容用于排序显示
        self.__数据表 = self.__数据表原始

    def GetNumberRows(self):
        return self.__数据表.shape[0]+1

    def GetNumberCols(self):
        return self.__数据表.shape[1]+1

    def IsEmptyCell(self, row, col):
        return True

    def GetValue(self, row, col):#为网格提供数据
        if row == 0:
            return self.__数据表.columns[col-1]
        else:
            # 设置序号列显示内容
            if col == 0:
                return row
            # 设置代码列显示内容
            if col == 1:
                return self.__数据.代码格式化(str(self.__数据表.iloc[row-1, 0]))
            # 设置名称|行业列显示内容
            if col in [2, 5]:
                return self.__数据表.iloc[row-1, col-1]
            # 设置涨幅|现价|流通市值|总市值|换手|量比|市盈|活跃度|攻击波等列显示内容
            if col in range(3, 13):
                return ('{:.2f}'.format(self.__数据表.iloc[row-1, col-1]))

    def GetAttr(self, row, col, kind):
        __temp = self.GetValue(row, col)
        __cell_attr = wx.grid.GridCellAttr()
        __cell_attr.SetAlignment(wx.ALIGN_RIGHT, wx.ALIGN_CENTER )
        if row == 0:
            if col in [1, 2, 5]:
                __cell_attr.SetAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER )
        else:
            # 设置代码列排列方式
            if col == 1:
                __cell_attr.SetAlignment(wx.ALIGN_CENTER, wx.ALIGN_CENTER )

            # 设置名称列显示颜色排列方式
            if col ==2 :
                color = wx.RED if (float(self.GetValue(row, 3)) > 0) else wx.GREEN
                __cell_attr.SetTextColour(color)
                __cell_attr.SetAlignment(wx.ALIGN_LEFT, wx.ALIGN_CENTER )

            # 设置涨幅列显示颜色
            if col == 3:
                __temp = float(__temp)
                if float(self.GetValue(row, 3)) > 0:
                    __color_index = [__temp <= 3, 3 < __temp <= 6, 6 < __temp]
                    __cell_attr.SetTextColour(self.__配色方案['红'][__color_index.index(True)])
                else:
                    __color_index = [-3 <= __temp, -6 <= __temp < -3, __temp < -6]
                    __cell_attr.SetTextColour(self.__配色方案['绿'][__color_index.index(True)])

            # 设置现价列显示颜色
            if col == 4:
                color = wx.RED if (float(self.GetValue(row, 3)) > 0) else wx.GREEN
                __cell_attr.SetTextColour(color)

            # 设置行业列显示颜色
            if col == 5:
                __cell_attr.SetTextColour([12, 217, 215])

            # 设置流通市值|总市值列显示颜色
            if col in [6, 7]:
                __temp = float(__temp)
                __color_index = [__temp <= 30, 30 < __temp <= 50, 50 < __temp <= 100, 100 < __temp <= 200, __temp > 200]
                __cell_attr.SetTextColour(self.__配色方案['黄渐变'][__color_index.index(True)])

            # 设置换手列显示颜色
            if col == 8:
                __temp = float(__temp)
                __color_index = [__temp <= 5, 5 < __temp <= 10, 10 < __temp <= 20, 20 < __temp <= 50, __temp > 50]
                __cell_attr.SetTextColour(self.__配色方案['黄渐变'][__color_index.index(True)])

            # 设置量比列显示颜色
            if col == 9:
                __temp = float(__temp)
                __color_index = [__temp <= 1, 1 < __temp <= 3, 3 < __temp <= 6, 6 < __temp <= 11, __temp > 10]
                __cell_attr.SetTextColour(self.__配色方案['黄渐变'][__color_index.index(True)])

            # 设置市盈列显示颜色
            if col == 10:
                __temp = float(__temp)
                __color_index = [__temp <= 30, 30 < __temp <= 60, 50 < __temp <= 100, 100 < __temp <= 200, __temp > 200]
                __cell_attr.SetTextColour(self.__配色方案['黄渐变'][__color_index.index(True)])

            # 设置活跃度列显示颜色
            if col == 11:
                pass
            # 设置攻击波列显示颜色
            if col == 12:
                pass

        if row == self.__选中行:
            __cell_attr.SetBackgroundColour([0,0,160])
        return __cell_attr

    def SetValue(self, row, col, value):#给表赋值
        pass

    def HihgtLight(self, row):
        self.__选中行 = row

    def SortCol(self, col, sortindex):
        self.__排序标志 = {0:'原始', 1:'涨幅' ,2:'跌幅'}
        if self.__排序标志[sortindex] == '原始':
            self.__数据表 = self.__数据表原始
        else:
            flag = [True, False][self.__排序标志[sortindex] == '涨幅']
            self.__数据表 = self.__数据表.sort_values(by=self.__数据表.columns[col-1], ascending=flag)

class 画十字光标(AxesWidget):
    def __init__(self, axes, horizOn=True, vertOn=True, useblit=False,
                 **lineprops):
        self.canvas = axes[0].figure.canvas
        self.axes = axes
        self.horizOn = horizOn
        self.vertOn = vertOn
        self.cids = []
        xmin, xmax = axes[0].get_xlim()
        ymin, ymax = axes[0].get_ylim()
        xmid = 0.5 * (xmin + xmax)
        ymid = 0.5 * (ymin + ymax)

        self.visible = True
        self.useblit = useblit and self.canvas.supports_blit
        self.background = None
        self.needclear = False

        if self.useblit:
            lineprops['animated'] = True

        if vertOn:
            self.vlines = [ax.axvline(xmid, visible=False, **lineprops)
                           for ax in axes]
        else:
            self.vlines = []

        if horizOn:
            self.hlines = [ax.axhline(ymid, visible=False, **lineprops)
                           for ax in axes]
        else:
            self.hlines = []

        self.connect_event('motion_notify_event', self.onmove)
        self.connect_event('draw_event', self.clear)
        self.connect_event('figure_leave_event', self.leave)

    def leave(self,event):
        for line in self.vlines + self.hlines:
            line.set_visible(False)
        self.canvas.draw()

    def clear(self, event):
        if self.ignore(event):
            return
        if self.useblit:
            self.background = (
                self.canvas.copy_from_bbox(self.canvas.figure.bbox))
        for line in self.vlines + self.hlines:
            line.set_visible(False)

    def onpress(self, event):
        ex=event.xdata#这个数据类型是numpy.float64
        ey=event.ydata#这个数据类型是numpy.float64
        if ex  and ey :
            self.set_text('%10.5f,%10.5f' % (float(ex),float(ey)))
        self.canvas.draw_idle()

    def onmove(self, event):
        if event.inaxes == self.axes[0]:
            self.axes1flag = 1
            self.axes2flag = 0
        if event.inaxes == self.axes[1]:
            self.axes1flag = 0
            self.axes2flag = 1
        if self.ignore(event):
            return
        if event.inaxes is None:
            return
        if not self.canvas.widgetlock.available(self):
            return
        self.needclear = True
        if not self.visible:
            return
        if self.vertOn:
            for line in self.vlines:
                line.set_xdata((event.xdata, event.xdata))
                line.set_visible(self.visible)
        if self.horizOn:
            for line in self.hlines:
                line.set_ydata((event.ydata, event.ydata))
                line.set_visible(self.visible)
        self._update()

    def _update(self):
        if self.useblit:
            if self.background is not None:
                self.canvas.restore_region(self.background)
            if self.vertOn:
                for ax, line in zip(self.axes, self.vlines):
                    ax.draw_artist(line)
            if self.axes1flag:
                self.axes[0].draw_artist(self.hlines[0])
            if self.axes2flag:
                self.axes[1].draw_artist(self.hlines[1])
            self.canvas.blit(self.canvas.figure.bbox)
        else:
            self.canvas.draw_idle()

class 股市数据():
    def __init__(self):
        self.下载收盘行情()

    #=================================================================================#
    #                              下载各类市场数据方法                                 #
    #=================================================================================#
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
            self.收盘数据 = ts.get_day_all()
            self.收盘数据.to_csv(文件路径名)
        else:
            self.收盘数据 = pd.read_csv(文件路径名, encoding="gbk")

    def 下载基本信息(self):
        文件路径名 = './股票数据/基本信息/基本信息.csv'
        if not os.path.exists(文件路径名) or not self.是否收盘后数据(文件路径名):
            ts.get_stock_basics().to_csv('./股票数据/基本信息/基本信息.csv')

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

    def 获取个股分时数据(self, 代码, 周期):
        #======================获取个股数据===========================
        文件路径名 = './股票数据/' + 周期 + 'F线/' + 代码 + '.csv'
        print(文件路径名)
        if not os.path.exists(文件路径名) or not self.是否收盘后数据(文件路径名):
            # 下载个股数据，直到完成
            while True:
                分时数据 = ts.get_k_data(代码,ktype=周期)
                print(分时数据)
                分时数据 = 分时数据.reindex(分时数据.index[::-1])
                分时数据.to_csv(文件路径名)
                if not 分时数据.empty: break
        分时数据 = pd.read_csv(文件路径名, encoding="gbk")
        return 分时数据

    def 获取日线数据(self, 代码, 起始日期='',结束日期 = time.strftime("%Y%m%d")):
        文件路径名 = './股票数据/日线/'+ 代码 +'.csv'
        # ==========根据文件是否存及是否是最新数据判断下载数据的日期=========
        # 如果文件不存在，则下载日期为全部数据
        if not os.path.exists(文件路径名):
            if 起始日期 is None:
                起始日期 = 结束日期[0:3]+str(int(结束日期[3])-2)+结束日期[4:]
            日线数据 = self._网易下载日线数据(代码,起始日期,结束日期)
            日线数据.to_csv(文件路径名,index=False)
        # 如果文件存在，但不是最新的收盘后数据，则下载日期为原有文件中的最后一日的下一日
        elif not self.是否收盘后数据(文件路径名):
            原数据 = pd.read_csv(文件路径名,encoding="gbk")

            # =============起始日期为原数据中最后日期再加1天=================
            起始日期 = datetime.datetime.strptime(原数据.head(1).date.tolist()[0],'%Y-%m-%d')
            起始日期 = (起始日期 + datetime.timedelta(days=1)).strftime('%Y%m%d')
            新数据 = self._网易下载日线数据(代码,起始日期,结束日期)
            新数据.append(原数据).to_csv(文件路径名,index=False)

        return pd.read_csv(文件路径名,encoding="gbk")

    def _网易下载日线数据(self,code, start,end):
        """
        通过网易财经获取到日线历史数据
        各列内容：date 日期，close 收盘价，high 最高价, low 最低价，
                 l_close 前收盘，change 涨跌，p_change 涨幅，
                 turnover 换手，volume 成交量，amount 成交额
        """
        #==========================爬网下数据=========================

        if code[0:3] in ['000','002','300']: code ='1'+code
        if code[0:3] in ['600','601','603']: code ='0'+ code
        url='http://quotes.money.163.com/service/chddata.html?code=%s&start=%s&end=%s&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;TURNOVER;VOTURNOVER;VATURNOVER'%(code,start,end)
        req=urllib.request.Request(url,headers={
            'Connection': 'Keep-Alive',
            'Accept': 'text/html, application/xhtml+xml, */*',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
        })
        opener=urllib.request.urlopen(req)
        page=opener.read().decode('gb2312') #该段获取原始数据
        page=page.split('\r\n')  #按行分隔

        col_info=page[0].split(',')   #各列的含义
        index_data=page[1:]     #真正的数据

        #================改列名==================
        col_info[col_info.index('日期')]='date'
        col_info[col_info.index('股票代码')]='code'
        col_info[col_info.index('名称')]='name'
        col_info[col_info.index('收盘价')]='close'
        col_info[col_info.index('最高价')]='high'
        col_info[col_info.index('最低价')]='low'
        col_info[col_info.index('开盘价')]='open'
        col_info[col_info.index('前收盘')]='l_close'
        col_info[col_info.index('涨跌额')]='change'
        col_info[col_info.index('涨跌幅')]='p_change'
        col_info[col_info.index('换手率')]='turnover'
        col_info[col_info.index('成交量')]='volume'
        col_info[col_info.index('成交金额')]='amount'

        #===================去掉代码前的“ ' ”==================
        # index_data=[x.replace("'",'') for x in index_data]

        #====================每一行以","分割====================
        index_data=[x.split(',') for x in index_data]

        #===================最后一行为空，需要去掉=================
        index_data=index_data[0:index_data.__len__()-1]

        #=====================转为DateFrame===================
        day_data = pd.DataFrame(index_data,columns=col_info)

        #================删除code列=================
        del day_data['code']

        #================删除含有None的行的数据并返回值=================
        return  day_data[(True-day_data['change'].isin(['None']))]

    #=================================================================================#
    #                            下载交易软件所需各类数据的方法                          #
    #=================================================================================#
    def 生成板块数据(self, 板块名, 股票列表):
        '''
            对输入板块文件中的所有股票，按照代码在收盘数据文件中进行查找，然后再将查找到的
        最新收盘数据写入新的文件。注意：新文件会覆盖原文件。
        '''
        # self.收盘数据 = pd.read_csv('./股票数据/基本信息/收盘行情.csv', encoding="gbk")  #读收盘数据
        with open('./股票数据/板块分类/'+板块名+'.csv', 'w', newline='') as csvfile: #新建板块数据文件
            文件索引 = csv.writer(csvfile)
            文件索引.writerow(self.收盘数据.columns.values.tolist()[1:])  #在新建板块数据文件中写入列名
            for row in range(len(股票列表)):
                文件索引.writerow((self.收盘数据[self.收盘数据.code == 股票列表[row]]).iloc[0])

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


    def 获取板块股票代码 (self, 板块名):
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
    app = wx.App()
    主框架 = 小白交易系统框架()
    主框架.Show(True)
    app.MainLoop()

