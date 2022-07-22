from config import uat_config
import requests,random,time,json
from Common.login import login


# 签收扫描接口
class signScan:
    def signScan(self,token,waybillCode):
        url = uat_config + "/basic/manager/sign/deliver/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                "waybillCode":waybillCode,
                "photoUrl":"517f5f2b-59a7-4343-9226-ff5fb7253941.png",
            }

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        if re["success"] == True:
            print("正常签收成功")
        else:
            print("正常签收失败",re)


if __name__ == "__main__":
    token = login("880220033","test123456")
    res = signScan().signScan(token,"BD040001001703")


