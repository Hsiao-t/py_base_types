本程序是一个小巧的通过snmp监控设备流量的Python应用程序,涉及文件：
1. snmp_utils.py 主要实现snmp-walk,snmp-get操作
2. interface-monitor.py 流量监控程序
3. nm_array.py 一个处理数组四则运算的模块
4. nm_dict.py 一个处理散列表四则运算的模块
5. /opt/.security_data/snmp_con.conf 记录连接设备的snmp口令

依赖
1. net-snmp-utils
2. mongodb
