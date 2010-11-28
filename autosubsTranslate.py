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


def gtranslate(text, lang_from="en", lang_to="es"):
    urllib.FancyURLopener.version = "Mozilla/5.0 (X11; U; Linux i686; en-US; rv:1.9.0.1) Gecko/2008070400 SUSE/3.0.1-0.1 Firefox/3.0.1"
    data = urllib.urlencode({"sl":lang_from, "tl":lang_to, "text":text})
    page = urllib.urlopen("http://translate.google.com/translate_t", data)
    content = page.read().decode('utf-8')
    page.close()
    res = re.search('<.*?id=result_box.*?((<span.*?</span>)*)</span>',content)
    if not res:
      res
    res = re.sub('</*span.*?>','',res.group(1))
    return mejoraformato(htmldecode(res))





if __name__ == '__main__':
  t = gtranslate(sys.argv[1])
  print t
  print repr(t)

