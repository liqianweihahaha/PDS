import time
def get_now_time():
    """
    获取当前日期时间
    :return:当前日期时间
    """
    now =  time.localtime()
    now_time = time.strftime("%Y-%m-%d %H:%M:%S", now)  # 获取当前时间

    # 转为时间数组
    # timeArray = time.strptime(now_time,'%Y-%m-%d %H:%M:%S')
    # now_TimeStamp = int(time.mktime(timeArray) * 1000)  # 毫秒转换
    return now_time


if __name__ == '__main__':
    now_time = get_now_time()
    print(now_time)
