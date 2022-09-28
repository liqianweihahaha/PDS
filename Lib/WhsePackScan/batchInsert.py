from config import uat_config
import requests,random,time,json


# 装箱-上传接口
class batchInsert:
    def batchInsert(self,token,boxCode,billCode):
        url = uat_config + "/basic/manager/whsePackScan/batchInsert"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
        "whsePackScanDtoList":[
            {
            "boxCode":boxCode,
            "waybillCode":billCode,
            "firstPackWaybill":"1",
            "customerName":"86test",
            "returnHk":"1",
            "returnHkName":"是",
        }
    ]
}


        re = requests.post(url,json=data,headers=headers)
        re = json.loads(re.text)  # 字符串转成字典
        if re["success"] == True:
            print("装箱上传成功")
        else:
            print("装箱上传失败",re)


# batchInsert().batchInsert('bdadmin:c117c08c-a4b7-4668-9dea-4a641f64efd4',"BDB202209080001",['BD121503909732','BD121503909841'])