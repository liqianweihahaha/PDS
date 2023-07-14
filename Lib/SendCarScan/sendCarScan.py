from config import uat_config
import requests,random,time,json
from Common.login import login
from Common.get_NowTime import get_now_time


# 发车扫描相关接口
class sendCarScan:
    # 发车扫描
    def sendCarScan(self,token,detailCode):
        url = uat_config + "/basic/manager/sendCarScan/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                "detailCode":detailCode,
                "carPlate":"testA2222222粤",
                "driverName":"测试分拨司机",
                "operationTimeFmt":get_now_time(),  # 当前时间
                "operationTime":int(time.mktime(time.strptime(get_now_time(),'%Y-%m-%d %H:%M:%S')) * 1000),  # 当前时间戳
                "driverCode":"880220031"
                }

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典


        if re["success"] == True:
            print("发车扫描成功")
        else:
            print("发车扫描失败",re)


    # 打印任务单
    def detailCodePrint(self, token):
        url = uat_config + "/basic/manager/sendCarScan/generatorDetailCode"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        re = requests.post(url, headers=headers)
        re = json.loads(re.text)  # 字符串转成字典

        url = re["data"]["printUrl"]  # 获取任务单面单的url
        detailCode = re["data"]["detailCode"]  # 获取任务单，给到发件扫描、发车扫描接口用

        if re["success"] == True:
            print(f"打印任务单成功，任务单面单url为：{url}")
            return url, detailCode
        else:
            print("打印任务单失败", re)







if __name__ == "__main__":
    token = login("880220031","test123456")
    res = sendCarScan().sendCarScan(token,"RWBD0000000013")

    # res = sendCarScan().detailCodePrint(token)
    # print(res)

