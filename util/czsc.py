# -*- coding: utf-8 -*-  
#---History:
# -----1 Convert from caomaolufei's code to python
#     2 fix bug in initFx: kx.fxqj = self.kxData[i-1].low
#    
import pandas as pd
from util.draw import *


TICK_DATA, MIN1_DATA, MIN5_DATA, MIN15_DATA, MIN30_DATA, MIN60_DATA,\
DAY_DATA, WEEK_DATA, MONTH_DATA, MULTI_DATA = ([] for i in range(2,12))                   

class STKDATA(object):
    def __init__(self):
        self.m_time = 0
        self.m_fOpen = 0       #开盘
        self.m_fHigh = 0       #最高
        self.m_fLow  = 0          #最低
        self.m_fClose = 0       #收盘
        self.m_fVolume = 0       #成交量
        self.m_fAmount = 0       #成交额
        self.m_wAdvance = 0       #上涨家数(仅大盘有效)
        self.m_wDecline = 0      #下跌家数(仅大盘有效)
        
class CALCINFO(object):
    def __init__(self, df, datatype):
        self.m_pData = self._initStockData(df)
        self.m_nNumData = len(self.m_pData)
        self.m_dataType = datatype
#        if interval == 60:
#            self.m_dataType = MIN1_DATA
#        elif interval == 300:
#            self.m_dataType = MIN5_DATA
#        elif interval == 1800:
#            self.m_dataType = MIN30_DATA
#        elif interval == 3600:
#            self.m_dataType = MIN60_DATA
#        elif interval == 3600*24:
#            self.m_dataType = DAY_DATA
        
    
    def _initStockData(self, df):
        stockData = []
        for i in range(len(df)):
            stk = STKDATA()
            stk.m_time = df.index[i]
            stk.m_fClose = df.ix[i]['close']
            stk.m_fHigh = df.ix[i]['high']
            stk.m_fOpen = df.ix[i]['open']
            stk.m_fLow = df.ix[i]['low']
            stk.m_fVolume = df.ix[i]['volume']
            stockData.append(stk)
        return stockData
        
       

class ckx(object):
    def __init__(self):
        self.no, self.rhigh, self.rlow, self.high, self.low, \
        self.flag, self.fxqj, self.dir, self.bi,self.duan = ([] for _ in range(10))
#        int no;                // K线序号 从1开始是
#        float rhigh;        // 高值
#        float rlow;            // 低值
#        float high;        //包含处理后的高值
#        float low;        //包含处理后的低值
#        int    flag;            //1顶 -1底 0 非顶底
#        float fxqj;        // 分型区间 如果为顶底 记录区间边界
#        int dir;            //K线方向 1上 -1下 2 上包含 -2 下包含
#        int bi;                //笔 1上 -1下 2 上包含 -2 下包含
#        int duan;            //段 1上 -1下 2 上包含 -2 下包含


class cbi(object):
    def __init__(self):
        self.no, self.noh, self.nol, self.high, self.low, self.dir, self.flag, self.qx = ([] for _ in range(8))
#        int no; // 序号
#        int noh; // 高点K线编号
#        int nol;  // 低点K线编号
#        float high; // 高点
#        float low; // 低点
#        int dir; // 方向 方向 1上 -1下 2 上包含 -2 下包含
#        int flag; // 1顶 -1底
#        int qk; // 特征1 2 之间是否存在缺口 


class cduan(object):
    def __init__(self):
        self.no, self.noh, self.nol, self.high, self.low, self.flag, self.binum = ([] for _ in range(7))
#        int no; // 序号
#        int noh; // 高点K线编号
#        int nol;  // 低点K线编号
#        float high; // 高点
#        float low; // 低点
#        int flag; //  1顶 -1底
#        int binum; // 包含几笔


class czhongshu(object):
    def __init__(self):
        self.no, self.duanno, self.flag, self.ksno, self.jsno, self.znnum, \
        self.zg, self.zd, self.gg, self.dd, self.zz = ([] for _ in range(11))
#        int no; // 序号
#        int duanno; // 段序号
#        int flag; // 走势方向 1上 -1下
#        int ksno; // zg所在K线NO (有zg必有zd)
#        int jsno; // zd所在K线NO
#        int znnum; // 包含zn数
#        float zg; // ZG=min(g1、g2)
#        float zd; // ZD=max(d1、d2)
#        float gg; // GG=max(gn);
#        float dd; // dd=min(dn);
#        float zz; // 震荡中轴(监视器)

DIR_0 = 0
DIR_UP = 1
DIR_DN = -1
DIR_SBH = -2
DIR_XBH = 2
    
