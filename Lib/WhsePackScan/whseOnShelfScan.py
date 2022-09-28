from config import uat_config
import requests,random,time,json


# 箱子上架
class whseOnShelfScan:
    def whseOnShelfScan(self,token,boxCode):
        url = uat_config + "/basic/manager/whseOnShelfScan/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
            "newShelfCode":"A03",
            "boxCode":boxCode
        }

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        if re["success"] == True:
            print("上架接口请求成功")
        else:
            print("上架接口请求失败",re)