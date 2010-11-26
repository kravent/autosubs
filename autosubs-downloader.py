#!/usr/bin/env python2.6
# -*- coding: utf-8 -*-
import sys
import os
import urllib
import re
import time
import libtorrent

def getNyaTorrentsFile(serie,fansub,capitulo,size='720',otros_patrones=None):
  serie = serie.lower()
  page = 'http://www.nyaatorrents.org/?page=search&cat=0_0&filter=0&term='+serie.replace(' ','+')
  try:
    file = urllib.urlopen(page)
    pagina = str(file.read())
    file.close()
    for line in re.findall('<td class="tlistname">.*?</td>',pagina):
      name = re.sub('<.*?>','',line).strip()
      dname = name.lower()
      url='http://www.nyaatorrents.org/?page=download&'+re.findall('tid=\d+',line)[0]
      if (re.search('\['+fansub+'\]',dname) and re.search(serie,dname) and
          re.search('\D'+capitulo+'\D',dname) and
          (re.search(size+'p',dname) or re.search('x'+size,dname))):
        if otros_patrones:
          valido = True
          for patron in otros_patrones:
            if not re.search(patron,dname):
              valido = False
          if valido:
            return [name,url]
        else:
          return [name,url]
  except:
    print >> sys.stderr, 'Error al acceder a la web'



def waitfile(serie,fansub,capitulo,size='720',otros_patrones=None):
  while True:
    print 'Buscando capítulo...',
    sys.stdout.flush()
    file=getNyaTorrentsFile(serie,fansub,capitulo,size,otros_patrones)
    if file:
      print 'ENCONTRADO "'+file[0]+'"'
      return file
    print 'LINK NO DISPONIBLE'
    print time.strftime("%H:%M:%S", time.gmtime()),'LINK NO DISPONIBLE -> (esperando 10 min)'
    time.sleep(600)


class TorrentProgress:
  def __init__(self):
    pass
  def setProgress(self,progress,download_rate,upload_rate,num_peers):
    print "\r%3.2f%% complete (down: %4.1f kb/s up: %4.1f kB/s peers: %3d)" % \
          (progress * 100, download_rate / 1000, \
          upload_rate / 1000, num_peers) ,#Coma final -> NO "\n"
    sys.stdout.flush()



def downloadtorrent(torrentfile,destino='./',puertos=[51413,51413]):
  print 'DESCARGANDO...'
  ses = libtorrent.session()
  ses.listen_on(puertos[0], puertos[1])
  
  if re.search('^http://',torrentfile) or re.search('^https://',torrentfile):
    e = libtorrent.bdecode(urllib.urlopen(torrentfile).read())
  else:
    e = libtorrent.bdecode(open(torrentfile, 'rb').read())
  info = libtorrent.torrent_info(e)
  h = ses.add_torrent(info, destino)

  progreso=TorrentProgress()
  while (not h.is_seed()):
    s = h.status()
    progreso.setProgress(s.progress,s.download_rate,s.upload_rate,s.num_peers)
    time.sleep(1)
  s = h.status()
  progreso.setProgress(s.progress,s.download_rate,s.upload_rate,s.num_peers)

  filesaved=info.name()
  ses.remove_torrent(h)
  print "\nGUARDADO: \"%s\"" % filesaved
  return filesaved



if __name__ == '__main__':
  """
  if len(sys.argv) < 4:
    print 'USO: autosubs-downloader.py serie fansub capitulo [resolucion]', \
        '[patron_regular1 patron_regular2 ...]'
    exit(-1)
  elif len(sys.argv) == 4:
    res = waitfile(sys.argv[1],sys.argv[2],sys.argv[3])
  elif len(sys.argv) == 5:
    res = waitfile(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
  else:
    res = waitfile(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4],sys.argv[5:])

  downloadtorrent(res[1])
  """
  downloadtorrent('http://www.nyaatorrents.org/?page=download&tid=176003')
