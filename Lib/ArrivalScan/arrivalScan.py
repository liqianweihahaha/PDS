from config import uat_config
import requests,random,time,json
from Common.login import login
from Common.get_NowTime import get_now_time


# 到件扫描接口
class arrivalScan:
    def arrivalScan(self,token,waybillCode):
        url = uat_config + "/basic/manager/arrivalScan/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {"weight":"2","waybillCode":waybillCode}

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        if re["success"] == True:
            print("到件扫描成功")
        else:
            print("到件扫描失败",re)



if __name__ == "__main__":
    token = login("880220031","test123456")
    res = arrivalScan().arrivalScan(token,"BD040021504447")


