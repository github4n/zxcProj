#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 15:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Weixin网页版消息处理接口（功能库）--机器人类--日志
"""
import sys, os, time ,mySystem

#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类 
mySystem.Append_Us("", False) 
import myRobot, myManager_Msg
from myGlobal import gol   

    
#机器人类--聊天机器人
class myRobot_Robot(myRobot.myRobot):
    def __init__(self, usrName, usrID):
        super().__init__(usrName, usrID)
        self.doTitle = "Robot_Log"     #说明 
        self.prjName = "Robot_Log"     #功能名
        self.doCmd = "@@zxcRobot_Log"  #启动命令 
        self.msgLogs = gol._Get_Setting('manageMsgs')   #全局消息日志管理器
        
    #消息处理接口
    def _Done(self, Text, msgID = "", isGroup = False, idGroup = ""): 
        #日志记录
        #strText = Text + "--by zxcLog"
        self.msgLogs.Log(self.usrID, self.usrName, "", Text, msgID) 
        return "" 

    def _Title_User_Opened(self): 
        return "开启Robot Log..." 
        

#主启动程序
if __name__ == "__main__":
    pR = myRobot_Robot("zxc", "zxcID");
    pp = pR.Done("@@zxcRobot_Log")
    print(pp)
    print(pR.Done("Hello"))
    print(pR.Done("Test", "@zxcvbnm"))
    print(pR.Done("Bye"))

    pp = pR.Done("@@zxcRobot_Log")
    print(pp)
    time.sleep (2)
    
    #提取消息测试
    pMsg = pR.msgLogs._Find_Log("zxcID").Find("@zxcvbnm")
    print("msgID: " , pMsg.msgID, "msg: ", pMsg.msg)