QK_Y = 0
QK_N = 1
class ChanlunCore:    
    
    def __init__(self):
        
        self.kxData = []
        self.xbData = []
        self.sbData = []
        self.dData = []
        self.zsData = []
        
        self.biQuekou = 0.0
        self.firstDuanDir = DIR_0
    

        
    
    def initBiQK(self, pData):
        qk = 0.005
        if pData.m_nNumData == 0:
            return
        
        if pData.m_dataType == MIN1_DATA:
            self.biQuekou = qk
        elif pData.m_dataType == MIN5_DATA:
            self.biQuekou = qk*3
        elif pData.m_dataType == MIN15_DATA:
            self.biQuekou = qk*6
        elif pData.m_dataType == MIN30_DATA:
            self.biQuekou = qk*9
        elif pData.m_dataType == MIN60_DATA:
            self.biQuekou = qk*18
        elif pData.m_dataType == DAY_DATA:
            self.biQuekou = qk*30
        elif pData.m_dataType == WEEK_DATA:
            self.biQuekou = qk*90
        elif pData.m_dataType == MONTH_DATA:
            self.biQuekou = qk*250
        else:
            self.biQuekou = qk*1000
    
    def initKx(self, pData):
        
        if len(self.kxData) != 0:
            self.kxData = []
        if pData.m_nNumData > 0:
            self.initBiQK(pData)
            h, l, h1, l1 = (0, 0, 0, 0)
            dir = 0
            tj_jg = 5
            
            #处理包含关系
            for i in range(pData.m_nNumData):
                h = pData.m_pData[i].m_fHigh
                l = pData.m_pData[i].m_fLow
                
                if(dir > DIR_0):
                    if (h >= h1 and l <= l1) or (h <= h1 and l>= l1):
                        h = max(h, h1)                        
                        l = max(l, l1)
                        dir = DIR_SBH
                elif dir < DIR_0:
                    if (h >= h1 and l <= l1) or (h <= h1 and l >= l1):
                        h = min(h, h1)
                        l = min(h, h1)
                        dir = DIR_XBH
                
                if h > h1 and l > l1:
                    dir = DIR_UP
                elif h<h1 and l < l1:
                    dir = DIR_DN
                
                kx = ckx()
                kx.low = l
                kx.high = h
                kx.dir = dir
                kx.flag = DIR_0
                kx.fxqj = 0
                kx.bi = DIR_0
                kx.duan = DIR_0
                kx.no = i + 1
                
                kx.rhigh = h
                kx.rlow = l
                h1 = h
                l1 = l
                
                self.kxData.append(kx)
    def initFX(self):
        kxnum = len(self.kxData)
            
        if kxnum <= 5:
            return
    
        i = 0
        j = 0
        k = 0
    
        h, h11, h12, h13, h21 = (0 for i in range(5))
        l, l11, l12, l13, l21 = (0 for i in range(5))
        p31, p32, p33, quekou = (0 for i in range(4))
        tjg1, tjd1, tjc = (False for i in range(3))
            
        jg = 0
        jg2 = 0 # 至少5根K线
        gdnum = 0  #顶底数量
    
        tj_jg = 3
        tj_jg2 = 3
        #if (pData.m_dataType > WEEK_DATA) tj_jg = 4
    
        kx, kxt, kxl, kxlg, kxld = (ckx() for i in range(5))
            
        kx = self.kxData[0]
        kx = self.getCKX(2)
    
        # 标出顶底分型
        i = 2 
        while i < len(self.kxData)-1:
                
			#i = i + 1
            kx = self.kxData[i]
            jg = jg + 1    		
                
            #if(DIR_DN==kx.dir || DIR_UP==kx.dir) jg2++; # 处理包含关系后的间隔

    
            h11, h12, h13, h21, l11, l12, l13,  l21, p31, p32, p33 = ([0]*11)
                
            tjg1 = False
            tjd1 = False
    
            h = kx.high
            l = kx.low
                
            j = i
            kxt = kx            
            # 前第一个高点
            while True:
                j = j - 1
                if j>0:
                    kxt = self.kxData[j]
                    h11 = kxt.high
                    l11 = kxt.low
                if h11 == h and j>0:
                    continue
                else:
                    break
                # 前第二个高点
                j = j - 1
                if j>0:
                    kxt = self.kxData[j]
                    h12 = kxt.high;
            # 前第三个高点
                j = j - 1
                if j>0:
                    kxt = self.kxData[j]
                    h13 = kxt.high;
            k = i
            kxt = kx
            # 后第一个高点
            while True:                    
                k = k + 1
                if k<kxnum-1:
                    kxt = self.kxData[k]
                    h21 = kxt.high;    
                    l21 = kxt.low
                if h21 == h and k<kxnum-1:
                    continue
                else:
                    break
               
                
            # 顶判断 缠论定义 以及 最高>顶分的前2根K线的高点
            tjg1 = h>h11 and h>h21 and h>h12 and h>h13 
                
                # 非顶
            if not tjg1:
                j = i
                kxt = kx;            
                # 前第一个低点
                while True:
                    j = j - 1
                    if j>0:
                        kxt = self.kxData[j]
                        h11 = kxt.high;    
                        l11 = kxt.low
                    if l11 == l and j>0:
                        continue
                    else:
                        break
                   
                    # 前第2个低点
                j = j - 1
                if j>0:
                    kxt = self.kxData[j]
                    h12 = kxt.high;    
                    l12 = kxt.low
                    # 前第3个低点
                j = j - 1
                if j>0:
                    kxt = self.kxData[j]
                    h13 = kxt.high
                    l13 = kxt.low
                k = i
                kxt = kx
                # 后第一个低点
                while True:
                    k = k + 1
                    if k<kxnum-1:
                        kxt = self.kxData[k]
                        h21 = kxt.high;    
                        l21 = kxt.low
                    if l21 == l and k<kxnum-1:
                        continue
                    else:
                        break
                   
                    
                # 底判断 缠论定义 以及 最低<底分的前2根K线的低点
                tjd1 = l<l11 and l<l21 and l<l13 and l<l12
                # 非顶
                
                
                # 标出顶底分型
            if tjg1 or tjd1:
                if 0 == gdnum:
                    # 第一个分型
                    if tjg1:
                        kx.fxqj = self.kxData[i-1].low
                        kx.flag = DIR_UP
                        kxlg = kx
                    elif tjd1:
                        kx.fxqj = self.kxData[i-1].high
                        kx.flag = DIR_DN
                        kxld = kx
                    kxl = kx
                    gdnum = gdnum + 1
                    jg = 1
                    jg2 = 1
                else:
                    if tjg1:
                        # 计算边界
                        kxt = kx
                        kxt = self.kxData[i-1]
                        p31 = kxt.low
                        kx.fxqj = p31
                        # 如果存在缺口 缺口边界就未本K线的顶底 (上涨缺口)
                            
                        if i>1:
                            j = i - 1
                            #quekou = pData.m_pData[i].m_fLow - pData.m_pData[j].m_fHigh
                            quekou = kx.rlow - kxt.rhigh
                            if quekou >= self.biQuekou:
                                kx.fxqj = kx.low
                            # 顶接顶 价高为新顶
                        if DIR_UP == kxl.flag:
                            if kx.high > kxl.high:
                                kx.flag = DIR_UP
                                gdnum = gdnum + 1
                                jg = 1
                                #jg2 = 1
                                    
                                kxl.flag = DIR_SBH
                                kxl = kx;        
                                kxlg = kx
                            else:
                                pass
                                    #kx.flag = DIR_SBH
                        else:
                            # 底接顶 
                            # 包含后的K线至少3跟 构成顶分 最高值必须大于前低分高（不再顶的分型区间内）
                            if jg >= tj_jg and kx.high > kxl.fxqj and kx.fxqj > kxl.low:
                                kx.flag = DIR_UP
                                gdnum = gdnum + 1
                                jg = 1
                                jg2 = 1
                                    
                                kxl = kx
                                kxlg = kx
                            elif jg == 2:
                                # 1 存在缺口(上涨) 2 大于前顶
                                    
                                if i>1 and quekou  >= self.biQuekou:
                                    # 存在缺口 顶分成立 前底分也有效 
                                    kx.flag = DIR_UP
                                    gdnum = gdnum + 1
                                    jg = 1
                                    jg2 = 1
                                        
                                    kxl = kx
                                    kxlg = kx
                                elif gdnum>=4 and quekou  < self.biQuekou and kx.high > kxlg.high:
                                    # 大于前顶， 前底失效 前顶失效
                                    kx.flag = DIR_UP
                                    kxlg.flag = DIR_SBH
                                    kxld.flag = DIR_0
    
                                    gdnum = gdnum + 1
                                    jg = 1
                                    jg2 = 1
                                        
                                    kxl = kx
                                    kxlg = kx
                    elif tjd1:
                        # 计算边界
                        kxt = kx
                        kxt = self.kxData[i-1]
                        p31 = kxt.high
                        kx.fxqj = p31
                        # 如果存在缺口 缺口边界就未本K线的顶底 (下跌缺口)
                        if i>1:
                            j = i - 1
                            #quekou = -(pData.m_pData[i].m_fHigh - pData.m_pData[j].m_fLow)
                            quekou = -(kx.rhigh - kxt.rlow)
                            if quekou>=self.biQuekou:
                                kx.fxqj = kx.high
                        # 底接底 价低为新底
                        if DIR_DN == kxl.flag:
                            if kx.low < kxl.low:
                                kx.flag = DIR_DN
                                gdnum = gdnum + 1
                                jg = 1
                                jg2 = 1
                                    
                                kxl.flag = DIR_XBH
                                kxl = kx
                                kxld = kx
                            else:
                                pass
                                    #kx.flag = DIR_XBH
                        else:
                            # 顶接底 包含后的K线至少3 构成底分 最低值必须小于前顶低 不再顶区间内
                            if jg >= tj_jg and kx.low < kxl.fxqj and kx.fxqj < kxl.high:
                                kx.flag = DIR_DN
                                gdnum = gdnum + 1
                                jg = 1
                                jg2 = 1
                                    
                                kxl = kx
                                kxld = kx
                            elif jg == 2:
                                # 1 存在缺口(下跌) 2 小于前底
                                if i>1 and quekou  >= self.biQuekou:
                                    # 存在缺口 顶分成立 前底分也有效 
                                    kx.flag = DIR_DN
                                    gdnum = gdnum + 1
                                    jg = 1
                                    jg2 = 1
                                        
                                    kxl = kx
                                    kxld = kx
                                elif gdnum>=4 and quekou  < self.biQuekou  and kx.low < kxld.low:
                                    # 大于前顶， 前底失效 前顶失效
                                    kx.flag = DIR_DN
                                    kxld.flag = DIR_XBH
                                    kxlg.flag = DIR_0
                                        
                                    gdnum = gdnum + 1
                                    jg = 1
                                    jg2 = 1
                                        
                                    kxl = kx
                                    kxld = kx
            #} # end 顶底
            else:
                pass
                
                    # do nothing
                #} # end else  非顶底
            i = i + 1
    
    
            #} # end for 标出顶底分型
    
            
            # 当下 
        kxt = self.kxData[-1]
        kxt = self.kxData[-2]; # 最后一根K线
        # 非顶 非底 用于判断当下 顶底未成之前
        # 创新高 低 必然产生新的高点和低点 去掉前一个高低点 注意必须是高高 低低
        if DIR_UP == kxl.flag:
            if kxt.high > kxl.high:
                kxl.flag = DIR_SBH
        elif DIR_DN == kxl.flag:
            if kxt.low < kxl.low:
                kxl.flag = DIR_XBH
                    
                    
    def getCKX(self, num):
        return self.kxData[num]

