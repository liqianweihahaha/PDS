import pymysql

# UAT数据库
hostname = "47.241.40.42"
username = "logistic"
password = "ARxk8mkoyRf8"
dbname = "speedaf_cheetah_warehouse_bd"    # 要连接的库名


# Test数据库
# hostname = "39.108.178.162"
# username = "root"
# password = "root"
# dbname = "speedaf_cheetah_warehouse_bd"    # 要连接的库名



# 查询运单状态
def waybillStatus_query(waybill):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    # 执行sql，查询运单状态
    sql = f"select waybill_status,id from tt_waybill where code in ('{waybill}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    waybill_status = int(data[0][0])


    # 关闭，释放资源
    cursor.close()
    conn.close()

    return waybill_status


# 查询运单记录
def waybill_query(waybill):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    # 执行sql，查询运单是否存在
    sql = f"select * from tt_waybill where code in ('{waybill}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    data_length = len(data)

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return data_length



# 查询打印状态
def printStatus_query(waybill):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql，查询运单的打印状态  0-未打印 1-已打印
    sql = f"select print_status from tt_waybill where code in ('{waybill}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    waybill_status = int(data[0][0])

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return waybill_status


# 查询短信发送记录
def smsRecord_query(waybill,type):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql，查询是否生成派件短信发送记录  type=1 代表派件短信  type=2 代表存件短信
    sql = f"SELECT * FROM tt_sms_send_record where type ='{type}' and waybill_code  in ('{waybill}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    # 获取返回的data元组的长度，正常情况下只会查询到一条短信记录
    data_length = len(data)

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return data_length


# 查询运单轨迹是否生成



# 查询运单的问题件记录
def problemRecord_query(waybill):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql，查询是否生成问题件记录，problem_type代表问题件类型，IP13代表修改面单信息
    sql = f"SELECT problem_type,bl_reply FROM tt_waybill_problem  where  waybill_code  in ('{waybill}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    data_length = len(data)
    problem_type = data[0][0]
    bl_reply = int(data[0][1])

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return data_length,problem_type,bl_reply



# 查询运单的拦截件记录 以及拦截状态
def interceptRecord_query(waybill):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql，查询是否生成拦截件记录，bl_auto_generate代表是否修改运单自动生成，0--否，1--是；status代表拦截状态，0--已拦截，1--取消拦截
    sql = f"SELECT bl_auto_generate,status,id FROM tt_intercept_scan where  waybill_code  in ('{waybill}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    bl_auto_generate = int(data[0][0])
    status = int(data[0][1])
    id = data[0][2]

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return bl_auto_generate,status,id


# 查询tt_waybill_problem问题件表中对应运单的id，用于回复问题件接口的传参
def problemRecordId_query(waybill):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql，查询问题件登记表对应的id
    sql = f"SELECT id FROM tt_waybill_problem where  waybill_code  in ('{waybill}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    problemId = data[0][0]


    # 关闭，释放资源
    cursor.close()
    conn.close()

    return problemId


# 查询留仓登记记录表
def keepScanRecord_query(waybill):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql
    sql = f"SELECT * FROM tt_keep_scan where  waybill_code  in ('{waybill}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    data_length = len(data)

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return data_length


# 存件记录查询
def shelvesScanRecord_query(waybill):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql
    sql = f"SELECT * FROM tt_shelves_scan where  waybill_code  in ('{waybill}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    data_length = len(data)

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return data_length


# 退件登记记录查询
def returnRegisterRecord_query(waybill):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql
    sql = f"SELECT * FROM tt_return_register where  waybill_code  in ('{waybill}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    data_length = len(data)

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return data_length


# 查询最新轨迹状态
def waybillTrack_query(waybill):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql,查询轨迹表最新一条轨迹的super_action_code
    sql = f"SELECT super_action_code FROM tt_waybill_track where  waybill_code  in ('{waybill}') order by create_time desc limit 0,1;"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    super_action_code = int(data[0][0])

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return super_action_code


# 查询签收记录表对应的记录id，用于删除签收
def signRecord_query(waybill):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql,
    sql = f"SELECT id FROM tt_sign where  waybill_code  in ('{waybill}') order by create_time desc limit 0,1;"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    id = int(data[0][0])

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return id


# 查询退件登记表对应的记录id，用于取消退件
def returnRegisterRecordID_query(waybill):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql，查询是否生成退件记录ID     退件状态status 0为已取消，1为未取消
    sql = f"SELECT id,status FROM tt_return_register where  waybill_code  in ('{waybill}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    id = data[0][0]
    status = int(data[0][1])

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return id,status



# 查询箱号表是否有该箱号数据
def whseBoxCode_query(box_code):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql，查询是否生成箱号记录
    sql = f"SELECT * FROM tt_whse_box where  box_code  in ('{box_code}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    data_length = len(data)

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return data_length


# 查询装箱表是否有该条数据
def whsePackScan_query(box_code):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql，查询是否生成箱号记录
    sql = f"SELECT * FROM tt_whse_pack_scan where  box_code  in ('{box_code}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    data_length = len(data)

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return data_length


# 查询上架表是否有该条数据
def onShelfScan_query(box_code):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql，查询是否生成箱号记录
    sql = f"SELECT * FROM tt_whse_on_shelf_scan where  box_code  in ('{box_code}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    data_length = len(data)

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return data_length


# 查询箱子表 该箱的完结状态
def boxStatus_query(box_code):
    # 创建数据库连接
    conn = pymysql.connect(host=hostname, user=username, password=password, db=dbname)
    # 建立游标
    cursor = conn.cursor()

    conn.ping(reconnect=True)
    # 执行sql，查询是否生成箱号记录
    sql = f"SELECT status FROM tt_whse_box where  box_code  in ('{box_code}');"
    cursor.execute(sql)

    # 获取数据
    data = cursor.fetchall()
    status = int(data[0][0])

    # 关闭，释放资源
    cursor.close()
    conn.close()

    return status





a = boxStatus_query('BDB202209280008')
print(a)
