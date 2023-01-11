from config import uat_config
from Common.encrypt import myEncrypt
import requests
import json


# 登录接口,获取token
def login(username, password):
    url = uat_config + "/basic/token/login"
    headers = {'content-type': 'application/json'}
    # 密码加密
    password = myEncrypt(password)

    data = {"userName": username, "password": password}
    re = requests.post(url, json=data, headers=headers, verify=False)

    # 判断接口是否请求成功
    if json.loads(re.text)["success"] == True:
        token = json.loads(re.text)["data"]["access_token"]  # 响应体先转字典，然后取token
        return token
    else:
        print("登录失败",re.text)


# data = login("880220031", "test123456")
# print(data)
