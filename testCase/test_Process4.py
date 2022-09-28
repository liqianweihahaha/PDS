# -*- coding: utf-8 -*-


import pytest
# 导入库函数


from Common.login import login
from Lib.Waybill.openAPI_createOrder_B import createOrder
from Common.mysql import waybill_query
# 导入网点和分拨中心的账号密码
from config import site01_username,site01_password,site01_code
from config import Ds01_username,Ds01_password,Ds01_code
from config import site02_username,site02_password,site02_code
import allure, os,json,time

"""
核心测试场景4--客户通过openAPI下单--同步到日不落系统：
        openAPI下单--日不落系统财务中心登录--查询运单
"""

@allure.story('核心测试场景4-客户管家订单同步到日不落')
@pytest.mark.TestProcess4
class TestProcess4:
    # 前置方法
    def setup_class(self):
        """登录初始化"""

        # 分拨中心01登录
        self.Ds01_token = login(Ds01_username, Ds01_password)

        self.billCode_list = []


    @allure.story('客户管家订单同步到日不落系统')
    @allure.title('客户管家订单同步到日不落系统')
    @allure.severity('critical')  # 测试用例的重要级别
    @allure.description('客户管家订单同步到日不落系统')
    @pytest.mark.orderSyn
    def test_orderSyn_B(self):
        i = 0
        while i < 1:
            waybillCode = createOrder()[0]  # openAPI下单
            self.billCode_list.append(waybillCode)
            i = i + 1

        # 循环断言在日不落系统waybill表能否查询到
        for billCode in self.billCode_list:
            assert waybill_query(billCode) == 1



if __name__ == '__main__':
    # 执行用例，生成tmp
    pytest.main(['test_Process4.py', '-s', '--alluredir', '../report/tmp'])
    # 复制环境变量文件
    # os.system('copy environment.properties report/tmp/environment.properties')
    # # # 生成报告
    # os.system('allure generate ../report/tmp -o ../report/report  --clean')
