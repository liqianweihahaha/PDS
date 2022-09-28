from config import uat_config
import requests,random,time,json


# 打印箱号接口
class printWhseBoxCode:
    def printWhseBoxCode(self,token):
        url = uat_config + "/basic/manager/whseBox/printWhseBoxCode"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        re = requests.post(url,headers=headers)
        re = json.loads(re.text)

        if re["success"] == True:
            boxCode = re["data"]["boxCode"]
            # print(f"打印箱号成功，箱号为 {boxCode}")
            return boxCode  # 返回箱号

        else:
            print("打印箱号失败",re)


# a = printWhseBoxCode().printWhseBoxCode("bdadmin:bbf2aba6-91b0-4a59-9471-c64a48f0b8c5")
# print(a)