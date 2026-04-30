import socket
import re
import mysql.connector

# 创建TCP套接字并绑定到1008端口
tcp_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_sock.bind(('10.0.4.17', 1008))
tcp_sock.listen(5)
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
conn,addr=tcp_sock.accept()
# 处理接收到的信息并插入到mytable表中
while True:
    data=conn.recv(4096*10)
    message = data.decode("utf-8")
    print(message)
    if message.endswith("#"):
        # 使用正则表达式提取信息中的各个数值
        pattern = re.compile(r'temperature:([\d.]+)&humid:([\d.]+)&smoke_status:(\d+)&door_status:(\d+)&air_status:(\d+)')
        match = pattern.match(message)
        print(match)
        if match:
            temperature = float(match.group(1))
            humid = float(match.group(2))
            smoke_status = int(match.group(3))
            door_status = int(match.group(4))
            air_status = int(match.group(5))
            # 插入数据到mytable表中
            sql = "INSERT INTO app01_home (time, temperature, humid, smoke_status, door_status, air_status) VALUES (CURRENT_TIMESTAMP, %s, %s, %s, %s, %s)"
            val = (temperature, humid, smoke_status, door_status, air_status)
            cursor.execute(sql, val)
            db.commit()

# 关闭连接
cursor.close()
db.close()
tcp_sock.close()