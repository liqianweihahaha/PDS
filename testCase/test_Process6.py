# -*- coding: utf-8 -*-

import pytest
# 导入库函数
from Lib.Waybill.createWaybill import Waybill
from Lib.PickedScan.pickScan import pickScan
from Lib.DispatchScan.dispatchScan import dispatchScan
from Lib.ReturnRegister.returnRegister import returnRegister

from Lib.SignScan.signScan import signScan
from Lib.SignScan.signReturnScan import signReturnScan
from Lib.SignScan.signDelete import signDelete

from Common.login import login
from Common.mysql import waybillStatus_query,problemRecord_query,keepScanRecord_query,\
    interceptRecord_query,shelvesScanRecord_query,smsRecord_query,\
    returnRegisterRecord_query,waybillTrack_query,returnRegisterRecordID_query
# 导入请求体和期望值的数据源
from Common.get_ExcelData import get_excelData, write_excelData
# 导入网点和分拨中心的账号密码
from config import site01_username,site01_password,site01_code
import allure, os,json,time


"""
核心测试场景5：覆盖退件取消+退件签收限制:
            网点下单--》揽件--》派件--》登记退件--》正常签收，签收失败--》
            退件签收，签收成功--》删除签收--》取消退件登记--》正常签收，签收成功
"""
@allure.story('核心测试场景6-退件取消和退件签收')
@pytest.mark.TestProcess6
class TestProcess6:
    # 前置方法
    def setup_class(self):
        """登录初始化"""
        # 一级网点01登录
        self.site01_token = login(site01_username, site01_password)

        self.billCode_list = []  # 运单号list


    @allure.story('一级网点-快递录单')
    @allure.title('一级网点-快递录单')
    @allure.severity('critical')  # 测试用例的重要级别
    @allure.description('一级网点-快递录单')
    @pytest.mark.createWaybill  # 标签---
    @pytest.mark.parametrize('inData,exp_value', get_excelData('录单数据', 2, 2, 5, 8))
    def test_create_waybill_site01(self, inData, exp_value):
        res = Waybill().createWaybill(json.loads(inData), self.site01_token)
        waybillCode_KD = res  # 输出运单号
        self.billCode_list.append(waybillCode_KD)
        assert waybillStatus_query(waybillCode_KD) == 10  # 断言运单状态为待揽收



    @allure.story('一级网点-揽件扫描')
    @allure.title('一级网点-揽件扫描')
    @allure.severity('critical')
    @allure.description('一级网点-揽件扫描')
    @pytest.mark.pickScan
    def test_pickScan_site01(self):
        # 循环进行揽件扫描
        for billCode in self.billCode_list:
            pickScan().pickScan(self.site01_token, billCode)
        # 循环断言运单状态为已揽件--1
        for billCode in self.billCode_list:
            assert waybillStatus_query(billCode) == 1
        # 循环断言揽件轨迹是否生成，且super_aciton_code == 1
        for billCode in self.billCode_list:
            assert waybillTrack_query(billCode) == 1



    # 一级网点01--派件扫描
    @allure.story('一级网点01-派件扫描')
    @allure.title('一级网点01-派件扫描')
    @allure.severity('critical')
    @allure.description('一级网点01-派件扫描')
    @pytest.mark.dispatchScan
    def test_dispatchScan_site01(self):
        # 循环进行派件扫描
        for billCode in self.billCode_list:
            dispatchScan().dispatchScan(self.site01_token, billCode)
        # 循环断言运单状态为派送中--4
        for billCode in self.billCode_list:
            assert waybillStatus_query(billCode) == 4
        # 循环断言是否生成派件短信记录（UAT的短信发送屏蔽了，所以不断言发送状态，只断言是否有生成发送记录）
        for billCode in self.billCode_list:
            assert smsRecord_query(billCode,1) == 1
        # 循环断言派件轨迹是否生成，且super_aciton_code == 4
        for billCode in self.billCode_list:
            assert waybillTrack_query(billCode) == 4



    @allure.story('一级网点01-退件登记')
    @allure.title('一级网点01-退件登记')
    @allure.severity('critical')
    @allure.description('一级网点01-退件登记')
    @pytest.mark.returnRegisterApproval
    def test_returnRegisterApproval_site01(self):
        returnRegister().returnRegisterApproval(self.site01_token, self.billCode_list[0])
        # 断言退件登记记录表 是否有该条记录
        # assert returnRegisterRecordID_query(self.billCode_list[0])[1] == -1



    # @allure.story('一级网点01-退件审核')
    # @allure.title('一级网点01-退件审核')
    # @allure.severity('critical')
    # @allure.description('一级网点01-退件审核')
    # @pytest.mark.returnRegister
    # def test_returnRegister_site01(self):
    #     returnRegister().returnRegister(self.site01_token, self.billCode_list[0])
    #     # 断言退件登记记录表 该运单的状态应该是 0-已退件
    #     # assert returnRegisterRecordID_query(self.billCode_list[0])[1]  == 0



    # 一级网点01--签收扫描
    @allure.story('一级网点01-签收扫描')
    @allure.title('一级网点01-签收扫描')
    @allure.severity('critical')
    @allure.description('一级网点01-签收扫描')
    @pytest.mark.signScan
    def test_signScan_site01(self):
        # 循环进行签收扫描，预期是签收失败，状态仍然是【派送中】
        for billCode in self.billCode_list:
            signScan().signScan(self.site01_token, billCode)
        # 循环断言运单状态为派送中---4
        for billCode in self.billCode_list:
            assert waybillStatus_query(billCode) == 4


    @allure.story('一级网点01-退件签收操作')
    @allure.title('一级网点01-退件签收操作')
    @allure.severity('critical')
    @allure.description('一级网点01-退件签收操作')
    @pytest.mark.signReturnScan
    def test_signReturnScan_site01(self):
        # 退件签收记录---这里只退件签收一个运单
        signReturnScan().signReturnScan(self.site01_token, self.billCode_list[0])

        # 断言这个运单的最新状态是否是退件签收-- 730
        assert waybillStatus_query(self.billCode_list[0]) == 730





if __name__ == '__main__':
    # 执行用例，生成tmp
    pytest.main(['test_Process6.py', '-s', '--alluredir', '../report/tmp'])
    # 复制环境变量文件
    # os.system('copy environment.properties report/tmp/environment.properties')
    # # # 生成报告
    # os.system('allure generate ../report/tmp -o ../report/report  --clean')