"""数据都保存在这个文件内，用这个文件生成各个json。
因为json格式比较麻烦，用python的dict转为json易于修改。
只能从py->json，不支持反向转换！

生成的json文件，保存在单独分支
"""

import json

class BaseGen:
  def __init__(self,filename):
    self.filename = filename
    self.d = {}

  def gen(self):
    """生成json"""
    with open(self.filename,"w") as f:
      json.dump(self.d,f,indent=True,ensure_ascii=False)


class EntryGen(BaseGen):
  def __init__(self):
    super().__init__('entry.json')
    self.d = self.getD()

  def getD(self):
    d = {}
    d['chinaEntry'] = ''
    d['foreignEntry'] = 'currency'
    d['availableCurrencies'] = self.get_availableCurrencies()
    return d

  def get_availableCurrencies(self):
    """可用的货币"""
    return ['美国','中国','欧盟','日本',
            '英国','印度','巴西','加拿大',
            '韩国','俄罗斯']




if __name__ == '__main__':
  EntryGen().gen()
