# -*- coding: utf-8 -*-


import pytest
# 导入库函数
from Common.login import login
from Lib.Waybill.openAPI_createOrder_B import createOrder
from Common.mysql import waybill_query


# 导入网点和分拨中心的账号密码
from config import site01_username,site01_password,site01_code
import allure, os,json,time


"""
核心测试场景8-正常流程：加纳--》孟加拉
          国际快递录单--加纳网点揽收-网点发件--分拨到件-分拨发件 --》下单网点修改运单税费 --》 
          孟加拉中心重新打印面单--》孟加拉中心到件--》中心发件--》网点到件--》网点派件--》网点签收     
"""




