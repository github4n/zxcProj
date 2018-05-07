#-*- coding: utf-8 -*-
"""
Created on  张斌 2018-05-03 14:58:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    监听--源基类 
"""
import sys, os, time, mySystem 
import urllib, urllib.request

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.m_strFloders.append('/zxcPy.Quotation')
mySystem.m_strFloders.append('/zxcPy.Quotation/Quote_Data')
mySystem.Append_Us("", False)    
import myQuote_Data, myData_Stock, myQuote_Listener, myQuote_Source  


#行情源--新浪--Stock
class Source_Sina_Stock(myQuote_Source.Quote_Source):
    def query(self):    
        #新浪Stock接口查询
        host="http://hq.sinajs.cn/list="
        url = host + self.params
        req = urllib.request.Request(url)
        res_data = urllib.request.urlopen(req)
        res = res_data.read().decode(encoding = "gbk")
        
        #解析所有返回数据
        qd = myData_Stock.Data_Stock()
        lines = res.split('\n')
        for line in lines:
            if len(line) < 50 :
                continue
            stkid = line[13: 19]
            info = line[21:len(line)-2]
            vargs = info.split(',')
            
            qd.id = stkid
            qd.rawline = info
            qd.name = vargs[0]
            qd.openPrice = vargs[1]
            qd.preClose = vargs[2]
            qd.lastPrice = vargs[3]
            qd.highPrice = vargs[4]
            qd.lowPrice = vargs[5]
            qd.buyPrice = vargs[6]
            qd.sellPrice = vargs[7]
            qd.tradeValume = vargs[8]
            qd.tradeTurnover = vargs[9]
            qd.buy1Volume = vargs[10]
            qd.buy1Price = vargs[11]
            qd.buy2Volume = vargs[12]
            qd.buy2Price = vargs[13]
            qd.buy3Volume = vargs[14]
            qd.buy3Price = vargs[15]
            qd.buy4Volume = vargs[16]
            qd.buy4Price = vargs[17]
            qd.buy5Volume = vargs[18]
            qd.buy5Price = vargs[19]
            qd.sell1Volume = vargs[20]
            qd.sell1Price = vargs[21]
            qd.sell2Volume = vargs[22]
            qd.sell2Price = vargs[23]
            qd.sell3Volume = vargs[24]
            qd.sell3Price = vargs[25]
            qd.sell4Volume = vargs[26]
            qd.sell4Price = vargs[27]
            qd.sell5Volume = vargs[28]
            qd.sell5Price = vargs[29]
            qd.date = vargs[30]
            qd.time = vargs[31]
            
            #通知所有监听对象
            self.notifyListeners(qd)

   
#主启动程序
if __name__ == "__main__":
    stockids = 'sh600006,sh510050'
    s = Source_Sina_Stock(stockids)
    
    while True:
        s.query()
        time.sleep(3)




 