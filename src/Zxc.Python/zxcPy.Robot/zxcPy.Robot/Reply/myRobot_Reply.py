#-*- coding: utf-8 -*-
"""
Created on  张斌 2017-11-17 12:16:00 
    @author: zhang bin
    @email:  zhangbin@gsafety.com

    Python的Robot消息处理接口(文本消息)
"""
import os, threading  
import mySystem 
    
#引用根目录类文件夹--必须，否则非本地目录起动时无法找到自定义类
mySystem.Append_Us("../Prjs", False, __file__)
mySystem.Append_Us("../Roots", False, __file__)
mySystem.Append_Us("", False)    
import myWeb, myImport, myRoot, myRoot_Usr
from myGlobal import gol 


#机器人消息处理工厂类（所有消息从此处走）
class myRobot_Reply():
    def __init__(self): 
        self.usrTag = ""
        self.usrName = ""
        self.usrNameNick = ""
        self.usrReplys = myRoot_Usr.myRoot_Usrs("", "")   #消息用户集
        #self.wxDos = {}         #消息处理类
        #self.wxUser_Root = None #当前授权用户对象(避免频繁查找)
        self._Init()    #按全局权限初始
        print(">>实例消息处理工厂(%s::%s--%s)" % (self.usrName, self.usrNameNick, self.usrTag))
    def _Init(self,): 
        #初始用户全局功能权限对象 
        self.root = gol._Get_Value('rootRobot')     #权限信息
        if(self.root != None):
            self.usrName = self.root.usrName
            self.usrNameNick =self.root.usrNameNick
            self.usrTag =self.root.usrID
            self.usrReplys = myRoot_Usr.myRoot_Usrs(self.usrName, self.usrTag)   #消息用户集
        
    #处理封装返回消息(按标识内容处理)
    def Done_ByMsg(self, msg, isGroup = False):
        if(msg == None): return None

        #提取消息内容（可能随wx版本变更）
        usrName_To = msg['ToUserName']
        strText = msg['Text'] 
        idGroup = ""
        pWxdo = None 
        if(isGroup):
            idGroup = msg['User'].get('UserName',"")
            nickName = msg.get('ActualNickName',"")
            usrName = msg.get('ActualUserName',"")
        else:
            nickName = msg['User'].get('NickName',"")
            usrName = msg.get('FromUserName',"")

        #调用 
        return self.Done(usrName, nickName, strText, isGroup, idGroup)
    #按命令处理返回消息(按标识内容处理)
    def Done(self, usrID, usrName, nickName, usrPlant, strText, isGroup = False, idGroup = ""):
        #命令识别
        pWxdo = None 
        if(strText[0:2] == "@@"):
            pWxdo, pPrj, pUser = self._Create_Cmd(usrID, usrName, nickName, strText[2:], isGroup, idGroup)
            if(pWxdo != None):
                print( "--Create WxDo: %s " % pPrj.prjName)
                return pUser.Done(pWxdo, pPrj.cmdStr, isGroup, idGroup)    #直接消息处理方法调用
        else:
            self.wxRoot
            usrPlant
        #查找用户  
        pUser = self._Find_Usr(usrID, usrName, nickName, "", usrPlant)       
        if(pUser == None): return None

        #消息处理方法调用
        return pUser.Done(pWxdo, strText, isGroup, idGroup)

    #查找用户（不存在则自动创建）
    def _Find_Usr(self, usrID, usrName, usrName_Nick, usrID_sys = "", usrPlant = ""): 
        #按消息生成对应对象 
        pUser = self.root.usrInfos._Find(nickName, usrName, usrID, usrID_sys, usrPlant, False)
        if(pUser == None):      #非参与用户，于全局用户集信息提取，不存在的自动生成
            pUser = self.root.usrInfos._Find(nickName, usrName, usrID, usrID_sys, usrPlant, True)
            self.usrReplys._Add(pUser)
        return pUser
    #是否管理员账户（直接提升权限）
    def _IsRoot_Usr(self, usrName):
        pRoot = self.wxRoot.prjRoots_user.get(usrName.lower()) 
        if pRoot == None : return False
        if pRoot.prjRoot == False : return False
        return True
    #是否可启动命令用户
    def _IsEnable_Usr(self, pUser, pPrj, isGroup, pGroup = None):
        # 查找用户权限 
        bEnable = pPrj.IsRoot_user(pUser)
        if(bEnable == True): return True

        # 非功能root用户, 只有在程序运行过程中才是权限用户
        if(pPrj.IsRunning()):
            if(pPrj.IsEnable_All() == False):    #非统一启动时，需要个人启动
                if(isGroup):                     #群有效，且为设置群
                    return pPrj.IsEnable_group(pGroup)
                else:
                    return pPrj.IsEnable_one()   #单人有效



            else:           #单一启动 
                if(isGroup):
                    if pPrj.IsEnable_group() and pPrj.goupsEnable.get(idGroup, None) != None : return True
                else:
                    if(pPrj.IsEnable_one()): return True 
            return False

        
        # 提取集合权限
        pWxdo = self.wxDos.get(pPrj.cmdStr, None)
        if(pWxdo == None): return False
        
        if(pPrj.IsEnable_All()):    #系统级功能，全部用户更新
            return True
        else:
            if(isGroup):
                if pPrj.IsEnable_group() and pPrj.goupsEnable.get(idGroup, None) != None : return True
            else:
                if(pPrj.IsEnable_one()): return True 
        return False
            
    #命令处理（@@命令，一次开启，再次关闭）
    def _Create_Cmd(self, usrID, usrName, nickName, prjCmd, isGroup, idGroup):    
        #查找功能权限对象
        pPrj = self.root.rootPrjs._Find(prjCmd)
        if(pPrj == None):
            print(">>Create Prj(%s) Faield" % (prjCmd))
            return None, None, None
        if(pPrj.IsEnable() == False): return None, None, None     #必须启用

        #查找用户（功能开启全部可用则当前用户）  
        pUser = self._Find_Usr(usrID, usrName, nickName, "", usrPlant)   
        if(pUser == None): return None, None, None

        #功能权限验证 
        bEnable = self._IsEnable_Usr(pUser, pPrj, isGroup, idGroup)
        if(bEnable == False): return None, None, None             #必须可用

        #动态实例 (缓存，主控启动一次) 
        pWxdo = self.wxDos.get(pPrj.cmdStr, None)
        if(pWxdo == None):
            pWxdo = myImport.Import_Class(pPrj.fileName, pPrj.className)(self.usrName, "@@" + pPrj.prjName, pUser.usrRoot)
            self.wxDos[pWxdo.usrTag] = pWxdo
            
            if(pPrj.IsEnable_All() == False):    #非系统级功能，记录
                pPrj.goupsEnable[idGroup] = True 

            # 添加用户权限
            if(pUser.nickName != self.nickName):
                pUser._Add_Root(pWxdo)
        else:
            # 创建用户自己的Wxdo
            pWxdo = myImport.Import_Class(pPrj.fileName, pPrj.className)(self.usrName, "@@" + pPrj.prjName, pUser.usrRoot)
            pUser._Add_Root(pWxdo)
        return pWxdo, pPrj, pUser 
     

