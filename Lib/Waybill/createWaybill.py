from config import uat_config
import requests, json
from Common.login import login


# 运单相关接口
class Waybill:
    # 创建运单（录单,快递、零担、整车都是同一个接口）
    def createWaybill(self, inData, token):
        url = uat_config + "/basic/manager/waybill/create"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = inData

        re = requests.post(url, json=data, headers=headers, verify=False)
        re = json.loads(re.text)  # 字符串转成字典
        # 判断是否下单成功
        if re['success'] == True:
            waybillCode = re["data"]
            return waybillCode[0]
        else:
            print('录单接口请求失败，请检查', re)


    # 修改运单
    def modifyWaybill(self, waybillCode, token):
        url = uat_config + "/basic/manager/waybill/modify"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}
        data = {
                "customerCode":"",
                "seller":"",
                "sender":{
                    "name":"lqw",
                    "telephone":"02312321312",
                    "email":"123@qq.com",
                    "pca":[
                        "BDR00007",
                        "BDC00395",
                        "BDA01063"
                    ],
                    "provinceCode":"BDR00007",
                    "provinceName":"Barishal",
                    "cityCode":"BDC00395",
                    "cityName":"Barguna - Amtali",
                    "areaCode":"BDA01063",
                    "areaName":"Amtali",
                    "address":"autotest123"
                },
                "receiver":{
                    "name":"heihei",
                    "telephone":"02312321312",
                    "email":"666@qq.com",
                    "pca":[
                        "BDR00004",
                        "BDC00185",
                        "BDA00504"
                    ],
                    "provinceCode":"BDR00004",
                    "provinceName":"Chattogram",
                    "cityCode":"BDC00185",
                    "cityName":"Bandarban - Alikadam",
                    "areaCode":"BDA00504",
                    "areaName":"Alikadam",
                    "address":"autotest1666"
                },
                "goodsType":"IT01",
                "goodsName":"apple",
                "packageNumber":1,
                "forecastWeight":3,
                "productService":"SP01",
                "billingType":"PA01",
                "freightFee":3,
                "codFee":0,
                "insuranceAmount":0,
                "insuranceFee":"",
                "remark":"",
                "waybillCode": waybillCode,
                "waybillType":"2"
            }

        re = requests.post(url, json=data, headers=headers, verify=False)
        re = json.loads(re.text)  # 字符串转成字典
        # 判断是否修改成功
        if re['success'] == True:
           print('运单修改成功')
        else:
            print('运单修改失败，请检查', re)



if __name__ == "__main__":
    token = login("880220038", "a123456")
    indata = {
        "customerCode": "",
        "seller": "",
        "sender": {
            "name": "lqw",
            "telephone": "02312321312",
            "email": "123@qq.com",
            "pca": [
                "BDR00007",
                "BDC00395",
                "BDA01063"
            ],
            "provinceCode": "BDR00007",
            "provinceName": "Barishal",
            "cityCode": "BDC00395",
            "cityName": "Barguna - Amtali",
            "areaCode": "BDA01063",
            "areaName": "Amtali",
            "address": "autotest123"
        },
        "receiver": {
            "name": "yuanyuan",
            "telephone": "02312321312",
            "email": "666@qq.com",
            "pca": [
                "BDR00004",
                "BDC00185",
                "BDA00504"
            ],
            "provinceCode": "BDR00004",
            "provinceName": "Chattogram",
            "cityCode": "BDC00185",
            "cityName": "Bandarban - Alikadam",
            "areaCode": "BDA00504",
            "areaName": "Alikadam",
            "address": "autotest1666"
        },
        "goodsType": "IT01",
        "goodsName": "apple",
        "packageNumber": 1,
        "forecastWeight": "3",
        "productService": "SP01",
        "billingType": "PA01",
        "freightFee": "3",
        "codFee": "0",
        "insuranceAmount": "",
        "insuranceFee": "",
        "remark": "",
        "labelType": "1",
        "waybillCode": "",
        "waybillType": "2"
    }
    a = Waybill().createWaybill(indata, token)
    print(a)  # <class 'tuple'>