#
#list<ckx> ChanlunCore::getCkxData()
#    return kxData
#list<cbi> ChanlunCore::getXbData()
#    return xbData
#list<cbi> ChanlunCore::getSbData()
#    return sbData
#list<cduan> ChanlunCore::getDuanData()
#    return dData
#list<czhongshu> ChanlunCore::getZsData()
#    return zsData
    def initBi(self):
        
        kxnum = len(self.kxData)
    
        if kxnum>5:
            i = 0
            binum = 0
            bignum = 0
            bidnum = 0
            jg = 1
            jg2 = 2
    
    
            tj_jg = 5
            tj_jg2 = 4
    
            fx, fxl, fxt, fxlg, fxld = (ckx() for i in range(5))
    
            quekou = 0
    
            fx = self.kxData[0]
            fx = self.getCKX(2)
    
            # 标出笔
            i = 2
            #for(i=2; i<kxnum-2; i++, fx++)
            while i<kxnum-2: 
                fx = self.kxData[i]               
                jg = jg + 1
                if DIR_UP == fx.dir or DIR_DN == fx.dir:
                    jg2 = jg + 1; # 包含处理
    
    
                if binum > 0:
                    if DIR_UP == fx.flag:
                        # 底接顶
                        if DIR_DN == fxl.bi:
                            # 如果存在缺口 当成一天K线 jg 和JG2 都+1 (上涨)
