from config import uat_config
import requests,random,time,json
from Common.login import login


# 异常签收扫描接口
class exceptionSignScan:
    def exceptionSignScan(self,token,waybillCode,exceptionType):
        url = uat_config + "/basic/manager/sign/exception/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                "exceptionType": exceptionType,   # 731代表的是电话不通或错误
                "signer":"tata",
                "waybillCode": waybillCode,
                "remark":"autotest",
                "photoUrl":"517f5f2b-59a7-4343-9226-ff5fb7253941.png",
                "dutySite":"880011",
                "dutySiteName":"一级网点",
            }

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        if re["success"] == True:
            print("异常签收扫描成功")
        else:
            print("异常签收扫描失败",re)


if __name__ == "__main__":
    token = login("880220033","test123456")
    res = exceptionSignScan().exceptionSignScan(token,"BD030001006343")


