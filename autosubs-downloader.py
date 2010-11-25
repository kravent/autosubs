#!/usr/bin/env python3.1
# -*- coding: utf-8 -*-
import sys
from urllib.request import urlopen
import re
import time

def geturifile(serie,fansub,capitulo,size='720',otros_patrones=None):
  serie=serie.lower()
  page='http://www.nyaatorrents.org/?page=search&cat=0_0&filter=0&term='+serie.replace(' ','+')
  try:
    file=urlopen(page)
    pagina=str(file.read())
    file.close()
    for line in re.findall('<td class="tlistname">.*?</td>',pagina):
      name=re.sub('<.*?>','',line).strip()
      dname=name.lower()
      url='http://www.nyaatorrents.org/?page=download&'+re.findall('tid=\d+',line)[0]
      if (re.search('\['+fansub+'\]',dname) and re.search(serie,dname) and
          re.search('\D'+capitulo+'\D',dname) and
          (re.search(size+'p',dname) or re.search('x'+size,dname))):
        if otros_patrones:
          valido=True
          for patron in otros_patrones:
            if !re.search(patron,dname):
              valido=False
          if valido:
            return [name,url]
        else:
          return [name,url]
  except:
    print('Error al acceder a la web',file=sys.stderr)


def waitfile(serie,fansub,capitulo,size='720',mkv=True):
  while True:
    print('Buscando capítulo...',end="\r")
    file=geturifile(serie,fansub,capitulo,size,mkv)
    if file:
      print('ENCONTRADO "',file[0],'"',sep='')
      return file
    print(time.strftime("%H:%M:%S", time.gmtime()),'-> LINK NO DISPONIBLE (esperando 10 min)',end="\r")
    time.sleep(600)




if __name__ == '__main__':
  res=waitfile(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
  print(res)
