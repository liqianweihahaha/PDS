from Crypto.Cipher import AES
import base64
import requests

# str不是16的倍数那就补足为16的倍数
def add_to_16(value='1234567890123456'):
    while len(value) % 16 != 0:
        value += '\0'
    return str.encode(value)  # 返回bytes


# 加密方法
def myEncrypt(data):
    # 初始化加密器，先进行aes加密
    key = 'f351ddc7e3698ab8'.encode('utf-8')
    mode = AES.MODE_CBC
    iv = b'02f3b743271aef51'

    aes = AES.new(key,AES.MODE_CBC,iv)
    encrypt_aes = aes.encrypt(add_to_16(data))

    # 用base64编码
    encrypted_data = base64.encodebytes(encrypt_aes)
    # print(encrypted_data)
    return str(encrypted_data, encoding='utf-8')


# 解密方法
def myDecrypt(encrypted_data):
    # 优先逆向解密base64成bytes
    encrypt_aes = base64.decodebytes(encrypted_data.encode(encoding='utf-8'))

    # 初始化加密器，进行aes解密
    aes = AES.new(add_to_16(), AES.MODE_ECB)
    data = aes.decrypt(encrypt_aes)
    # print(data)
    print(str(data, encoding='utf-8'))


if __name__ == '__main__':
    url = "http://8.214.27.92:3000/basic/login"
    headers = {'content-type': 'application/json'}
    # 密码加密
    password = myEncrypt("test123456")

    print(password)
    # data = {"userName": "880220030", "password": password}
    #
    # re = requests.post(url, json=data, headers=headers)
    # print(re.text)


