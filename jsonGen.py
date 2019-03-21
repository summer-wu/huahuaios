"""数据都保存在这个文件内，用这个文件生成各个json。
因为json格式比较麻烦，用python的dict转为json易于修改。
只能从py->json，不支持反向转换！

生成的json文件，保存在单独分支
"""

import json
import os,sys
import glob

class BaseGen:
  def __init__(self, filename):
    self.filename = filename
    self.d = {}

  def gen(self):
    """生成json"""
    with open(self.filename, "w") as f:
      json.dump(self.d, f, indent=True, ensure_ascii=False)


####################
class EntryGen(BaseGen):
  """打开app的入口json"""

  def __init__(self):
    super().__init__('entry.json')
    self.d = self.getD()

  def getD(self):
    d = {}
    d['chinaEntry'] = 'https://sogou.com'
    d['foreignEntry'] = 'currency'
    d['availableCurrencies'] = self.get_availableCurrencies()
    d['flagsMapping'] = self.get_flagsMapping()
    d['rateMapping'] = self.get_rateMapping()
    return d

  def get_availableCurrencies(self):
    """可用的货币"""
    return ['美国', '欧盟', '日本',
            '英国', '印度', '巴西', '加拿大',
            '韩国', '俄罗斯']

  def get_flagsMapping(self):
    """国家->国旗 dict"""
    mapping = {'美国': 'us.png',
               '欧盟': 'europe.png',
               '日本': 'japan.png',
               '英国': 'britian.png',
               '印度': 'indian.png',
               '巴西': 'brazil.png',
               '加拿大': 'canada.png',
               '韩国': 'korea.png',
               '俄罗斯': 'russia.png'}

    for country,filename in mapping.items():
      mapping[country] = f"flagImgs/{filename}"
    return mapping

  def get_rateMapping(self):
    """国家->汇率。100外币对应??人民币，
    参见 中国人民银行货币财政司（不全） http://www.pbc.gov.cn/zhengcehuobisi/125207/125217/125925/index.html
    中国银行 外汇牌价 http://www.boc.cn/sourcedb/whpj/
    """
    mapping = {'美国': 668.5,
               '欧盟': 763.76,
               '日本': 6.035,
               '英国': 882.12,
               '印度': 9.7107,
               '巴西': 176.93,
               '加拿大': 502.73,
               '韩国': 0.5934	,
               '俄罗斯': 10.47	}
    return mapping

####################
class PicModel:
  """表示一张图片"""
  def __init__(self,filename):
    self.filename = filename
    basename = os.path.basename(filename)
    namepart = basename.split(".")[0]
    parts =namepart.split("_")
    assert len(parts)==2
    self.mianE = int(parts[0])
    self.face = parts[1]

  def compareKey(self):
    k = f"{self.mianE:5}_{self.face}"
    return k

  def __str__(self):
    s = f"{self.filename}"
    return s
  __repr__ = __str__

  def dictRepr(self):
    if self.face == 'a':
      faceCN = '正面'
    else:
      faceCN = '背面'
    d = {'mianE':self.mianE,
         'face':faceCN,
         'filename':self.filename,}
    return d

#############
class CurrencyModel:
  """表示某个货币，对应一个文件夹"""
  def __init__(self,dirpath):
    infoPyPath = os.path.join(dirpath,'info.py')
    assert os.path.exists(infoPyPath)
    with open(infoPyPath, 'rt') as f:
      text = f.read(9999)
      locals = {}
      exec(text, None, locals)
    self.dirpath = dirpath
    self.country = locals['country']
    self.currencyName = locals['currencyName']
    self.symbol = locals['symbol']
    self.iso_code = locals['iso_code']
    self.country_description = locals['country_description']

  def dictRepr(self):
    d = {"country":self.country,
         'currencyName':self.currencyName,
         'symbol':self.symbol,
         'iso_code':self.iso_code,
         "full_description":self.full_description(),
         "pics":self.get_pics()}
    return d

  def full_description(self):
    desc = f"{self.country_description} {self.country}的官方货币名称为{self.currencyName}。符号为{self.symbol}，ISO货币代码为{self.iso_code}。"
    return desc

  def get_pics(self)->list:
    """pics是一个list，显示时从前到后显示"""
    jpgs = glob.glob(f"{self.dirpath}/*_?.jpg")
    pngs = glob.glob(f"{self.dirpath}/*_?.png")
    files = []
    files.extend(jpgs)
    files.extend(pngs)

    models = []
    for filename in files:
      model = PicModel(filename)
      models.append(model)

    models = sorted(models,key=PicModel.compareKey)

    pics = []
    for m in models:
      pics.append(m.dictRepr())
    return pics




####################
class CurrenciesGen(BaseGen):
  """一个json，保存所有的货币"""
  def __init__(self):
    filename = f"currencies.json"
    super().__init__(filename)
    self.d = self.getD()

  def getD(self):
    """格式是 country->CurrencyModel """
    d = {}
    for m in self.iterCurrencyImgs():
      d[m.country] = m.dictRepr()
    return d

  def iterCurrencyImgs(self)->list:
    """遍历 currencyImgs 目录"""
    dirs = glob.glob('currencyImgs/*')
    models = []
    for dir in dirs:
      m = CurrencyModel(dir)
      models.append(m)
    return models



if __name__ == '__main__':
  EntryGen().gen()
  CurrenciesGen().gen()
  # m = CurrencyModel.fromDir('currencyImgs/brazil_real')
  # models = m.get_pics()
  # print(models)