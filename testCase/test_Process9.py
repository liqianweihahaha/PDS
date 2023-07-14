# -*- coding: utf-8 -*-


import pytest
# 导入库函数
from Lib.Waybill.createWaybill import Waybill
from Lib.Print.print import Print
from Lib.PickedScan.pickScan import pickScan
from Lib.SendScan.sendScan import sendScan
from Lib.PackCardScan.packCardScan import packCardScan
from Lib.ArrivalScan.arrivalScan import arrivalScan
from Lib.ArrivalCarScan.arrivalCarScan import arrivalCarScan
from Lib.SendCarScan.sendCarScan import sendCarScan
from Lib.DispatchScan.dispatchScan import dispatchScan
from Lib.SignScan.signScan import signScan
from Lib.SignScan.signDelete import signDelete
from Lib.SignScan.exceptionSignScan import exceptionSignScan
from Common.login import login
from Common.mysql import waybillStatus_query,printStatus_query,smsRecord_query,waybillTrack_query

# 导入请求体和期望值的数据源
from Common.get_ExcelData import get_excelData, write_excelData
# 导入网点和分拨中心的账号密码
from config import site01_username,site01_password,site01_code
from config import Ds01_username,Ds01_password,Ds01_code
from config import site02_username,site02_password,site02_code
import allure, os,json,time


"""
核心测试场景9-涉及装包发车的主流程；
            一级网点登录--下单--批量打印--》揽件扫描--》发件扫描，发往分拨中心01
             分拨中心01登录--》单票到件扫描--》打印包号，装包扫描--》打印任务单，发件扫描，发往末端网点--》发车扫描
             末端网点登录--》到车扫描--》单票到件扫描--》派件扫描--》签收扫描 ---》删除签收---》异常签收         
"""
@allure.story('核心测试场景1-全流程')
@pytest.mark.TestProcess1
class TestProcess1:
    # 前置方法
    def setup_class(self):
        """登录初始化"""
        # 一级网点01登录
        self.site01_token = login(site01_username, site01_password)

        # 分拨中心01登录
        self.Ds01_token = login(Ds01_username, Ds01_password)

        # 一级网点02登录
        self.site02_token = login(site02_username, site02_password)

        self.billCode_list = []  # 运单号list
        self.detailCode = []   # 任务单
        self.packCard = []  # 包号


    @allure.story('一级网点-快递录单')
    @allure.title('一级网点-快递录单')
    @allure.severity('critical')  # 测试用例的重要级别
    @allure.description('一级网点-快递录单')
    @pytest.mark.createWaybill  # 标签---
    @pytest.mark.parametrize('inData,exp_value', get_excelData('录单数据', 2, 2, 5, 8))
    def test_create_express_site01(self, inData, exp_value):
        res = Waybill().createWaybill(json.loads(inData), self.site01_token)
        waybillCode_KD = res  # 输出运单号
        self.billCode_list.append(waybillCode_KD)
        assert waybillStatus_query(waybillCode_KD) == 10   # 断言运单状态为待揽收



    @allure.story('一级网点-零担录单')
    @allure.title('一级网点-零担录单')
    @allure.severity('critical')
    @allure.description('一级网点-零担录单')
    @pytest.mark.createWaybill_LTL  # 标签---
    @pytest.mark.parametrize('inData,exp_value', get_excelData('录单数据', 3, 3, 5, 8))
    def test_create_waybill_LTL_site01(self, inData, exp_value):
        res = Waybill().createWaybill(json.loads(inData), self.site01_token)
        waybillCode_LD = res  # 输出运单号
        self.billCode_list.append(waybillCode_LD)
        assert waybillStatus_query(waybillCode_LD) == 10    # 断言运单状态为待揽收


    @allure.story('一级网点-整车录单')
    @allure.title('一级网点-整车录单')
    @allure.severity('critical')
    @allure.description('一级网点-整车录单')
    @pytest.mark.createWaybill_FTL  # 标签---
    @pytest.mark.parametrize('inData,exp_value', get_excelData('录单数据', 4, 4, 5, 8))
    def test_create_waybill_FTL_site01(self, inData, exp_value):
        res = Waybill().createWaybill(json.loads(inData), self.site01_token)
        waybillCode_ZC = res  # 输出运单号
        self.billCode_list.append(waybillCode_ZC)
        assert waybillStatus_query(waybillCode_ZC) == 10  # 断言运单状态为待揽收


    @allure.story('一级网点-批量打印')
    @allure.title('一级网点-批量打印')
    @allure.severity('critical')
    @allure.description('一级网点-批量打印')
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



    @allure.story('一级网点-揽件扫描')
    @allure.title('一级网点-揽件扫描')
    @allure.severity('critical')
    @allure.description('一级网点-揽件扫描')
    @pytest.mark.pickScan
    def test_pickScan_site01(self):
        # 循环进行揽件扫描
        for billCode in self.billCode_list:
            pickScan().pickScan(self.site01_token,billCode)
        # 循环断言运单状态为已揽件--1
        for billCode in self.billCode_list:
            assert waybillStatus_query(billCode) == 1
        # 循环断言揽件轨迹是否生成，且super_aciton_code == 1
        for billCode in self.billCode_list:
            assert waybillTrack_query(billCode) == 1



    @allure.story('一级网点-发件扫描')
    @allure.title('一级网点-发件扫描')
    @allure.severity('critical')
    @allure.description('一级网点-发件扫描')
    @pytest.mark.sendScan
    def test_sendScan_site01(self):
        # 循环进行发件扫描
        for billCode in self.billCode_list:
            sendScan().sendScan(self.site01_token, billCode, Ds01_code,"")
        # 循环断言运单状态为---2映射的状态是运输中
        for billCode in self.billCode_list:
            assert waybillStatus_query(billCode) == 2
        # 循环断言发件轨迹是否生成，且super_aciton_code == 2
        for billCode in self.billCode_list:
            assert waybillTrack_query(billCode) == 2




