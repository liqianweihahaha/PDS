from config import uat_config
import requests,random,time,json
from Common.login import login


# 退件签收扫描接口
class signReturnScan:
    def signReturnScan(self,token,waybillCode):
        url = uat_config + "/basic/manager/sign/return/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                "signer":"autotest",
                "waybillCode": waybillCode
            }

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        if re["success"] == True:
            print("退件签收扫描成功")
        else:
            print("退件签收扫描失败",re)


if __name__ == "__main__":
    token = login("880220030","test123456")
    res = signReturnScan().signReturnScan(token,"BD020156564658")


