from config import uat_config
import requests,random,time,json
from Common.login import login
from Common.get_NowTime import get_now_time


# 发件扫描接口
class sendScan:
    def sendScan(self,token,billCode_list,nextSite):
        url = uat_config + "/basic/manager/sendScan/batchInsert"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                    "sendScanDtoList":[
                        {
                            "waybillCode":billCode_list[0],
                            "nextSite":nextSite,
                            # "nextSiteName":"测试分拨中心01",
                            "operationTimeFmt":get_now_time(),  # 当前时间
                            "operationTime":int(time.mktime(time.strptime(get_now_time(),'%Y-%m-%d %H:%M:%S')) * 1000) # 当前时间戳
                        },
                        {
                            "waybillCode":billCode_list[1],
                            "nextSite":nextSite,
                            # "nextSiteName":"测试分拨中心01",
                            "operationTimeFmt":get_now_time(),
                            "operationTime":int(time.mktime(time.strptime(get_now_time(),'%Y-%m-%d %H:%M:%S')) * 1000)
                        },
                        {
                            "waybillCode": billCode_list[2],
                            "nextSite": nextSite,
                            # "nextSiteName": "测试分拨中心01",
                            "operationTimeFmt": get_now_time(),
                            "operationTime": int(time.mktime(time.strptime(get_now_time(),'%Y-%m-%d %H:%M:%S')) * 1000)
                        }
                    ]
                }

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        if re["success"] == True:
            print("批量发件扫描成功")
        else:
            print("批量发件扫描失败",re)





if __name__ == "__main__":
    token = login("880220030","test123456")
    res = sendScan().sendScan(token,["BD020138535019","001","002"],88011)


