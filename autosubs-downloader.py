#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
import sys
import urllib
import re
import time

def getNyaTorrentsFile(serie,fansub,capitulo,size='720',otros_patrones=None):
  serie=serie.lower()
  page='http://www.nyaatorrents.org/?page=search&cat=0_0&filter=0&term='+serie.replace(' ','+')
  try:
    file=urllib.urlopen(page)
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
    print >> sys.stderr, 'Error al acceder a la web'



def waitfile(serie,fansub,capitulo,size='720',otros_patrones=None):
  while True:
    print 'Buscando capítulo...\r',
    file=getNyaTorrentsFile(serie,fansub,capitulo,size,otros_patrones)
    if file:
      print 'ENCONTRADO "'+file[0]+'"'
      return file
    print time.strftime("%H:%M:%S", time.gmtime()),'-> LINK NO DISPONIBLE (esperando 10 min)\r',
    time.sleep(600)




if __name__ == '__main__':
  res=waitfile(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
  print(res)
