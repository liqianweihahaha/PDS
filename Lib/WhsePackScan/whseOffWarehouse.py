from config import uat_config
import requests,random,time,json


# 出库--整箱销毁
class whseOffWarehouse:
    def whseOffWarehouse(self,token,boxCode):
        url = uat_config + "/basic/manager/whseOffWarehouse/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
            "blBoxOff":"1",
            "offType":"1",
            "boxCode":boxCode
        }

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        if re["success"] == True:
            print("出库接口请求成功")
        else:
            print("出库接口请求失败",re)