import requests
import json,random
from config import C_uat_config
from Common import DesUtils


# 批量创建C端订单
def createOrder_C(token):

    orderCode = random.randint(111111111,999999999)  # 运单号

    headers = {"Authorization":token,'content-type': 'application/json'}

    myData = {
    "orderType": "L",
    "insuranceAmount": 100,
    "freightFee":100,   # 运费
    "orderSource": "O-WEB",
    "receiver": {
        "address": "rewyruweqryuweqryuweqr",
        "provinceCode": "BDR00001",
        "cityCode": "BDC00001",
        "telephone": "01111111111",
        "areaCode": "A00001",
        "cityName": "Ras Al Khaimah",
        "areaName": "Dhaka Cantonment--TSO",
        "countryCode": "BD",
        "name": "lqw23232131232131321323",
        "orderCode": orderCode,
        "countryName": "",
        "provinceName": "Ras Al Khaimah",
        "email": "11@qq.com"
    },
    "deliveryType": "DE01",
    "goodsList": [
        {
            "unitPrice": 0,
            "unitWeight": "3",
            "quantity": 1,
            "unitVolume": "0.0000",
            "length": 0,
            "nameDialect": "",
            "declarePrice": 0,
            "createBy": "C86000030",
            "updateBy": "C86000030",
            "hasBattery": "0",
            "name": "3",
            "width": 0,
            "blInsured": "0",
            "currency": "AED",
            "sku": "",
            "category": "IT01",
            "height": 0
        }
    ],
    "customerCode": "C86000030",
    "remark": "",
    "threeSectionsCode": "",
    "packageNumber": 1,
    "goodsType": "IT01",
    "shipmentType": "ST01",
    "waybillType": "快递",
    "codFee": 0,
    "billingType": "PA01",
    "sender": {
        "address": "lqw23213213213213",
        "provinceCode": "BDR00001",
        "cityCode": "BDC00002",
        "telephone": "123456789",
        "areaCode": "BDA00002",
        "cityName": "Fujairah",
        "areaName": "Dhamrai",
        "countryCode": "BD",
        "name": "222",
        "orderCode": orderCode,
        "countryName": "",
        "provinceName": "Fujairah",
        "email": "11@qq.com"
    },
    "forecastTime": 1652407164340,
    "waybillCode": "",
    "orderCode": orderCode,
    "forecastWeight": 3,
    "currency": "AED",
    "transportType": "TT01",
    "goodsName": "3"
}

    myData1 = json.dumps(myData)

    url = C_uat_config + "/manager/consumerOrder/push"

    res = requests.post(url, data=myData1,headers=headers,verify=False)

    print(f"C端下单成功，订单号为 {orderCode}")

    return orderCode



# i = 0
# while i < 5:
#     re = createOrder_C(token)
#     # print(re)
#     i = i + 1
#
# print('Good bye!')
