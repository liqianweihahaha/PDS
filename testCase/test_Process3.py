# -*- coding: utf-8 -*-


import pytest
# 导入库函数
from Lib.Waybill.createWaybill import Waybill
from Lib.PickedScan.pickScan import pickScan
from Lib.WaybillProblem.problemWaybill import ProblemWaybill
from Lib.KeepScan.keepScan import keepScan
from Lib.InterceptScan.interceptScan import interceptScan
from Lib.ShelvesScan.shelvesScan import shelvesScan
from Lib.ReturnRegister.returnRegister import returnRegister
from Common.login import login
from Common.mysql import waybillStatus_query,problemRecord_query,keepScanRecord_query,\
    interceptRecord_query,shelvesScanRecord_query,smsRecord_query,returnRegisterRecord_query

# 导入请求体和期望值的数据源
from Common.get_ExcelData import get_excelData, write_excelData
# 导入网点和分拨中心的账号密码
from config import site01_username,site01_password,site01_code
from config import Ds01_username,Ds01_password,Ds01_code
from config import site02_username,site02_password,site02_code
import allure, os,json,time

"""
核心测试场景3--回归各种登记操作：
            1、问题件登记+回复  2、留仓件登记  3、拦截件登记+取消拦截    4、存件上架并检查上架短信   5、退件登记
"""

@allure.story('核心测试场景3-回归各种登记操作')
@pytest.mark.TestProcess3
class TestProcess3:
    # 前置方法
    def setup_class(self):
        """登录初始化"""
        # 一级网点01登录
        self.site01_token = login(site01_username, site01_password)

        # 分拨中心01登录
        self.Ds01_token = login(Ds01_username, Ds01_password)

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


    @allure.story('分拨中心01-问题件登记,通知一级网点01')
    @allure.title('分拨中心01-问题件登记，通知一级网点01')
    @allure.severity('critical')
    @allure.description('分拨中心01-问题件登记，通知一级网点01')
    @pytest.mark.problemWaybilRegister
    def test_problemWaybill_register_Ds01(self):
        ProblemWaybill().createProblemWaybill(self.Ds01_token,self.billCode_list[0],site01_code)
        # 断言是否生成问题件登记记录-1  以及 对应的问题件类型-'IP09'，以及状态为未回复--0
        assert problemRecord_query(self.billCode_list[0])[0] == 1
        assert problemRecord_query(self.billCode_list[0])[1] == 'IP09'
        assert problemRecord_query(self.billCode_list[0])[2] == 0



    @allure.story('一级网点01-问题件回复')
    @allure.title('一级网点01-问题件回复')
    @allure.severity('critical')
    @allure.description('一级网点01-问题件回复')
    @pytest.mark.problemWaybilReply
    def test_problemWaybill_reply_site01(self):
        ProblemWaybill().problemWaybillReply(self.site01_token, self.billCode_list[0])
        # 断言对应的问题件的状态应该是已回复--1
        assert problemRecord_query(self.billCode_list[0])[2] == 1



    @allure.story('分拨中心01-留仓件登记')
    @allure.title('分拨中心01-留仓件登记')
    @allure.severity('critical')
    @allure.description('分拨中心01-留仓件登记')
    @pytest.mark.keepScanRegister
    def test_keepScan_register_Ds01(self):
        keepScan().keepScan(self.Ds01_token, self.billCode_list[0])
        # 断言对应的留仓登记表 是否有留仓登记记录
        assert keepScanRecord_query(self.billCode_list[0]) == 1



    @allure.story('分拨中心01-拦截件登记')
    @allure.title('分拨中心01-拦截件登记')
    @allure.severity('critical')
    @allure.description('分拨中心01-拦截件登记')
    @pytest.mark.interceptScanRegister
    def test_interceptScan_register_Ds01(self):
        interceptScan().interceptScan(self.Ds01_token,self.billCode_list[0])
        # 断言拦截状态 是否是已拦截--0
        assert interceptRecord_query(self.billCode_list[0])[1] == 0



    @allure.story('分拨中心01-取消拦截')
    @allure.title('分拨中心01-取消拦截')
    @allure.severity('critical')
    @allure.description('分拨中心01-取消拦截')
    @pytest.mark.interceptScanRegister
    def test_interceptCancle_Ds01(self):
        interceptScan().interceptCancle(self.Ds01_token, self.billCode_list[0])
        # 断言拦截状态 是否是取消拦截--1
        assert interceptRecord_query(self.billCode_list[0])[1] == 1



    @allure.story('分拨中心01-存件上架')
    @allure.title('分拨中心01-存件上架')
    @allure.severity('critical')
    @allure.description('分拨中心01-存件上架')
    @pytest.mark.shelvesScanRegister
    def test_shelvesScan_Ds01(self):
        shelvesScan().shelvesScan(self.Ds01_token,self.billCode_list[0])
        # 断言存件上架表是否有该条记录--1
        assert shelvesScanRecord_query(self.billCode_list[0]) == 1
        # 断言短信发送记录表是否有短信记录--1
        assert smsRecord_query(self.billCode_list[0], 2) == 1



    @allure.story('分拨中心01-退件登记')
    @allure.title('分拨中心01-退件登记')
    @allure.severity('critical')
    @allure.description('分拨中心01-退件登记')
    @pytest.mark.returnRegister
    def test_returnRegister_Ds01(self):
        returnRegister().returnRegister(self.Ds01_token, self.billCode_list[0])
        # 断言退件登记记录表是否有该条记录
        assert returnRegisterRecord_query(self.billCode_list[0])



if __name__ == '__main__':
    # 执行用例，生成tmp
    pytest.main(['test_Process3.py', '-s', '--alluredir', '../report/tmp'])
    # 复制环境变量文件
    # os.system('copy environment.properties report/tmp/environment.properties')
    # # # 生成报告
    # os.system('allure generate ../report/tmp -o ../report/report  --clean')