#主启动程序
if __name__ == "__main__":
    #sys.path.append("C:\Python35-32\Lib\site-packages\myPy_Libs")

    #动态实例测试
    pWxdo2 = myImport.Import_Class("myRobot_Repeater","myRobot_Repeater")('zxc');
    print( pWxdo2.Done("@@Repeater"))
    print( pWxdo2.Done("Hello"))
    print( pWxdo2.Done("Bye"))
    print( pWxdo2.Done("@@Repeater"))
    print("\n\n")

    #机器人消息处理
    pWxReply = myRobot_Reply()
    pWxReply._Init()
    
    #用户信息
    usrID = "zxc_0"
    usrName = "墨紫_0"
    nickName = "墨紫"
    usrPlant = "wx"


    #权限初始
    print(pWxReply.Done(usrID, usrName, nickName, usrPlant, '@@Repeater'))

    print(pWxReply.Done(usrID, usrName, nickName, usrPlant, '@@zxcRobot_Root'))
    print(pWxReply.Done('zxc_0',"墨紫_0",'Repeater'))

    #功能开关
    print(pWxReply.Done('zxc_0',"墨紫_0",'@@Repeater'))
    print(pWxReply.Done('zxc_0',"",'@@Repeater'))


    print(pWxReply.Done('zxc', "墨紫",'@@Repeater'))
    print(pWxReply.Done('zxc', "",'Hello'))
    print(pWxReply.Done('zxc', "",'@@Repeater'))

    time.sleep(2)
    print(pWxReply.Done('zxc', "",'@@Repeater'))

 
 
