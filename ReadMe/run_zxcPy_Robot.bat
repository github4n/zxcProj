@echo off 


::����΢�ź�̨
start python ./zxcPy.Weixin/zxcPy.Weixin/myWeixin_ItChat.py

::��ʱ5��
choice /t 5 /d y /n >nu
del nu


::����΢��API
start python ./zxcPy.Robot/myRobot_API.py


exit
 