#                            /*
#                            quekou = (pData.m_pData[i].m_fLow - pData.m_pData[i-1].m_fHigh)
#                            if quekou>=biQuekou:
#                                jg2++; 
#                                jg = jg+2
#                            }*/
    
                            if jg >= tj_jg and jg2 >= tj_jg2:
                                fx.bi = DIR_UP
                                
                                binum = binum + 1
                                jg = 1
                                jg2 = 1
                                fxl = fx
                                bignum = bignum + 1
                                fxlg = fx
                            else:
                                # 包含处理 取高中的高点低中的低点
                                if bignum>0:
                                    if fx.high > fxlg.high:
                                        fx.bi = DIR_UP
                                        fxlg.bi = DIR_SBH
                                        fxld.bi = DIR_XBH; # add
                                        
                                        binum = binum + 1
                                        jg = 1
                                        jg2 = 1
                                        fxl = fx
                                        bignum = bignum + 1
                                        fxlg = fx
                        elif DIR_UP == fxl.bi:
                            # 顶接顶 
                            # 取高顶
                            if fx.high > fxl.high:
                                fx.bi = DIR_UP
                                fxl.bi = DIR_SBH
                                binum = binum +1
                                jg = 1
                                jg2 = 1
                                fxl = fx
                                bignum = bignum + 1
                                fxlg = fx
                    #} # end if DIR_UP == fx.flag:
                    elif DIR_DN == fx.flag:
                        # 顶接底
                        if DIR_UP == fxl.bi:
