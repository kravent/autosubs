#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib, urllib2
import copy
import re
import codecs
import threading
import time
import simplejson


def htmldecode(text):
  text = text.replace('&lt;','<').replace('&gt;','>')
  text = text.replace('&#39;',"'").replace('&quot;','"')
  text = text.replace('&amp;','&')
  return text


def mejoraformato(text):
  n = len(text)
  i=0
  while i < n:
    if text[i] == '!':
      salto = re.search('(\s*[.?!]\s*)*$',text[:i+1])
      if salto:
        nsalto = 1+len(salto.group(0))
      else:
        nsalto = 1
      j = i-nsalto
      while j < 0 or text[j] != u'¡':
        if j < 0:
          text = u'¡' + text
          n += 1
          i += 1
          break
        elif text[j] == '!' or text[j] == '?' or text[j] == '.':
          text = text[:j+1] + u'¡' + text[j+1:]
          n += 1
          i += 1
          break
        j -= 1
    elif text[i] == '?':
      salto = re.search('(\s*[.?!]\s*)*$',text[:i+1])
      if salto:
        nsalto = 1+len(salto.group(0))
      else:
        nsalto = 1
      j = i-nsalto
      while j < 0 or text[j] != u'¿':
        if j < 0:
          text = u'¿' + text
          n += 1
          i += 1
          break
        elif text[j] == '!' or text[j] == '?' or text[j] == '.':
          text = text[:j+1] + u'¿' + text[j+1:]
          n += 1
          i += 1
          break
        j -= 1
    i += 1
  text = re.sub(u'\s*¿\s*',u' ¿',text)
  text = re.sub(u'\s*¡\s*',u' ¡',text)
  text = re.sub('\s*\?\s*','? ',text)
  text = re.sub('\s*!\s*','! ',text)
  text = re.sub('\s*\.\s*','. ',text)
  text = re.sub('\s*\.\s*\.\s*\.\s*','... ',text)
  text = re.sub('\s*\?\s*!\s*','?! ',text)
  text = re.sub('\s*!\s*\?\s*','!? ',text)
  text = re.sub(u'\s*¿\s*¡\s*',u' ¿¡',text)
  text = re.sub(u'\s*¡\s*¿\s*',u' ¡¿',text)
  text = re.sub(u'^\s*¿\s*',u'¿',text)
  text = re.sub(u'^\s*¡\s*',u'¡',text)
  return text


GTRANSLATOR_URL = 'http://ajax.googleapis.com/ajax/services/language/translate'
NRECONECTIONS = 10
RECONECTIONSLEEP = 15
def gtranslate(text, lang_from='en', lang_to='es'):
  try:
    params = urllib.urlencode({'langpair': '%s|%s' % (lang_from, lang_to),
             'v': '1.0',
             'q': text.encode('ascii', 'xmlcharrefreplace')
             })
    resp = simplejson.load(urllib2.urlopen(GTRANSLATOR_URL, params))
    if resp['responseStatus']==200:
      return mejoraformato(resp['responseData']['translatedText'])
    print >> sys.stderr, '\nERROR al traducir "%s"' % text.encode('ascii', 'xmlcharrefreplace')
    print >> sys.stderr, '  responseStatus:', resp['responseStatus']
    print >> sys.stderr, '  responseDetails:', resp['responseDetails']
  except urllib2.HTTPError, e:  
    print >> sys.stderr, '\nERROR al traducir "%s"' % text.encode('ascii', 'xmlcharrefreplace')
    print >> sys.stderr, e.code
  except urllib2.URLError, e:  
    print >> sys.stderr, '\nERROR al traducir "%s"' % text.encode('ascii', 'xmlcharrefreplace')
    print >> sys.stderr, e.reason
  return None

th_n = 0
th_lista = []
th_lbool = []
th_loock = threading.Lock()
th_error = False

def savelistafrases(lista):
  global th_n
  global th_lista
  global th_lbool
  th_n = len(lista)
  th_lista = lista
  th_lbool = []
  for i in range(0, th_n):
    th_lbool.append(0)

def getnfrase():
  global th_loock
  global th_n
  global th_lista
  global th_lbool
  th_loock.acquire()
  res = None
  for i in range(0, th_n):
    if not th_lbool[i]:
      th_lbool[i] = 1
      res = i
      break
  th_loock.release()
  return res

def getfrase(n):
  global th_lista
  return th_lista[n]

def savefrase(n, frase):
  global th_loock
  global th_lista
  global th_lbool
  th_loock.acquire()
  th_lbool[n] = 2
  th_lista[n] = frase
  th_loock.release()

def syncfrasestofile(fileobject):
  global th_n
  global th_lista
  global th_lbool
  ntraducidas = 0
  traducir = True
  for i in range(0, th_n):
    if th_lbool[i] < 2:
      traducir = False
    elif th_lbool[i] >= 2:
      ntraducidas += 1
      if traducir and th_lbool[i] == 2:
        fileobject.write(th_lista[i])
        th_lbool[i] = 3
  return ntraducidas

