from config import uat_config
import requests, json
from Common.login import login
from Common.mysql import problemRecordId_query


# 问题件相关接口
class ProblemWaybill:
    # 问题件登记
    def createProblemWaybill(self, token, waybillCode, notifySiteCode):
        url = uat_config + "/basic/manager/waybillProblem/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
            "waybillCode":waybillCode,
            "problemPictureUrl":"6242bb16-e4c5-4a5e-a6b7-bea7e9b0316e.png",
            "notifySiteCode": notifySiteCode,   # 该运单的揽件网点
            "problemType":"IP09",
            "reason":"autotest"
        }

        re = requests.post(url, json=data, headers=headers, verify=False)
        re = json.loads(re.text)  # 字符串转成字典
        # 判断是否登记成功
        if re['success'] == True:
            print('问题件登记成功')
        else:
            print('问题件登记失败，请检查', re)


    # 问题件回复
    def problemWaybillReply(self, token, waybillCode):
        url = uat_config + "/basic/manager/waybillProblem/reply"

        # 查询数据库该运单在问题件表对应的id
        id = problemRecordId_query(waybillCode)

        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                    "replyContent":"autotest",
                    "waybillCodeSet":[
                        waybillCode
                    ],
                    "idSet":[
                        id
                    ]
            }

        re = requests.post(url, json=data, headers=headers, verify=False)
        re = json.loads(re.text)  # 字符串转成字典
        # 判断是否回复成功
        if re['success'] == True:
            print('问题件回复成功')
        else:
            print('问题件回复失败，请检查', re)


if __name__ == "__main__":
    token = login("880220030", "test123456")
    # a = ProblemWaybill().createProblemWaybill('BD020004138404','880009', token)
    ProblemWaybill().problemWaybillReply(token, 'BD020004139064')

