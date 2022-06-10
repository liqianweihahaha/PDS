from config import uat_config
import requests, json
from Common.login import login


# 留仓件登记相关接口
class keepScan:
    # 留仓件登记
    def keepScan(self, token, waybillCode):
        url = uat_config + "/basic/manager/keepScan/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                "keepType":"HO02",
                "waybillCode": waybillCode,
                "remark":"autotest"
            }

        re = requests.post(url, json=data, headers=headers, verify=False)
        re = json.loads(re.text)  # 字符串转成字典
        # 判断是否留仓登记成功
        if re['success'] == True:
            print('留仓登记成功')
        else:
            print('留仓登记失败，请检查', re)



# token = login("880220030","test123456")
# keepScan().keepScan(token, 'BD020004139545')