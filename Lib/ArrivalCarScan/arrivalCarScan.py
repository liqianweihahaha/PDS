from config import uat_config
import requests,random,time,json
from Common.login import login
from Common.get_NowTime import get_now_time


# 到车扫描接口
class arrivalCarScan:
    def arrivalCarScan(self,token,detailCode,operationSiteCode):
        url = uat_config + "/basic/manager/arrivalCarScan/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                    "detailCode":detailCode,
                    "operationTime":int(time.mktime(time.strptime(get_now_time(),'%Y-%m-%d %H:%M:%S')) * 1000),  # 当前时间戳
                    "operationSiteCode":operationSiteCode   # 当前网点code
                }

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        if re["success"] == True:
            print("到车扫描成功")
        else:
            print("到车扫描失败",re)


if __name__ == "__main__":
    token = login("880220033","test123456")
    res = arrivalCarScan().arrivalCarScan(token,"RWBD0000000013","880010")


