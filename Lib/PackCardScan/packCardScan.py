from config import uat_config
import requests,json,time
from Common.login import login
from Common.get_NowTime import get_now_time


# 装包相关接口
class packCardScan:
    # 打印包号
    def packCardPrint(self,token,startSite,endSite):
        url = uat_config + "/basic/manager/packageCard/generatorPackCardCodes"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                    "num":1,
                    "startSite":startSite,
                    "endSite":endSite
                }

        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典

        url = re["data"][0]["printUrl"]  # 获取包号面单的url
        packCard = re["data"][0]["packCard"]   # 获取包号，给到装包扫描接口用

        if re["success"] == True:
            print(f"打印包号成功，包号面单url为：{url}")
            return url,packCard
        else:
            print("打印包号失败",re)


    # 装包扫描-APP
    def packCardScan(self,token,packCard,billCode_list):
        url = uat_config + "/basic/manager/pda/batchInsert"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data ={
                    "packageCardWaybillScanDtoList": [
                        {
                            "endSite": "880010",
                            "endSiteName": "一级网点02",
                            "operationTime": int(time.mktime(time.strptime(get_now_time(),'%Y-%m-%d %H:%M:%S')) * 1000),
                            "packCard": packCard,
                            "startSite": "88011",
                            "startSiteName": "测试分拨中心01",
                            "waybillCode": billCode_list[0]
                        },
                        {
                            "endSite": "880010",
                            "endSiteName": "一级网点02",
                            "operationTime": int(time.mktime(time.strptime(get_now_time(),'%Y-%m-%d %H:%M:%S')) * 1000),
                            "packCard": packCard,
                            "startSite": "88011",
                            "startSiteName": "测试分拨中心01",
                            "waybillCode": billCode_list[1]
                        },
                        {
                            "endSite": "880010",
                            "endSiteName": "一级网点02",
                            "operationTime": int(time.mktime(time.strptime(get_now_time(),'%Y-%m-%d %H:%M:%S')) * 1000),
                            "packCard": packCard,
                            "startSite": "88011",
                            "startSiteName": "测试分拨中心01",
                            "waybillCode": billCode_list[2]
                        }
                    ]
                }


        re = requests.post(url, json=data, headers=headers)
        re = json.loads(re.text)  # 字符串转成字典

        if re["success"] == True:
            print(f"装包扫描成功")
        else:
            print("装包扫描失败", re)


if __name__ == "__main__":
    token = login("880220030","test123456")
    # res = packCardScan().packCardScan(token,"BDBAG2300000020",["BD030115023265001001","BD040093018762","BD030114523135001001"])


    res = packCardScan().packCardPrint(token,"88011","88010")
    print(res)