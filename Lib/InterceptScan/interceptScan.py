from config import uat_config
import requests, json
from Common.login import login
from Common.mysql import interceptRecord_query


# 拦截件登记相关接口
class interceptScan:
    # 拦截件登记
    def interceptScan(self, token, waybillCode):
        url = uat_config + "/basic/manager/intercept/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                "interceptType":"INT01",
                "waybillCode": waybillCode
            }

        re = requests.post(url, json=data, headers=headers, verify=False)
        re = json.loads(re.text)  # 字符串转成字典
        # 判断是否拦截登记成功
        if re['success'] == True:
            print('拦截登记成功')
        else:
            print('拦截登记失败，请检查', re)



    # 取消拦截
    def interceptCancle(self, token, waybillCode):
        url = uat_config + "/basic/manager/intercept/cancel"

        # 查询拦截记录表中 运单关联的id，用于取消接口传参
        id = interceptRecord_query(waybillCode)[2]

        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                    "waybillCodeSet":[
                        waybillCode
                    ],
                    "idSet":[
                        id
                    ]
             }

        re = requests.post(url, json=data, headers=headers, verify=False)
        re = json.loads(re.text)  # 字符串转成字典
        # 判断是否取消拦截登记成功
        if re['success'] == True:
            print('取消拦截成功')
        else:
            print('取消拦截失败，请检查', re)


# token = login("880220030","test123456")
# interceptScan().interceptCancle(token, 'BD020004139545')