"""
@module_name: nm_dict
@author: Hsiao-t
@funct: 一个命名数字列表，用于完成简单四则运算，可以对列表内相同key的数据进行简单四则运算

"""
class nm_dict(object):
  def __init__(s,dict_data):
    s._data = dict()
    if type(dict_data) is dict:
      for key in dict_data.keys():
        try: s._data[key] = float(dict_data[key])
        except: s._data[key] = 0.0
    else:
      err_data = "Only numeric data can be passed in.\nPassed data:{}".format(dict_data)
      raise ValueError(err_data)

  def __setitem__(s,key,value):
    if type(value) is int or type(value) is float(value):
      s._data[key] = value
    else:
      try: s._data[key]=float(value)
      except: s._data[key]=0.0

  def __getitem__(s,key):
    return s._data.get(key)

  def __add__(s,op2):
    ret_dict = dict()
    if type(op2) is dict or type(op2) is nm_dict:
      keys = s._data.keys() & op2.keys()
      for key in keys: ret_dict[key] = s._data[key] + op2.get(key)
    elif type(op2) is int or type(op2) is float:
      for key in s._data.keys(): ret_dict[key] = s._data[key] + op2
    else:
      try: ret_dict[key] = s._data[key] + float(op2)
      except: ret_dict[key] = s._data[key]
    return nm_dict(ret_dict)

  def __sub__(s,op2):
    ret_dict = dict()
    if type(op2) is dict or type(op2) is nm_dict:
      keys = s._data.keys() & op2.keys()
      for key in keys: ret_dict[key] = s._data[key] - op2.get(key)
    elif type(op2) is int or type(op2) is float:
      for key in s._data.keys(): ret_dict[key] = s._data[key] - op2
    else:
      try: ret_dict[key] = s._data[key] - float(op2)
      except: ret_dict[key] = s._data[key]
    return nm_dict(ret_dict)

  def __mul__(s,op2):
    ret_dict = dict()
    if type(op2) is dict or type(op2) is nm_dict:
      keys = s._data.keys() & op2.keys()
      for key in keys: ret_dict[key] = s._data[key] * op2.get(key)
    elif type(op2) is int or type(op2) is float:
      for key in s._data.keys(): ret_dict[key] = s._data[key] * op2
    else:
      try: ret_dict[key] = s._data[key] * float(op2)
      except: ret_dict[key] = s._data[key]
    return nm_dict(ret_dict)

  def __truediv__(s,op2):
    ret_dict = dict()
    if type(op2) is dict or type(op2) is nm_dict:
      keys = s._data.keys() & op2.keys()
      for key in keys: ret_dict[key] = s._data[key] / op2.get(key)
    elif type(op2) is int or type(op2) is float:
      for key in s._data.keys(): ret_dict[key] = s._data[key] / op2
    else:
      try: ret_dict[key] = s._data[key] / float(op2)
      except: ret_dict[key] = s._data[key]
    return nm_dict(ret_dict)

  def keys(s):
    return s._data.keys()

  def values(s):
    return s._data.values()

  def get(s,key):
    return s._data.get(key)

  def adjust(s,cb=64):
    max_value = pow(2,cb) - 1
    ret_dict = dict()
    for key in s._data.keys():
      if s._data[key] < 0 : ret_dict[key] = s._data[key] + max_value
      else: ret_dict[key] = s._data[key]
    return nm_dict(ret_dict)
