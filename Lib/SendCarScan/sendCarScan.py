from config import uat_config
import requests,random,time,json
from Common.login import login
from Common.get_NowTime import get_now_time


# 发车扫描接口
class sendCarScan:
    def sendCarScan(self,token,billCode_list):
        url = uat_config + "/basic/manager/sendCarScan/batchInsert"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                    "sendCarScanDto":[
                                {
                                "packCard":billCode_list[0],
                                "carPlate":"粤B444445",
                                "driverName":"测试分拨司机",
                                "operationTimeFmt":get_now_time(),  # 当前时间
                                "operationTime":int(time.mktime(time.strptime(get_now_time(),'%Y-%m-%d %H:%M:%S')) * 1000),  # 当前时间戳
                                "driverCode":"880220031"
                                },
                                {
                                    "packCard": billCode_list[1],
                                    "carPlate": "粤B444445",
                                    "driverName": "测试分拨司机",
                                    "operationTimeFmt": get_now_time(),
                                    "operationTime": int(time.mktime(time.strptime(get_now_time(),'%Y-%m-%d %H:%M:%S')) * 1000),
                                    "driverCode": "880220031"
                                },
                                {
                                    "packCard": billCode_list[2],
                                    "carPlate": "粤B444445",
                                    "driverName": "测试分拨司机",
                                    "operationTimeFmt": get_now_time(),
                                    "operationTime": int(time.mktime(time.strptime(get_now_time(),'%Y-%m-%d %H:%M:%S')) * 1000),
                                    "driverCode": "880220031"
                                }
                                ]
                    }

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        # 获取车次清单号
        detailCode = re["data"]["detailedList"][0]["detailCode"]

        if re["success"] == True:
            return "发车扫描成功，车次清单为：",detailCode
        else:
            print("发车扫描失败",re)


if __name__ == "__main__":
    token = login("880220030","test123456")
    res = sendCarScan().sendCarScan(token,["BD020138535019","001","002"])
    print(res)

