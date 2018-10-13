class nm_array(object):
  """
  创建只包含数字的列表，可以完成两个列表的简单四则运算
  --> 第二个操作数可以是数字，也可以是一个长度相同的列表
  --> 如果第二个操作数为数字，只将第一个操作数的每个元素与第二个元素进行运算，如果第二个操作数为列表，则将第一个操作数的每个元素分别与第二个操作数的每个元素进行运算。
  --> 初始化参数：一个列表、Tuple、或者一个数字
  """
  def __init__(s,data):
    s._data = []
    if type(data) is list or type(data) is tuple:
      for c in data:
        if type(c) is int or type(c) is float:
          s._data.append(c)
        else:
          try: s._data.append(float(c))
          except: s._data.append(0)
    elif type(data) is int or type(data) is float: s._data.append(data)
    else:
      try: s._data.append(float(data))
      except: pass

  def __add__(s,op2):
    ret_list = []
    if type(op2) is nm_array:
      if len(s._data) != len(op2._data): raise ValueError("Length of operands are not equal")
      for c in range(len(s._data)):
        ret_list.append(s._data[c] + op2._data[c])
      return nm_array(ret_list)
    elif type(op2) is list:
      if len(s._data) != len(op2): raise ValueError("Length of operands are not equal")
      for c in range(len(s._data)):
        ret_list.append(s._data[c] + op2[c])
      return nm_array(ret_list)
    else:
      return nm_array(ret_list)

  def __sub__(s,op2):
    ret_list = []
    if type(op2) is nm_array:
      if len(s._data) != len(op2._data): raise ValueError("Length of operands are not equal")
      for c in range(len(s._data)):
        ret_list.append(s._data[c] - op2._data[c])
      return nm_array(ret_list)
    elif type(op2) is list:
      if len(s._data) != len(op2): raise ValueError("Length of operands are not equal")
      for c in range(len(s._data)):
        ret_list.append(s._data[c] - op2[c])
      return nm_array(ret_list)
    else:
      return nm_array(ret_list)

  def __mul__(s,op2):
    ret_list = []
    if type(op2) is nm_array:
      if len(s._data) != len(op2._data): raise ValueError("Length of operands are not equal")
      for c in range(len(s._data)):
        ret_list.append(s._data[c] * op2._data[c])
      return nm_array(ret_list)
    elif type(op2) is list:
      if len(s._data) != len(op2): raise ValueError("Length of operands are not equal")
      for c in range(len(s._data)):
        ret_list.append(s._data[c] * op2[c])
      return nm_array(ret_list)
    elif type(op2) is int or type(op2) is float:
      for c in range(len(s._data)):
        ret_list.append(s._data[c] * op2)
      return nm_array(ret_list)
    else:
      return nm_array(ret_list)

  def __truediv__(s,op2):
    ret_list = []
    if type(op2) is nm_array:
      if len(s._data) != len(op2._data): raise ValueError("Length of operands are not equal")
      for c in range(len(s._data)):
        ret_list.append(s._data[c] / op2._data[c])
      return nm_array(ret_list)
    elif type(op2) is list:
      if len(s._data) != len(op2): raise ValueError("Length of operands are not equal")
      for c in range(len(s._data)):
        ret_list.append(s._data[c] / op2[c])
      return nm_array(ret_list)
    elif type(op2) is int or type(op2) is float:
      for c in range(len(s._data)):
        ret_list.append(s._data[c] / op2)
      return nm_array(ret_list)
    else:
      return nm_array(ret_list)

  def __iter__(s):
    for i in s._data:
      yield i

  def __getitem__(s,index):
    if index >= 0 and index < len(s._data):
      return s._data[index]
    else:
      raise ValueError("Index out of array")

  def append(s,num):
    if type(num) is int or type(num) is float:
      s._data.append(num)
    else:
      raise ValueError("Only numeric parameter is allowed")

