@echo off 

::����΢�ź�̨
start python zxcPy.Weixin/myWeixin_ItChat.py
::��ʱ5��
choice /t 5 /d y /n >nu

::����΢��API
start python myWeixin_API.py


exit
 