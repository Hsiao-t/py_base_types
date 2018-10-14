#!/usr/bin/python

snmp_cfg = '/opt/.security_data/snmp_info.py'
from imp import load_source
from snmp_util import *
from nm_dict import *

def get_snmp_info(cfg,dev):
  snmp_info = load_source('snmpinfo',cfg).snmp_info
  return snmp_info.get(dev)

snmp_co = get_snmp_info(snmp_cfg,'1.1.6.9')

ifnames = snmp_u('1.1.6.9',snmp_co,'ifDescr',snmp_parse_t['ifDescr'])
u_cast = {}
b_cast = {}
m_cast = {}


