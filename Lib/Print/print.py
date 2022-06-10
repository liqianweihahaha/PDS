from config import uat_config
import requests, json
from Common.login import login


# 面单打印相关接口
class Print:
    # 打印面单，两联单、三联单、退件单
    def print(self, inData, token):
        url = uat_config + "/basic/manager/waybill/print"
        headers = {'Content-Type': 'application/json',
                   'Authorization': token,
                   'lang': "zh_CN",
                   'Connection': 'close'
                   }

        data = inData

        re = requests.post(url, headers=headers, json=data)
        # 判断是否打印成功
        if re.json()['success'] == True:
            urls = re.json()["data"]["urls"]
            print('面单批量打印成功')
            return urls
        else:
            print('面单批量打印失败，请检查', re.json())


if __name__ == "__main__":
    token = login("880220030", "test123456")
    inData = {'blBase64': '0', 'printType': '2', 'waybillCodeSet': ['BD020108028905', 'BD030006501454', 'BD040006001322']}

    urls = Print().print(inData, token)
    print(urls)
