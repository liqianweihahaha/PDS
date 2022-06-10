# -*- coding: utf-8 -*-


import pytest
# 导入库函数

from Common.login import login
from Lib.Waybill.createOrder_C import createOrder_C
# 导入请求体和期望值的数据源
from Common.get_ExcelData import get_excelData, write_excelData
# 导入网点和分拨中心的账号密码
from config import site01_username,site01_password,site01_code
from config import Ds01_username,Ds01_password,Ds01_code
from config import site02_username,site02_password,site02_code
import allure, os,json,time

"""
核心测试场景5--C端下单，日不落分单--网点操作：
        C端App下单--日不落系统财务中心登录--查询运单--分单给网点A--网点A取消分单--财务中心重新分单给网点B--网点B分配骑手--骑手做揽收操作
"""

@allure.story('核心测试场景5-C端订单同步到日不落')
@pytest.mark.TestProcess5
class TestProcess5:
    # 前置方法
    def setup_class(self):
        """登录初始化"""

        # 孟加拉财务中心登录
        self.bdCenter_token = login(Ds01_username, Ds01_password)

    def test_orderSyn_C(self):
        createOrder_C(self.bdCenter_token)





if __name__ == '__main__':
    # 执行用例，生成tmp
    pytest.main(['test_Process5.py', '-s', '--alluredir', '../report/tmp'])




