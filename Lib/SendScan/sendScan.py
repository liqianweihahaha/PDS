from config import uat_config
import requests,random,time,json
from Common.login import login
from Common.get_NowTime import get_now_time


# 发件扫描接口
class sendScan:
    def sendScan(self,token,waybillCode,nextSite):
        url = uat_config + "/basic/manager/sendScan/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
            "waybillCode":waybillCode,
            "nextSite":nextSite,
                }

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典

        if re["success"] == True:
            print("发件扫描成功")
        else:
            print("发件扫描失败",re)





if __name__ == "__main__":
    token = login("880220030","test123456")
    res = sendScan().sendScan(token,"BD040093518829",88011)


