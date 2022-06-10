from config import uat_config
import requests, json
from Common.login import login


# 存件上架登记相关接口
class shelvesScan:
    # 存件上架登记
    def shelvesScan(self, token, waybillCode):
        url = uat_config + "/basic/manager/pda/shelvesScan/add"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'}

        data = {
                      "shelvesCode": "A01",
                      "waybillCode": waybillCode,
                 }

        re = requests.post(url, json=data, headers=headers, verify=False)
        re = json.loads(re.text)  # 字符串转成字典
        # 判断是否存件上架成功
        if re['success'] == True:
            print('存件上架成功')
        else:
            print('存件上架失败，请检查', re)



# token = login("880220030","test123456")
# shelvesScan().shelvesScan(token, 'BD020004140132')