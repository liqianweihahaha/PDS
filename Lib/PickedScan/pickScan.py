from config import uat_config
import requests,json
from Common.login import login


# 揽件扫描接口
class pickScan:
    def pickScan(self,token,waybillCode):
        url = uat_config + "/basic/manager/pickedScan/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {"weight":"1","waybillCode":waybillCode}

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        if re["success"] == True:
            print("揽件扫描成功")
        else:
            print("揽件扫描失败",re)


if __name__ == "__main__":
    token = login("880220030","test123456")
    res = pickScan().pickScan(token,"BD030017003558")
    print(res)

