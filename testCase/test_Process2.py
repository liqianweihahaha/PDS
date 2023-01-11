# -*- coding: utf-8 -*-


import pytest
# 导入库函数
from Lib.Waybill.createWaybill import Waybill
from Lib.Print.print import Print
from Common.login import login
from Common.mysql import waybillStatus_query,printStatus_query,problemRecord_query,interceptRecord_query

# 导入请求体和期望值的数据源
from Common.get_ExcelData import get_excelData, write_excelData
# 导入网点和分拨中心的账号密码
from config import site01_username,site01_password,site01_code
import allure, os,json,time

"""
核心测试场景2-修改运单：一级网点登录--下单--打印--修改运单，自动拦截--重新打印后，自动取消拦截
"""

@allure.story('核心测试场景2-修改运单')
@pytest.mark.TestProcess2
class TestProcess2:
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



    @allure.story('一级网点-打印')
    @allure.title('一级网点-打印')
    @allure.severity('critical')
    @allure.description('一级网点-打印')
    @pytest.mark.print
    def test_print_site01(self):
        data = {
            "blBase64": "0",
            "printType": "2",  # 二联单=2   三联单=1  退件单=5
            "waybillCodeSet": self.billCode_list,
            'printSource': '1'
        }
        Print().print(data, self.site01_token)
        # 循环断言运单打印状态为已打印--1
        for billCode in self.billCode_list:
            assert printStatus_query(billCode) == 1


    @allure.story('一级网点-修改运单')
    @allure.title('一级网点-修改运单')
    @allure.severity('critical')
    @allure.description('一级网点-修改运单')
    @pytest.mark.modifyWaybill
    def test_modifyWaybill_site01(self):
        Waybill().modifyWaybill(self.billCode_list[0], self.site01_token)

        # 断言运单修改后 是否正常生成问题件和拦截件,问题件类型IP13代表修改面单信息---9.5版本已去掉
        # assert problemRecord_query(self.billCode_list[0])[1] == "IP13"
        assert interceptRecord_query(self.billCode_list[0])[0] == 1  # 自动生成了拦截件
        assert interceptRecord_query(self.billCode_list[0])[1] == 0  # 已拦截



    @allure.story('一级网点-重新打印')
    @allure.title('一级网点-重新打印')
    @allure.severity('critical')
    @allure.description('一级网点-重新打印')
    @pytest.mark.rePrint
    def test_rePrint_site01(self):
        data = {
            "blBase64": "0",
            "printType": "2",  # 二联单=2   三联单=1  退件单=5
            "waybillCodeSet": self.billCode_list,
            'printSource': '1'
        }
        Print().print(data, self.site01_token)
        # 循环断言运单打印状态为已打印--1
        for billCode in self.billCode_list:
            assert printStatus_query(billCode) == 1
        # 断言运单是否已经自动取消拦截
        assert interceptRecord_query(self.billCode_list[0])[1] == 1  # 取消拦截




if __name__ == '__main__':
    # 执行用例，生成tmp
    pytest.main(['test_Process2.py', '-s', '--alluredir', '../report/tmp'])
    # 复制环境变量文件
    # os.system('copy environment.properties report/tmp/environment.properties')
    # # # 生成报告
    # os.system('allure generate ../report/tmp -o ../report/report  --clean')






