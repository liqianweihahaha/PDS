from config import uat_config
import requests, json
from Common.login import login
from Common.mysql import returnRegisterRecordID_query


# 退件登记相关接口
class returnRegister:
    # 退件登记
    def returnRegister(self, token, waybillCode):
        url = uat_config + "/basic/manager/ReturnRegister/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                "returnType":"RT01",
                "waybillCode": waybillCode,
                "reason":"autotest"
            }

        re = requests.post(url, json=data, headers=headers, verify=False)
        re = json.loads(re.text)  # 字符串转成字典
        # 判断是否退件登记成功
        if re['success'] == True:
            print('退件登记成功')
        else:
            print('退件登记失败，请检查', re)


    # 退件审核
    def returnRegisterApproval(self, token, waybillCode):
        url = uat_config + "/basic/manager/ReturnRegister/approval"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        # 查询退件登记表中 运单关联的id，用于取消接口传参
        id = returnRegisterRecordID_query(waybillCode)[0]

        data = {
                "status":"0",   # 退件状态，-1：待审核，0：已退件，1：取消退件，2：重新派送
                "approvalRemark":"",
                "idSet":[
                    id
                ],
                "waybillCodeSet":[
                    waybillCode
                ]
            }

        re = requests.post(url, json=data, headers=headers, verify=False)
        re = json.loads(re.text)  # 字符串转成字典
        # 判断是否退件登记成功
        if re['success'] == True:
            print('退件审核成功')
        else:
            print('退件审核失败，请检查', re)



    # 取消退件登记
    def returnRegisterCancle(self, token, waybillCode):
        url = uat_config + "/basic/manager/ReturnRegister/cancel"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        # 查询退件登记表中 运单关联的id，用于取消接口传参
        id = returnRegisterRecordID_query(waybillCode)[0]

        data = {"idSet":[ id ],
                "waybillCodeSet":[waybillCode]
                }

        re = requests.post(url, json=data, headers=headers, verify=False)
        re = json.loads(re.text)  # 字符串转成字典
        # 判断是否退件登记成功
        if re['success'] == True:
            print('取消退件登记成功')
        else:
            print('取消退件登记失败，请检查', re)



# token = login("bdadmin","12345678")
# returnRegister().returnRegisterApproval(token, 'BD121503934122')