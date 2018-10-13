from snmp_util import *

def ifnames(host,snmp_co):
  return snmp_u(host,snmp_co,"ifDescr",snmp_parse_t['ifDescr'])

def interface_broadcast(host,snmp_co):
  interfaces = ifnames(host,snmp_co)
  rd = dict()
  bc_in = snmp_u(host,snmp_co,'ifHCInBroadcastPkts',snmp_parse_t['ifHCInBroadcastPkts'])
  bc_out = snmp_u(host,snmp_co,'ifHCOutBroadcastPkts',snmp_parse_t['ifHCOutBroadcastPkts'])
  for key in bc_in.keys():
    rd[interfaces[key]] = (float(bc_in[key]),float(bc_out[key]))
  return rd

def compute_rate(cur,prev,interval,cb=64):
  max_value = pow(2,cb) - 1
  ret_dict = dict()
  if cur < prev: cur = cur + max_value
  return (cur-prev)/interval

def monitor(triger=None, interval=300):
  pass

def interface_multicast(host,snmp_co):
  pass

def interface_normal(host,snmp_co):
  pass
