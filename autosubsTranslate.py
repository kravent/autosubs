#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib
import copy
import re

#sys.setdefaultencoding("utf-8") 

def htmldecode(text):
  text = text.replace('&lt;','<').replace('&gt;','>')
  text = text.replace('&#39;',"'").replace('&quot;','"')
  text = text.replace('&amp;','&')
  return text


def mejoraformato(text):
  print repr(text)
  n = len(text)
  i=0
  while i < n:
    print i, '/', n, '(', text[i], ')', text
    if text[i] == '!':
      j=i-2
      while text[j] != u'¡':
        if j <= -1:
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
      j=i-2
      while text[j] != u'¿':
        if j <= -1:
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


def gtranslate(text, lang_from='en', lang_to='es'):
    urllib.FancyURLopener.version = 'Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008070400 SUSE/3.0.1-0.1 Firefox/3.0.1'
    data = urllib.urlencode({'sl':lang_from, 'tl':lang_to, 'text':text})
    page = urllib.urlopen('http://translate.google.com/translate_t', data)
    content = page.read().decode('utf-8')
    page.close()
    res = re.search('<.*?id=result_box.*?((<span.*?</span>)*)</span>',content)
    if not res:
      res
    res = re.sub('</*span.*?>','',res.group(1))
    return mejoraformato(htmldecode(res))


def asstranslate(ass_in, ass_out, lang_from='en', lang_to='es'):
  f_in = open(ass_in)
  lines = f_in.readlines()
  n = len(lines)
  f_in.close()
  f_out = open(ass_out, 'w')
  for i in range(0, n):
    print 'Traduciendo linea: %d/%d' % (i+1, n),
    sys.stdout.flush()
    line = lines[i].strip()
    line = re.sub('\s*\\N\s*', ' ', line)
    line = re.sub('\{\\be\d+\}', '', line)
    m = re.search('Dialoge:(.*?,){9}(.*)', line])
    if m:
      f_out.write(m.group(1))
      f_out.write(gtranslate(line, lang_from, lang_to))
    else:
      f_out.write(line)
    f_out.write("\n")
    f_out.close()
    print
  



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

