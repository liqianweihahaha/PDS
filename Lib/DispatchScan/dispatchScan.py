from config import uat_config
import requests,random,time,json
from Common.login import login
from Common.get_NowTime import get_now_time


# 派件扫描接口
class dispatchScan:
    def dispatchScan(self,token,waybillCode):
        url = uat_config + "/basic/manager/dispatchScan/checkAndAdd"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                "dispatcherCode":"880220033",   # 派件员code
                "waybillCode":waybillCode
                }

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        if re["success"] == True:
            print("派件扫描成功")
        else:
            print("派件扫描失败",re)


if __name__ == "__main__":
    token = login("880220033","test123456")
    res = dispatchScan().dispatchScan(token,"BD040001001703")