#-----------------------------------------------------------------------------------------------------------------------
    @allure.story('分拨中心01-到件扫描')
    @allure.title('分拨中心01-到件扫描')
    @allure.severity('critical')
    @allure.description('分拨中心01-到件扫描')
    @pytest.mark.arrivalScan
    def test_arrivalScan_Ds01(self):
        # 循环进行到件扫描
        for billCode in self.billCode_list:
            arrivalScan().arrivalScan(self.Ds01_token, billCode)
        # 循环断言运单状态为--3映射的状态也是运输中
        for billCode in self.billCode_list:
            assert waybillStatus_query(billCode) == 3
        # 循环断言到件轨迹是否生成，且super_aciton_code == 3
        for billCode in self.billCode_list:
            assert waybillTrack_query(billCode) == 3



    @allure.story('分拨中心01-打印包号')
    @allure.title('分拨中心01-打印包号')
    @allure.severity('critical')
    @allure.description('分拨中心01-打印包号')
    @pytest.mark.packCardPrint
    def test_packCardPrint_Ds01(self):
            res_list = packCardScan().packCardPrint(self.Ds01_token,"88011",'880010')
            self.packCard.append(res_list[1])


    @allure.story('分拨中心01-装包扫描')
    @allure.title('分拨中心01-装包扫描')
    @allure.severity('critical')
    @allure.description('分拨中心01-装包扫描')
    @pytest.mark.packCardScan
    def test_packCardScan_Ds01(self):
        # 装包扫描
        packCardScan().packCardScan(self.Ds01_token,self.packCard[0],self.billCode_list)




    @allure.story('分拨中心01-打印任务单')
    @allure.title('分拨中心01-打印任务单')
    @allure.severity('critical')
    @allure.description('分拨中心01-打印任务单')
    @pytest.mark.detailCodePrint
    def test_detailCodePrint_Ds01(self):
        res_list = sendCarScan().detailCodePrint(self.Ds01_token)
        self.detailCode.append(res_list[1])



    # 分拨中心01-发件扫描-下一站：一级网点02
    @allure.story('分拨中心01-发件扫描')
    @allure.title('分拨中心01-发件扫描')
    @allure.severity('critical')
    @allure.description('分拨中心01-发件扫描')
    @pytest.mark.sendScan
    def test_sendScan_Ds01(self):
        # 中心发件扫描,扫描包牌号发件
        sendScan().sendScan(self.Ds01_token, self.packCard[0],site02_code,self.detailCode[0])
        # 循环断言运单状态为--2映射的状态是运输中
        for billCode in self.billCode_list:
            assert waybillStatus_query(billCode) == 2
        # 循环断言发件轨迹是否生成，且super_aciton_code == 2
        for billCode in self.billCode_list:
            assert waybillTrack_query(billCode) == 2



    @allure.story('分拨中心01-发车扫描')
    @allure.title('分拨中心01-发车扫描')
    @allure.severity('critical')
    @allure.description('分拨中心01-发车扫描')
    @pytest.mark.sendCarScan
    def test_sendCarScan_Ds01(self):
        sendCarScan().sendCarScan(self.Ds01_token, self.detailCode[0])




