show databases;

# use nbiot;
#
# show tables ;
#
# desc app01_order;
#
# show create table app01_order;
#
# desc app01_admin ;
#
# # 插入初始账号root，密码root（90a0b867d1ae273da1be28d3c084749d为root字符串MD5加密后得值）
insert into app01_admin (username, password) values ('root', '90a0b867d1ae273da1be28d3c084749d');
#
# select * from nbiot_body;


