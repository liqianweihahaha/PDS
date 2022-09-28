from config import uat_config
import requests,random,time,json


# 打印箱唛接口
class printWhseBoxMark:
    def printWhseBoxMark(self,token,boxCode):
        url = uat_config + "/basic/manager/whseBox/printWhseBoxMark"
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
            print("打印箱唛成功")
        else:
            print("打印箱唛失败",re)


# printWhseBoxMark().printWhseBoxMark('bdadmin:c117c08c-a4b7-4668-9dea-4a641f64efd4','BDB202209080001')