#                            /*
#                            # 如果存在缺口 当成一天K线 jg 和JG2 都+1 (下跌)
#                            quekou = -(pData.m_pData[i].m_fHigh - pData.m_pData[i-1].m_fLow)
#                            if quekou>=biQuekou:
#                                jg2++; 
#                                jg = jg+2
#                            }*/
    
                            if jg >= tj_jg and jg2 >= tj_jg2:
                                fx.bi = DIR_DN
                                
                                binum = binum + 1
                                jg = 1
                                jg2 = 1
                                fxl = fx
                                bidnum = bidnum + 1
                                fxld = fx
                            else:
                                # 包含处理 取低中的低点
                                if bidnum>0:
                                    if fx.low < fxld.low:
                                        fx.bi = DIR_DN
                                        fxld.bi = DIR_XBH
                                        fxlg.bi = DIR_SBH; # add
                                        
                                        binum = binum + 1
                                        jg = 1
                                        jg2 = 1
                                        fxl = fx
                                        bidnum = bidnum + 1
                                        fxld = fx
                        elif DIR_DN == fxl.bi:
                            # 底接底 
                            # 取低底
                            if fx.low < fxl.low:
                                fx.bi = DIR_DN
                                fxl.bi = DIR_XBH
                                binum = binum + 1
                                jg = 1
                                jg2 = 1
                                fxl = fx
                                bidnum  = bidnum + 1
                                fxld = fx
                    #} # end elif DIR_DN == fx.flag:
                #} # end binum>0
                else:
                    # 第一笔
                    if DIR_UP == fx.flag:
                        fx.bi = DIR_UP
                        fxl = fx
                        binum = binum + 1
                        jg = 1
                        jg2 = 1
                        bignum = bignum + 1
                        fxlg = fx
                    elif DIR_DN == fx.flag:
                        fx.bi = DIR_DN
                        fxl = fx
                        binum = binum + 1
                        jg = 1
                        jg2 = 1
                        bidnum = bidnum + 1
                        fxld = fx
                i = i + 1
            #} # end 标出笔
    
    
            # 当下 
            fxt = self.kxData[-1]
            fxt = self.kxData[-2] # 最后一根K线
            # 非顶 非底 用于判断当下 顶底未成之前
            # 创新高 低 必然产生新的高点和低点 去掉前一个高低点 注意必须是高高 低低
            if DIR_UP == fxl.bi:
                if fxt.high > fxl.high:
                    fxl.bi = DIR_SBH
            elif DIR_DN == fxl.bi:
                if fxt.low < fxl.low:
                    fxl.bi = DIR_XBH
    def test(self):
        pass
    def initTZXL(self):
        
        if len(self.xbData) != 0:
            self.xbData = []
        if len(self.sbData):
            self.sbData = []
        
        kx = ckx()
        kxl = ckx()
        
        kxnum = len(self.kxData)
        i = 0
        begin = 2
        binum = 0
        sbnum = 0
        xbnum = 0
        
        kx = self.getCKX(begin)
        
        # 查找所有特征序列
        i = begin
        while i < kxnum - 1:
            kx = self.kxData[i]
            if DIR_UP == kx.bi:
                if binum > 0:
                    if DIR_DN == kxl.bi:
                        # 底接顶
                        binum = binum + 1
                        sbnum = sbnum +1
                        tz = cbi()
                        tz.dir = DIR_UP; # 向上笔
                        tz.high = kx.high
                        tz.noh = kx.no
                        tz.low = kxl.low
                        tz.no = binum
                        tz.nol = kxl.no
                        tz.flag = DIR_0
                        tz.qk = QK_N
                        # 向上笔 
                        self.sbData.append(tz)
                        #    bList.push_back(tz)
                        
                        kxl = kx
                else:
                    # 第一笔
                    kxl = kx
                    binum = binum + 1
            elif DIR_DN == kx.bi:
                if binum > 0:
                    # 顶接底
                    if DIR_UP == kxl.bi:
                        binum = binum + 1
                        xbnum = xbnum + 1
                        tz = cbi()
                        tz.dir = DIR_DN; # 向下笔
                        tz.high = kxl.high
                        tz.noh = kxl.no
                        tz.low = kx.low
                        tz.nol = kx.no
                        tz.no = binum
                        tz.flag = DIR_0
                        tz.qk = QK_N
                        # 向下笔 
                        self.xbData.append(tz)
                        #    bList.push_back(tz)
                        
                        kxl = kx
                else:
                    # 第一笔
                    kxl = kx
                    binum = binum + 1
            i = i + 1
        
        #} # END 查找所有特征序列
    def findTZG(self, fromNo):
        if len(self.xbData) == 0:
            return None
        ret = None

        kxnum = len(self.kxData)
        if fromNo >= kxnum:
            return ret
        

        bnum = len(self.xbData)
        if bnum >= 3:
            #bi, bit, btz2 = (self.xbData[-1] for i in range(3))
            #tz1 = cbi()
            
            #tz1, tz2, tz3 = (cbi() for i in range(3)) # 特征元素1 2

            doTZ1 = True
            doTZ2 = False
            doTZ3 = False
            i=0
            
            xbindex = 0

            for bi in self.xbData:
                if bi.noh < fromNo:
                    continue
                if doTZ1:
                    # 特征1
                    tz1 = bi
                    doTZ1 = False
                    doTZ2 = True
                    continue
#                    /*
#                    if 0 == i:
#                        tz1 = (*bi)
#                        doTZ1 = false
#                        doTZ2 = true
#                        continue
#                    else
#                        bit = bi
#                        bit--
#                        tz1 = (*bit)
#                        doTZ1 = false
#                        doTZ2 = true
#                    */
                    # ok 开始TZ2
                elif doTZ2:
                    # 特征2
                    if bi.high > tz1.high and bi.low > tz1.low:
                        # 上涨
                        btz2 = bi
                        tz2 = bi
                        doTZ2 = False
                        doTZ3 = True
                        continue
                        # ok 开始TZ3
                    elif bi.high < tz1.high and bi.low < tz1.low:
                        # 下跌
                        tz1 = bi
                        # 继续TZ2
                    else:
                        #TZ1 TZ2 处理在同一特征序列里的包含关系
                        if tz1.high > bi.high:
                            # 前包后
                            tz1.low = bi.low
                            tz1.nol = bi.nol
                        else:
                            # 后包前 (笔破坏不处理)
                            btz2 = bi
                            tz2 = bi
                            doTZ2 = False
                            doTZ3 = True
                            continue
#                        /*
#                        # 存在包含关系 2中情况
#                        # tz1 取高点的高点 低点的高点
#                        if tz1.high > bi.high:
#                            # 前包后
#                            tz1.low = bi.low
#                            tz1.nol = bi.nol
#                        else
#                            # 后包前
#                            tz2 = (*bi)
#                            tz2.low = tz1.low
#                            tz1 = tz2
#                        # 继续TZ2*/
                elif doTZ3:
                    # 特征3
                    if bi.high < tz2.high and bi.low < tz2.low:
                        # 下跌 顶分成立
                        #标记 tz2
                        #btz2.flag = DIR_UP
                        # 如果存在缺口
                        if tz2.low > tz1.high:
                            btz2.qk = QK_Y
                        return btz2
                        #break; # 找到了结束
                        # OK
                    elif bi.high > tz2.high and bi.low > tz2.low:
                        # 上涨
                        tz1 = tz2
                        tz2 = bi
                        # 继续TZ3
                    else:
                        # 特征3 和 特征2 存在包含关系
                        # tz1 不变 tz2 包含处理
                        if tz2.high > bi.high:
                            # 前包后
                            tz2.low = bi.low
                            tz2.nol = bi.nol
                        else:
                            # 后包前
                            btz2 = bi
                            tz3 = bi
                            tz3.low = tz2.low
                            tz2 = tz3
                        # 继续TZ3
            #} # end for 
        #} # end (bnum >= 3)
        
        return ret
    def findTZD(self, fromNo):
        ret = None
        
        if len(self.sbData) == 0:
            return ret
        
    
        kxnum = len(self.kxData)
        if fromNo >= kxnum: 
            return ret
        
        bnum = len(self.sbData)
        if bnum >= 3:
#            BIIT bi, btz2=sbData.end(), bit
#            cbi tz1, tz2, tz3; # 特征元素1 2
    
            doTZ1 = True
            doTZ2 = False 
            doTZ3 = False
            i=0
    
            for bi in self.sbData:
                if bi.nol < fromNo:
                    # do nothing
                    continue
                if doTZ1:
                    # 特征1
                    tz1 = bi
                    doTZ1 = False
                    doTZ2 = True
                    continue
                    
#                    /*
#                    if 0 == i:
#                        tz1 = (*bi)
#                        doTZ1 = false
#                        doTZ2 = true
#                        continue
#                    else
#                        bit = bi
#                        bit--
#                        tz1 = (*bit)
#                        doTZ1 = false
#                        doTZ2 = true
#                    }*/
    
                    # ok 开始TZ2
                elif doTZ2:
                    # 特征2
                    if bi.high < tz1.high and bi.low < tz1.low:
                        # 下跌
                        btz2 = bi
                        tz2 = bi
                        doTZ2 = False
                        doTZ3 = True
                        continue
                        # ok 开始TZ3
                    elif bi.high > tz1.high and bi.low > tz1.low:
                        # 上涨
                        tz1 = bi
                        # 继续TZ2
                    else:
                        #TZ1 TZ2 处理在同一特征序列里的包含关系
                        if  tz1.low < bi.low:
                            # 前包后
                            tz1.high = bi.high
                            tz1.noh = bi.noh
                        else:
                            # 后包前 (笔破坏不处理)
                            btz2 = bi
                            tz2 = bi
                            doTZ2 = False
                            doTZ3 = True
                            continue
