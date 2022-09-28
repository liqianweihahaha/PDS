# -*- coding: utf-8 -*-


import pytest
# 导入库函数
from Common.login import login
from Lib.Waybill.openAPI_createOrder_B import createOrder
from Common.mysql import waybill_query
from Lib.WhsePackScan.printWhseBoxCode import printWhseBoxCode
from Lib.WhsePackScan.batchInsert import batchInsert
from Lib.WhsePackScan.printWhseBoxMark import printWhseBoxMark
from Lib.WhsePackScan.whseOnShelfScan import whseOnShelfScan
from Lib.WhsePackScan.whseOffWarehouse import whseOffWarehouse
from Lib.WhsePackScan.printWhseBoxOutbound import printWhseBoxOutbound
from Common.mysql import whseBoxCode_query,whsePackScan_query,onShelfScan_query,boxStatus_query


# 导入网点和分拨中心的账号密码
from config import site01_username,site01_password,site01_code
import allure, os,json,time


"""
核心测试场景7-正常流程：
          API下单--打印箱号--装箱上传--打印箱唛--上架--整箱出库（走销毁） --打印出库单         
"""
@allure.story('核心测试场景7-装箱上传并打印箱唛')
@pytest.mark.TestProcess7
class TestProcess7:
    # 前置方法
    def setup_class(self):
        """登录初始化"""

        # 一级网点01登录
        self.site01_token = login(site01_username, site01_password)

        self.billCode_list = []
        self.boxCode_list = []


    @allure.story('客户管家订单同步到日不落系统')
    @allure.title('客户管家订单同步到日不落系统')
    @allure.severity('critical')  # 测试用例的重要级别
    @allure.description('客户管家订单同步到日不落系统')
    @pytest.mark.orderSyn
    def test_orderSyn_B(self):
        i = 0
        while i < 5:
            waybillCode = createOrder()[0]  # openAPI下单
            self.billCode_list.append(waybillCode)
            i = i + 1

        # 循环断言在日不落系统waybill表能否查询到
        for billCode in self.billCode_list:
            assert waybill_query(billCode) == 1


    @allure.story('打印箱号')
    @allure.title('打印箱号')
    @allure.severity('critical')
    @allure.description('打印箱号')
    @pytest.mark.printWhseBox
    def test_printWhseBox_site01(self):
        # 打印箱号
        boxCode = printWhseBoxCode().printWhseBoxCode(self.site01_token)
        self.boxCode_list.append(boxCode)

        # 断言是否打印成功--检查箱号表是否有这条记录
        assert whseBoxCode_query(self.boxCode_list[0]) == 1


    @allure.story('装箱上传')
    @allure.title('装箱上传')
    @allure.severity('critical')
    @allure.description('装箱上传')
    @pytest.mark.batchInsert
    def test_batchInsert_site01(self):
        # 装箱上传,循环装箱
        for billCode in self.billCode_list:
            batchInsert().batchInsert(self.site01_token, self.boxCode_list[0],billCode)

        # 循环断言在日不落系统tt_whse_pack_scan表能否查询到 5条记录；
        assert whsePackScan_query(self.boxCode_list[0]) == 5


    @allure.story('打印箱唛')
    @allure.title('打印箱唛')
    @allure.severity('critical')
    @allure.description('打印箱唛')
    @pytest.mark.printWhseBoxMark
    def test_printWhseBoxMark_site01(self):
        # 打印箱唛
        printWhseBoxMark().printWhseBoxMark(self.site01_token, self.boxCode_list[0])


    @allure.story('箱子上架')
    @allure.title('箱子上架')
    @allure.severity('critical')
    @allure.description('箱子上架')
    @pytest.mark.whseOnShelfScan
    def test_whseOnShelfScan_site01(self):
        whseOnShelfScan().whseOnShelfScan(self.site01_token, self.boxCode_list[0])

        # 断言在日不落系统tt_whse_on_shelf_scan表能否查到记录
        assert onShelfScan_query(self.boxCode_list[0]) == 5


    @allure.story('出库整箱销毁')
    @allure.title('出库整箱销毁')
    @allure.severity('critical')
    @allure.description('出库整箱销毁')
    @pytest.mark.whseOffWarehouse
    def test_whseOffWarehouse_site01(self):
        whseOffWarehouse().whseOffWarehouse(self.site01_token, self.boxCode_list[0])

        # 断言在日不落系统tt_whse_box表中的箱子状态 是否为已完结--1
        assert boxStatus_query(self.boxCode_list[0]) == 1


    @allure.story('打印出库单')
    @allure.title('打印出库单')
    @allure.severity('critical')
    @allure.description('打印出库单')
    @pytest.mark.printWhseBoxOutBound
    def test_printWhseBoxOutBound_site01(self):
        printWhseBoxOutbound().printWhseBoxOutbound(self.site01_token, self.boxCode_list[0])




if __name__ == '__main__':
    # 执行用例，生成tmp
    pytest.main(['test_Process7.py', '-s', '--alluredir', '../report/tmp'])
    # 复制环境变量文件
    # os.system('copy environment.properties report/tmp/environment.properties')
    # # # 生成报告
    # os.system('allure generate ../report/tmp -o ../report/report  --clean')



