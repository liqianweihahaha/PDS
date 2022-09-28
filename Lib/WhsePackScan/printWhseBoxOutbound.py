from config import uat_config
import requests,random,time,json


# 打印出库单接口
class printWhseBoxOutbound:
    def printWhseBoxOutbound(self,token,boxCode):
        url = uat_config + "/basic/manager/whseBox/printWhseBoxOutbound"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
            "boxCode":boxCode
        }

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        print(re)
        if re["success"] == True:
            print("打印出库单成功")
        else:
            print("打印出库单失败",re)



# printWhseBoxOutbound().printWhseBoxOutbound('880220030:c83fcb89-47c8-4aa4-9cdb-46da1804c156','BDB202209280009')
