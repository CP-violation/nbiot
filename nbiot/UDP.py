import socket
import re
import mysql.connector

# 创建UDP套接字并绑定到1006端口
udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
udp_sock.bind(('', 1006))

# 连接MySQL数据库
db = mysql.connector.connect(
    host="localhost",
    user="nbiot",
    password="123456",
    database="nbiot",
    auth_plugin="mysql_native_password"
)

# 创建MySQL游标对象
cursor = db.cursor()
print("initok")
# 处理接收到的信息并插入到nbiot表中
while True:
    print("true")
    udp_sock.settimeout(60)  # 设置超时时间为 5 秒
    try:
        data, addr = udp_sock.recvfrom(4096)
    except socket.timeout:
        print("没有接收到数据")
    else:
        print("接收到数据：", data)
    message = data.decode("utf-8")
    print(message)
    if message.endswith("#"):
        # 使用正则表达式提取信息中的各个数值
        pattern = re.compile(r'GPS_log:([\d.]+)&GPS_lat:([\d.]+)&heart:(\d+)&blood:(\d+)&body_status:(\d+)')
        match = pattern.match(message)
        if match:
            GPS_log = float(match.group(1))
            GPS_lat = float(match.group(2))
            heart = int(match.group(3))
            blood = int(match.group(4))
            body_status = int(match.group(5))
            GPS_log=GPS_log+0.075
            GPS_lat=GPS_lat+0.148
            # 插入数据到mytable表中
            sql = "INSERT INTO mytable (time, heart, blood, body_status, GPS_log, GPS_lat) VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s, %s)"
            val = (heart, blood, body_status, GPS_log, GPS_lat)
            cursor.execute(sql, val)
            db.commit()
            print("insertok")
# 关闭连接
cursor.close()
db.close()
udp_sock.close()
