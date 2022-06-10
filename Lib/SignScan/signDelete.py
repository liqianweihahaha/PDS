from config import uat_config
import requests,random,time,json
from Common.login import login
from Common.mysql import signRecord_query

# 删除签收接口
class signDelete:
    def signDelete(self,token,waybillCode):
        url = uat_config + "/basic/manager/sign/delete"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        # 查询需要删除的运单对应的id
        waybillId = signRecord_query(waybillCode)

        data = [
            {
                "id": waybillId,
                "waybillCode": waybillCode,
                "previousWaybillStatus":"4"  # 上一个状态：待派送--4
            }
        ]

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        if re["success"] == True:
            print("删除签收成功")
        else:
            print("删除签收失败",re)


if __name__ == "__main__":
    token = login("880220033","test123456")
    res = signDelete().signDelete(token,"BD030001006343")


