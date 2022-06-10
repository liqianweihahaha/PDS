"""
思路：1-单个下单，并将运单号和客户单号return
"""

from config import B_uat_config
import requests
import json,time,random
from Common import DesUtils
import pprint


appCode = "888888"
secretKey = "hvmaYYOyegNy4muv"


# 下单接口
def createOrder():
    timeline = str(int((time.time() + 0.5) * 1000))
    data = {
        "acceptAddress": "4324UYUYI234",
        "ACCEPT_STREET_NAME":"34234234",
        "acceptCityCode": "C034",
        "acceptCityName": "534RWERWERW5345",
        "acceptCompanyName": "acceptCompanyName",
        "acceptCountryCode": "BD",
        "acceptCountryName": "Bangladesh",
        "acceptDistrictCode": "A0624",
        "acceptDistrictName": "432TRETERTRET4234",
        "acceptEmail": "123@Test.com",
        "acceptMobile": "+2340000",  #
        "acceptCitizenId":"11111111110",
        "acceptName": "wewqeqwerewrewrwrrewrwer",
        "acceptPhone": "2341111111111",
        "acceptPostCode": "acceptCode",
        "acceptProvinceCode": "R006",
        "acceptProvinceName": "  3456REWR 7899 5501  ",
        "codFee": 10,
        # "billCode": 666666664,
        "customOrderNo": random.randint(1111111,9999999),
        "customerCode": "860062",   # uat普通客户--推msd
        "parcelHigh": 1000,
        "parcelLength": 1000,
        "parcelVolume": 1.52,
        "parcelWeight": 0,
        "parcelWidth": 1000,
        "goodsQTY": 2,
        "insurePrice": 875,
        "itemList": [
            {
                "battery": 0,
                "blInsure": 0,
                "dutyMoney": 1000,
                "goodsId": "19999",
                "goodsMaterial": "",
                "goodsName": "itemmanee",
                "goodsNameDialect": "itemnam",
                "goodsQTY": 3,  # 商品数量
                "goodsRemark": "goodsRemark",
                "goodsRule": "goodsRule",
                "goodsType": "IT01",
                "goodsUnitPrice": 1,
                "goodsValue": 10,  # 商品申报价值
                "currencyType": "USD",
                "goodsWeight": 0,  # 商品重量
                "goodsHigh": 100,
                "goodsLength": 200,
                "goodsVolume": 1.52,
                "makeCountry": "makeCountry",
                "salePath": "salePath",
                "sku": "sku001",
                "unit": "",
                "goodsWidth": 200,
                "hsCode": "234324234"
            },
            {
                "battery": 0,
                "blInsure": 0,
                "dutyMoney": 1000,
                "goodsId": "19999",
                "goodsMaterial": "",
                "goodsName": "itemmanee",
                "goodsNameDialect": "itemnam",
                "goodsQTY": 3,  # 商品数量
                "goodsRemark": "goodsRemark",
                "goodsRule": "goodsRule",
                "goodsType": "IT01",
                "goodsUnitPrice": 1,
                "goodsValue": 10,  # 商品申报价值
                "currencyType": "USD",
                "goodsWeight": 0,  # 商品重量
                "goodsHigh": 100,
                "goodsLength": 200,
                "goodsVolume": 1.52,
                "makeCountry": "makeCountry",
                "salePath": "salePath",
                "sku": "sku001",
                "unit": "",
                "goodsWidth": 200,
                "hsCode": "234324234"
            }
        ],
        "piece": 1,
        "remark": "1",
        "sendAddress": "sendAddre",
        "sendCityCode": "sendCityCode",
        "sendCityName": "sendCityName",
        "sendCompanyName": "sendCompanyName",
        "sendCountryCode": "CN",
        "sendCountryName": "China",
        "sendDistrictCode": "sendDistrictCode",
        "sendDistrictName": "sendDistrictName",
        "sendMail": "sendMail",
        "sendMobile": "sendMobile",
        "sendName": "sendName",
        "sendPhone": "sendPhone",
        "sendPostCode": "sendPostCode",
        "sendProvinceCode": "sendProvinceCode",
        "sendProvinceName": "sendProvinceName",
        "shippingFee": 1,
        "deliveryType": "DE02",
        "payMethod": "PA01",  # PA01 现金
        "parcelType": "PT01",
        "shipType":"ST02",   # 区分本地件 ST01 和国际件 ST02  海外仓发 ST03标识
        "transportType":"TT02",
        "platformSource":"csp",
        "smallCode": random.randint(1111111,9999999),
        "threeSectionsCode": ""
}

    myData = DesUtils.triple_des_encrypt(data, timeline)


    headers = {'content-type': 'application/json'}
    url = B_uat_config + f"/open-api/express/order/createOrder?appCode={appCode}&timestamp={timeline}"
    res = requests.post(url, data=myData, headers=headers,verify=False)

    re = json.loads(res.text)

    if re['data'] != None:

        aa = DesUtils.triple_des_decrypt(re['data']).decode('utf-8')  # byte类型转字符串，先解码
        # print(aa) # 解密后的响应数据

        billCode = json.loads(aa)['billCode']  # 字符串类型转成字典类型,获取到运单号
        customerOrderNo = json.loads(aa)['customerOrderNo']   # 获取到客户单号
        print(f"openAPI下单成功，运单号为 {billCode},客户单号为 {customerOrderNo}")
        return billCode,customerOrderNo
    else:
        print(re)




# 1---openapi下单
# billCode = createOrder()[0]
# print(billCode)






