from subprocess import Popen as popen,PIPE
from nm_array import nm_array
snmp_parse_t = {
  "ifHCInOctets": "IF-MIB::ifHCInOctets\.(\d+) = Counter64: (\d+)", # 端口接收的字节数(64位计数器)
  "ifHCOutOctets": "IF-MIB::ifHCOutOctets.(\d+) = Counter64: (\d+)", # 端口发送的字节数(64位计数器)
  "ifDescr": "IF-MIB::ifDescr.(\d+) = STRING: (.*)", # 端口表
  "ifHCInUcastPkts": "IF-MIB::ifHCInUcastPkts.(\d+) = Counter64: (\d+)", # 端口输入单播包数(64位计数器)
  "ifHCInMulticastPkts": "IF-MIB::ifHCInMulticastPkts.(\d+) = Counter64: (\d+)", # 端口输入多播包数
  "ifHCInBroadcastPkts": "IF-MIB::ifHCInBroadcastPkts.(\d+) = Counter64: (\d+)", # 端口输入广播包数
  "ifHCOutUcastPkts": "IF-MIB::ifHCOutUcastPkts.(\d+) = Counter64: (\d+)", # 端口输入单播包数(64位计数器)
  "ifHCOutMulticastPkts": "IF-MIB::ifHCOutMulticastPkts.(\d+) = Counter64: (\d+)", # 端口输入多播包数
  "ifHCOutBroadcastPkts": "IF-MIB::ifHCOutBroadcastPkts.(\d+) = Counter64: (\d+)", # 端口输入广播包数
}

def union_dict(dict_a,dict_b,union_method='inner'):
  """
  按照key_name联接两个HASH表(dict)，返回结果为{key_name: (value_a,value_b,value_c,....)}
  """
  ret_dict = dict()
  keys= []
  if union_method == 'inner':
    keys = set(dict_a.keys()) & set(dict_b.keys())
  elif union_method == 'outer':
    keys = set(dict_a.keys()) | set(dict_b.keys())
  else:
    keys = set(dict_a.keys()) & set(dict_b.keys())
  for key in keys:
    value = []
    value_a = dict_a.get(key) or 0
    value_b = dict_b.get(key) or 0
    if type(value_a) is list or type(value_a) is tuple:
      for v in value_a: value.append(v)
    elif type(value_a) is int or type(value_a) is float or type(value_a) is str: 
      value.append(value_a)
    else:
      raise ValueError("Cannot perform union operation between:{} and {}".format(type(value_a),type(value_b)))
    if type(value_b) is list or type(value_b) is tuple:
      for v in value_b: value.append(v)
    elif type(value_b) is int or type(value_b) is float or type(value_b) is str: 
      value.append(value_b)
    else:
      raise ValueError("Cannot perform union operation between:{} and {}".format(type(value_a),type(value_b)))
    ret_dict[key] = value
  return ret_dict

def snmp_u(host,snmp_comm, oid, pa, method="walk",interval=30):
  """
  输入参数(In):
  --> host: 主机名
  --> snmp_comm: 管理字符串
  --> oid: 获取的节点id
  --> pa: 提取pattern
  --> method: [walk]运行snmpwalk,[get]运行snmpget命令
  --> interval: 时间间隔
  输出参数(Out):
  --> {key:value}, 解析出的数据
  """
  import re
  cmd = "snmp{method} -v2c -c {snmp} {device} {oid}"
  p = popen(cmd.format(method=method,snmp=snmp_comm,device=host,oid=oid),shell=1,close_fds=1,stdout=PIPE,stderr=PIPE)
  ret = p.stdout.readlines()
  p.wait()
  ret = [ _.decode().replace('\n','') for _ in ret ]
  ret_dict = {}
  for el in ret:
    try:
      key,value = re.findall(pa,el)[0]
      ret_dict[key] = value
    except:
      continue
  return ret_dict

def snmp_bw(host, snmp_co, oids):
  """
  批量Walk数据
  """
  ret_dict = snmp_u(host,snmp_co,oids[0],snmp_parse_t[oids[0]])
  oids = oids[1:]
  for oid in oids:
    cur = snmp_u(host,snmp_co,oid,snmp_parse_t[oid])
    ret_dict = union_dict(ret_dict,cur) 
  return ret_dict

def rate(host,snmp_comm,oid,interval=5,cont=True,handle=print):
  """
  doc:
    获取端口数据传输速率信息，如总字节数，单播包数，广播包数，错误包数等
  param:
    --> host: 主机
    --> snmp_comm: snmp连接密钥
    --> oid: 需要获取的数据集
    --> interval: 监听时长
  """
  from time import time,sleep
  prev_timer = time()
  max_value = pow(2,64)-1
  ret_dict = dict()
  prev_value = snmp_u(host,snmp_comm,oid,snmp_parse_t[oid])
  if cont == True and handle is not None:
    while(True):
      sleep(interval-(time()-prev_timer)*2)
      cur_value = snmp_u(host,snmp_comm,oid,snmp_parse_t[oid])
      cur_timer = time()
      for key in cur_value.keys():
        cv = float(cur_value.get(key))
        pv = float(prev_value.get(key))
        if cv < pv: cv = cv + max_value
        ret_dict[key] = (cv-pv)/(cur_timer-prev_timer)
      prev_value = cur_value
      prev_timer = cur_timer
      handle(ret_dict)
  else:
    sleep(interval-(time()-prev_timer))
    cur_value = snmp_u(host,snmp_comm,oid,snmp_parse_t[oid])
    cur_timer = time()
    for key in cur_value.keys():
      cv = float(cur_value.get(key))
      pv = float(prev_value.get(key))
      if cv < pv: cv = cv + max_value
      ret_dict[key] = (cv-pv)/(cur_timer-prev_timer)
    prev_value = cur_value
    prev_timer = cur_timer
  return ret_dict

if __name__ == '__main__':
#  for k in snmp_parse_t.keys():
#    print("获取数据: snmp_id:{}, parse_pattern:{}".format(k,snmp_parse_t[k]))
#    print(snmp_u('1.1.6.9', 'sicnu', k, snmp_parse_t[k]))
#    input("Press enter")
#  print(rate('1.1.6.9','sicnu','ifHCInOctets',cont=False))
  fetch_list = ['ifDescr','ifHCInUcastPkts','ifHCOutUcastPkts','ifHCInBroadcastPkts','ifHCOutBroadcastPkts','ifHCInMulticastPkts','ifHCOutMulticastPkts']
  prev_timer = time()
  prev = snmp_bw('1.1.6.9','sicnu',fetch_list)
  indexies = fetch_list[1:]
  prev_data = dict()
  for value in rt.values():
    prev = prev_data[value[0]] = value[1:]