class ThreadTraduceFrases(threading.Thread):
  def __init__(self, lang_from='', lang_to='es'):
    threading.Thread.__init__(self)
    self.lang_from = lang_from
    self.lang_to = lang_to
    self.killed = False
  def run(self):
    while not self.killed:
      n = getnfrase()
      if n == None:
        break
      line = getfrase(n).strip()
      line = re.sub('\s*\\\\N\s*', ' ', line)
      line = re.sub('\{\\\\be\d+\}', '', line)
      m = re.search('Dialogue:((.*?,){9})(.*)', line)
      if m:
        traduction = gtranslate(m.group(3), self.lang_from, self.lang_to)
        if not traduction:
          traduction = u'* ERROR AL TRADUCIR *'
        trad = u'Dialogue:' + m.group(1) + traduction
      else:
        trad = line
      trad = trad + u'\n'
      savefrase(n, trad)
  def stop(self):
    self.killed = True


NTHREADS = 1
REFRESHTIME = 1
def asstranslate(ass_in, ass_out, lang_from='', lang_to='es', nthreads=NTHREADS):
  global th_n
  print 'Preparando traductor...',
  sys.stdout.flush()
  f_in = codecs.open(ass_in, encoding='utf-8')
  lines = f_in.readlines()
  f_in.close()
  savelistafrases(lines)

  f_out = codecs.open(ass_out, mode='w', encoding='utf-8')
  threads = []
  try:
    for i in range(0, NTHREADS):
      threads.append(ThreadTraduceFrases(lang_from, lang_to))
    for th in threads:
      th.start()
    while True:
      time.sleep(REFRESHTIME)
      alive = True
      for th in threads:
        alive = alive and th.is_alive()
      nlinea = syncfrasestofile(f_out)
      print '\rTraducidas %d líneas de %d' % (nlinea, th_n),
      sys.stdout.flush()
      if not alive:
        break
  except:
    for th in threads:
      th.stop()
    raise
  f_out.close()
  print '\rTraducidas %d líneas de %d' % (th_n, th_n)


####################
#    ESTILOS ASS   #
####################

def assStyleClear(assfile):
  f = codecs.open(assfile, encoding='utf-8')
  text = f.readlines()
  f.close()
  existe = False
  for line in text:
    if re.search('\[.*Styles.*\]',line):
      existe = True
      break
  exit = u''
  i = 0
  n = len(text)
  if existe:
    sal = u''
    i = 0
    while not re.search('\[.*Styles.*\]', text[i]):
      sal = sal + text[i]
      i += 1
    sal = sal + u"[V4+ Styles]\nFormat: Name, Fontname, Fontsize, "
    sal = sal + u"PrimaryColour, SecondaryColour, OutlineColour, "
    sal = sal + u"BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, "
    sal = sal + u"ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
    sal = sal + u"Alignment, MarginL, MarginR, MarginV, Encoding\n\n"
    i = i+1 #Salto la linea de definición de estilos en la que todavía estoy
    while i < n and not re.match('\s*\[.*\]',text[i]):
      i += 1
    while i < n:
      sal = sal + text[i]
      i +=1
  else:
    sal = text.join('')
    sal = sal + u"\n\n[V4+ Styles]\nFormat: Name, Fontname, Fontsize, "
    sal = sal + u"PrimaryColour, SecondaryColour, OutlineColour, "
    sal = sal + u"BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, "
    sal = sal + u"ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, "
    sal = sal + u"Alignment, MarginL, MarginR, MarginV, Encoding\n\n"
  f = codecs.open(assfile, mode='w', encoding='utf-8')
  f.write(sal)
  f.close()


def assStyleSet(assfile, name, fontname='Arial', fontsize='30', \
    primarycolour='&H00FFFFFF', secondarycolour='&H000000FF', \
    outlinecolour='&H00000000', backcolour='&H00000000', bold='-1', \
    italic='0', underline='0', strikeout='0', scalex='100', scaley='100', \
    spacing='1', angle='0', borderstyle='1', outline='2', shadow='0', \
    alignment='2', marginl='15', marginr='30', marginv='15', encoding='1'):
  f = codecs.open(assfile, encoding='utf-8')
  lines = f.readlines()
  f.close()
  sal = u''
  i = 0
  n = len(lines)
  while not re.search('\[.*Styles.*\]', lines[i]):
    sal = sal + lines [i]
    i +=1
  sal = sal + lines[i]
  i += 1
  while re.match('\s*$', lines[i]):
    sal = sal + lines[i]
    i +=1
  while re.match('\s*Format:', lines[i]):
    sal = sal + lines[i]
    i += 1
  espaciado = u""
  while re.match('\s*$', lines[i]):
    espaciado = espaciado + lines[i]
    i +=1
  while re.match('\s*Style:', lines[i]):
    sal = sal + lines[i]
    i += 1
  sal = sal + "Style: %s,%s,%s,%s,%s,%s,%s,%s,%s,%s," %( \
      name, fontname, fontsize, primarycolour, secondarycolour, \
      outlinecolour, backcolour, bold, italic, underline)
  
  sal = sal + "%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n" %( \
      strikeout, scalex, scaley, spacing, angle, borderstyle, outline, \
      shadow, alignment, marginl, marginr, marginv, encoding)
  sal = sal + espaciado
  while i < n:
    sal = sal + lines[i]
    i += 1
  f = codecs.open(assfile, mode='w', encoding='utf-8')
  f.write(sal)
  f.close()




if __name__ == '__main__':
  nargs = len(sys.argv)
  if nargs < 3:
    print 'USO: autosubs-translate ass_in ass_out [lang_in [lang_out]]'
    exit(-1)
  elif nargs <= 3:
    asstranslate(sys.argv[1],sys.argv[2])
  elif nargs <=4:
    asstranslate(sys.argv[1],sys.argv[2],sys.argv[3])
  else:
    asstranslate(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])