# # # ------------------------------------------------------------------------------------------------------------------------
    @allure.story('一级网点02-到车扫描')
    @allure.title('一级网点02-到车扫描')
    @allure.severity('critical')
    @allure.description('一级网点02-到车扫描')
    @pytest.mark.arrivalCarScan
    def test_arrivalCarScan_site02(self):
        arrivalCarScan().arrivalCarScan(self.site02_token, self.detailCode[0], site02_code)



    @allure.story('一级网点02-到件扫描')
    @allure.title('一级网点02-到件扫描')
    @allure.severity('critical')
    @allure.description('一级网点02-到件扫描')
    @pytest.mark.arrivalScan
    def test_arrivalScan_site02(self):
        # 循环进行到件扫描
        for billCode in self.billCode_list:
            arrivalScan().arrivalScan(self.site02_token, billCode)
        # 循环断言运单状态为待派送--11
        for billCode in self.billCode_list:
            assert waybillStatus_query(billCode) == 11
        # 循环断言到件轨迹是否生成，且super_aciton_code == 3
        for billCode in self.billCode_list:
            assert waybillTrack_query(billCode) == 3


    # 一级网点02--派件扫描
    @allure.story('一级网点02-派件扫描')
    @allure.title('一级网点02-派件扫描')
    @allure.severity('critical')
    @allure.description('一级网点02-派件扫描')
    @pytest.mark.dispatchScan
    def test_dispatchScan_site02(self):
        # 循环进行派件扫描
        for billCode in self.billCode_list:
            dispatchScan().dispatchScan(self.site02_token, billCode)
        # 循环断言运单状态为派送中--4
        for billCode in self.billCode_list:
            assert waybillStatus_query(billCode) == 4
        # 循环断言是否生成派件短信记录（UAT的短信发送屏蔽了，所以不断言发送状态，只断言是否有生成发送记录）
        for billCode in self.billCode_list:
            assert smsRecord_query(billCode,1) == 1
        # 循环断言派件轨迹是否生成，且super_aciton_code == 4
        for billCode in self.billCode_list:
            assert waybillTrack_query(billCode) == 4

    # 一级网点02--签收扫描
    @allure.story('一级网点02-签收扫描')
    @allure.title('一级网点02-签收扫描')
    @allure.severity('critical')
    @allure.description('一级网点02-签收扫描')
    @pytest.mark.signScan
    def test_signScan_site02(self):
        # 循环进行签收扫描
        for billCode in self.billCode_list:
            signScan().signScan(self.site02_token, billCode)
        # 循环断言运单状态为已签收--5
        for billCode in self.billCode_list:
            assert waybillStatus_query(billCode) == 5
        # 循环断言签收轨迹是否生成，且super_aciton_code == 5
        for billCode in self.billCode_list:
            assert waybillTrack_query(billCode) == 5


     # 一级网点02--删除签收操作
    @allure.story('一级网点02-删除签收操作')
    @allure.title('一级网点02-删除签收操作')
    @allure.severity('critical')
    @allure.description('一级网点02-删除签收操作')
    @pytest.mark.signDelete
    def test_signDelete_site02(self):
        # 删除签收记录---这里就删了第一个运单
        signDelete().signDelete(self.site02_token,self.billCode_list[0])

        # 断言这个运单的最新状态是否回退到 待派送---4
        assert waybillStatus_query(self.billCode_list[0]) == 4




    @allure.story('一级网点02-异常签收操作')
    @allure.title('一级网点02-异常签收操作')
    @allure.severity('critical')
    @allure.description('一级网点02-异常签收操作')
    @pytest.mark.exceptionSignScan
    def test_exceptionSignScan_site02(self):
        # 异常签收记录---这里只异常签收第一个运单
        exceptionSignScan().exceptionSignScan(self.site02_token, self.billCode_list[0],"731")

        # 断言这个运单的最新状态是否是异常签收-- -2
        assert waybillStatus_query(self.billCode_list[0]) == -2






if __name__ == '__main__':
    # 执行用例，生成tmp
    pytest.main(['test_Process9.py', '-s', '--alluredir', '../report/tmp'])
    # 复制环境变量文件
    # os.system('copy environment.properties report/tmp/environment.properties')
    # # # 生成报告
    # os.system('allure generate ../report/tmp -o ../report/report  --clean')