#                        /*
#                        # tz2 tz1 存在包含关系 2种情况
#                        # tz1 取高点的低点 低点的低点
#                        if  tz1.low < bi.low:
#                            # 前包后
#                            tz1.high = bi.high
#                            tz1.noh = bi.noh
#                        else
#                            # 后包前
#                            tz2 = (*bi)
#                            tz2.high = tz1.high
#                            tz1 = tz2
#                        # 继续TZ2
#                        */
                elif doTZ3:
                    # 特征3
                    if bi.high > tz2.high and bi.low > tz2.low:
                        # 上涨 底分成立
                        #标记 tz2
                    #    btz2.flag = DIR_DN
                        # 如果存在缺口
                        if tz2.high > tz1.low:
                            btz2.qk = QK_Y
                        return btz2
                        #break; # 找到了结束
                        # OK
                    elif bi.high < tz2.high and bi.low < tz2.low:
                        # 下跌
                        tz1 = tz2
                        tz2 = bi
                        # 继续TZ3
                    else:
                        # 特征3 和 特征2 存在包含关系
                        # tz1 不变 tz2 包含处理
                        if tz2.low < bi.low:
                            # 前包后
                            tz2.high = bi.high
                            tz2.noh = bi.noh
                        else:
                            # 后包前
                            btz2 = bi
    
                            tz3 = bi
                            tz3.high = tz2.high
                            tz2 = tz3
                        # 继续TZ3
                i = i + 1
        #} # end (bnum >= 3)
    
        return ret
    def initDuan(self):
        
        kxnum = len(self.kxData)
        
        if kxnum>21:
            self.initTZXL();    
            
            dnum, gnum, next, num = (0 for i in range(4))
            tzd, tzg, tzl = (cbi() for i in range(3))
            
            # 查找剩余的顶底知道结束
            isOver = False
    
            while True:
                dnum = kxnum
                gnum = kxnum
                
    
                tzd = self.findTZD(next)
                tzg = self.findTZG(next)
    
                if None != tzd:
                    dnum = tzd.nol
                if None != tzg:
                    gnum = tzg.noh
                if dnum < gnum:
                    # 底 tzd
                    if num > 0:
                        if DIR_UP == tzl.flag:
                            # 顶接底
                            tzd.flag = DIR_DN
                            tzl = tzd
                            num = num + 1
                        elif DIR_DN == tzl.flag:
                            # 底接底 保留低的底
                            if tzd.low < tzl.low:
                                tzd.flag = DIR_DN
                                tzl.flag = DIR_XBH
                                tzl = tzd
                                num = num + 1
                    else:
                        # 第一个顶OR底
                        tzd.flag = DIR_DN
                        tzl = tzd
                        num = num + 1
                    next = dnum
                #} # end if dnum < gnums
                elif dnum > gnum:
                    # 顶 tzg
                    if num > 0:
                        if DIR_DN == tzl.flag:
                            # 底接顶
                            tzg.flag = DIR_UP
                            tzl = tzg
                            num = num + 1
                        elif DIR_UP == tzl.flag:
                            # 顶接顶 取高的顶
                            if tzg.high > tzl.high:
                                tzg.flag = DIR_UP
                                tzl.flag = DIR_SBH
                                tzl = tzg
                                num = num + 1
                    else:
                        # 第一个顶OR底
                        tzg.flag = DIR_UP
                        tzl = tzg
                        num = num + 1
                    next = gnum
    
                #} # end if dnum > gnum + 1:
                else:
                    #结束
                    # do nothing
                    isOver = True
                if isOver:
                    break
            #} while(!isOver)
            
            kx = ckx() 
            kxl = ckx()
            
            # 标记段
            # 底
            for tzd in self.sbData:
                if DIR_DN == tzd.flag:
                    num = tzd.nol - 1
                    kx = self.getCKX(num)
                    kx.duan = DIR_DN
            # 顶
            for tzg in self.xbData:
                if DIR_UP == tzg.flag:
                    num = tzg.noh - 1
                    kx = self.getCKX(num)
                    kx.duan = DIR_UP
        #} # end kxnum>21
    def initDuanList(self):
        if len(self.dData):
            self.dData = []
        kx = ckx()
        kxl = ckx()
        
        kxnum = len(self.kxData)
        i = 0
        begin = 2
        num = 0
        
        kx = self.getCKX(begin)
        
        # 查找所有段
        i = begin
        while i < kxnum - 1:
            kx = self.kxData[i]
            if DIR_UP == kx.duan:
                if num > 0:
                    if DIR_DN == kxl.duan:
                        # 底接顶
                        num = num + 1
                        d = cduan()
                        d.flag = DIR_UP
                        d.no = num
                        d.noh = kx.no
                        d.high = kx.high
                        d.nol = kxl.no
                        d.low = kxl.low
                        self.dData.append(d)
                        
                        kxl = kx
                else:
                    # 第一笔
                    num = num + 1
                    kxl = kx;
            elif DIR_DN == kx.duan:
                if num > 0:
                    # 顶接底
                    if DIR_UP == kxl.duan:
                        num = num + 1
                        d = cduan()
                        d.flag = DIR_DN
                        d.no = num
                        d.noh = kxl.no
                        d.high = kxl.high
                        d.nol = kx.no
                        d.low = kx.low
                        self.dData.append(d)
                        
                        kxl = kx
                else:
                    # 第一笔
                    num = num + 1
                    kxl = kx
                    
            i = i + 1
        #} # END 查找所有段
    def findHuiTiaoZS(self, duanno, begin, end, high, low):
        if len(self.xbData) >= 2:
            zn = cbi() 
            znl = None
            zsit = czhongshu()
            findZSNew = True
            gg=0
            dd=0
            num=0
            for zn in self.xbData:
                if zn.noh > begin and zn.noh < end:
                    if num > 0:
                        if zn.low < znl.high:
                            if findZSNew:
                                gg = max(znl.high, zn.high)
                                dd = min(znl.low, zn.low)
                                if high > gg and low < dd:
                                    # ZN重叠 新中枢
                                    zs = czhongshu()
                                    zs.flag = DIR_UP
                                    zs.duanno = duanno
                                    zs.znnum = 2
                                    zs.zg = min(znl.high, zn.high)   
                                    zs.zd = max(znl.low, zn.low)
                                    zs.ksno = znl.noh
                                    zs.jsno = zn.nol
                                    zs.gg = gg
                                    zs.dd = dd
                                    zs.zz = zs.zd + (zs.zg-zs.zd)/2
    
                                    # 中枢必须全部在段内
                                    self.zsData.append(zs)
                                    findZSNew = False
                                else:
                                    findZSNew = True
                            else:
                                zsit = self.zsData[-1]
                                                 
                                if zn.low > zsit.zg or zn.high < zsit.zd:
                                    # 离开中枢
                                    findZSNew = True
                                else:
                                    # 中枢延伸
                                    zsit.jsno = zn.nol
                                    zsit.znnum = zsit.znnum + 1
                                    if zn.high > zsit.gg:
                                        zsit.gg = zn.high
                                    if zn.low < zsit.dd:
                                        zsit.dd = zn.low
                        else:
                            # 离开中枢
                            findZSNew = True
                    #}# end if num > 0:
                    else:
                        pass
                        # 如果第一笔破坏了向上段不处理
#                        /*
#                        if zn.high > low:
#                            break
#                        }*/
                    num = num + 1
                    znl = zn
                elif zn.noh >= end:
                    break
            #} # end for
    def findFanTanZS(self, duanno, begin, end, high, low):
        if len(self.sbData) >= 2:
            zn = cbi()
            znl = None
            zsit = czhongshu()
            findZSNew = True
            gg, dd, num = ([0]*3)
            for zn in self.sbData:
                if zn.nol > begin and zn.nol < end:
                    if num>0:
                        if zn.high > znl.low:
                            if findZSNew:
                                gg = max(znl.high, zn.high)
                                dd = min(znl.low, zn.low)
                                if high > gg and low < dd:
                                    # ZN重叠 新中枢
                                    zs = czhongshu()
                                    zs.flag = DIR_DN
                                    zs.duanno = duanno
                                    zs.znnum = 2
                                    zs.zg = min(znl.high, zn.high) 
                                    zs.zd = max(znl.low, zn.low) 
                                    zs.ksno = znl.nol
                                    zs.jsno = zn.noh
                                    zs.gg = gg
                                    zs.dd = dd
                                    zs.zz = zs.zd + (zs.zg-zs.zd)/2
    
                                    # 中枢必须全部在段内
                                    self.zsData.append(zs)
                                    findZSNew = False
                                else:
                                    findZSNew = True
                            else:
                                zsit = self.zsData[-1]
                                               
                                if zn.low > zsit.zg or zn.high < zsit.zd:
                                    # 离开中枢
                                    findZSNew = True
                                else:
                                    # 中枢延伸
                                    findZSNew = False
                                    zsit.jsno = zn.noh
                                    zsit.znnum = zsit.znnum + 1
                                    if zn.high > zsit.gg:
                                        zsit.gg = zn.high
                                    if zn.low < zsit.dd:
                                        zsit.dd = zn.low
                        else:
                            # 离开中枢
                            findZSNew = True
                    else:
                        pass
                        # 如果第一笔破坏了向下段不处理
#                        /*
#                        if zn.low < low:
#                            break
#                        }*/
                    num = num + 1
                    znl = zn
                elif zn.noh >= end:
                    break
            #} # end for
    def initZhongshu(self):
        if len(self.zsData) > 0:
            self.zsData = []
        
        self.initDuanList()
            
        if len(self.dData) > 0:
            dit = cduan()
            i = 0
            for dit in self.dData:
                i = i + 1
                if DIR_UP == dit.flag:
                    # 向上段
                    self.findHuiTiaoZS(i, dit.nol, dit.noh, dit.high, dit.low)
                elif DIR_DN == dit.flag:
                    # 向下段
                    self.findFanTanZS(i, dit.noh, dit.nol, dit.high, dit.low)
                    
        #} # if dData.size() > 0:
    def _getintervalfromdata(self, df):
        timeindex = df.index
        ret = DAY_DATA
        if len(df) >= 2:            
            t1 = timeindex[0]
            t2 = timeindex[1]
            timedelta = t2 - t1
            if timedelta.seconds == 60:
                ret = MIN1_DATA
            elif timedelta.seconds == 300:
                ret = MIN5_DATA
            elif timedelta.seconds == 900:
                ret = MIN15_DATA
            elif timedelta.seconds == 1800:
                ret = MIN30_DATA
            elif timedelta.seconds == 3600:
                ret = MIN60_DATA
            elif timedelta.days == 1:
                ret = DAY_DATA
            elif timedelta.days == 7:
                ret = WEEK_DATA
            elif timedelta.days> 7 and timedelta.days <= 31:
                ret = MONTH_DATA
        return ret
        
        
    def Draw(self, dc, df):
        interval = self._getintervalfromdata(df)
        calinfo = CALCINFO(df, interval)
        self.initBiQK(calinfo)
        self.initKx(calinfo)
        self.initFX()
        self.initBi()
        self.initDuan()
        self.initDuanList()
        self.initZhongshu()
        xmax, ymax = init_dc(dc)
        dc.SetPen(wx.Pen(wx.RED, 1))
        i = 0
        num = 0
        line = []
#        for i in range(len(self.kxData)):
#            kx = self.kxData[i]
#            if kx.bi == DIR_UP:
#
#                highx, highy = gethighpointfromdata(dc, df, i)
#                line.append(highx)
#                line.append(highy)
#            elif kx.bi == DIR_DN:
#                num += 1
#                lowx, lowy = getlowpointfromdata(dc, df, i)
#                line.append(lowx)
#                line.append(lowy)
#
#            if len(line) == 4:
#                dc.DrawLine(line[0], line[1], line[2], line[3])
#                tmp = []
#                tmp.append(line[2])
#                tmp.append(line[3])
#                line = tmp
                
                
        for i in range(len(self.sbData)):
            bi = self.sbData[i]
            highx, highy = gethighpointfromdata(dc, df, bi.noh-1)
            lowx, lowy = getlowpointfromdata(dc, df, bi.nol-1)
            dc.DrawLine(highx, highy, lowx, lowy)
        for i in range(len(self.xbData)):
            bi = self.xbData[i]
            highx, highy = gethighpointfromdata(dc, df, bi.noh-1)
            lowx, lowy = getlowpointfromdata(dc, df, bi.nol-1)
            dc.DrawLine(highx, highy, lowx, lowy)
            
            
            
        
        
        
                
def test():
    df = pd.DataFrame.from_csv('600016test.csv')
    calinfo = CALCINFO(df, MIN5_DATA)
    #print calinfo.m_pData
    czsc = ChanlunCore()
    czsc.initBiQK(calinfo)
    czsc.initKx(calinfo)
    czsc.initFX()
    czsc.initBi()
    print "after initBi"
    for kx in czsc.kxData:
        if kx.bi == DIR_UP or kx.bi == DIR_DN:
            print kx.bi,  " ", kx.no
    czsc.initDuan()
    print "after initDuan"
    czsc.initDuanList()
    print "bi ========================="
    for kx in czsc.kxData:
        if kx.bi == DIR_UP or kx.bi == DIR_DN:
            print kx.bi,  " ", kx.no
    print "xia bi data"
    for bi in czsc.xbData:
        print bi.no, "    ", bi.nol,"    " , bi.noh
    print "shang bi data"
    for bi in czsc.sbData:
        print bi.no, "    ", bi.nol, "    ", bi.noh
#    print len(czsc.kxData)
    print "duan=============================="
    for duan in czsc.dData:
        print duan.no, "    ", duan.noh, "    ", duan.nol
    
    print "zhongshu=========================="
    czsc.initZhongshu()
    for zs in czsc.zsData:
        print zs.no, '    ', zs.duanno,'    ', zs.flag,'    ', zs.ksno, '    ',zs.jsno, '    ', zs.znnum
#    for kx in czsc.kxData:
#        print kx.no, ' ', kx.high, ' ', kx.low, ' ', kx.rhigh, ' ', kx.rlow
     

            
if __name__ == '__main__':
    test()        
        
    
            
        





















