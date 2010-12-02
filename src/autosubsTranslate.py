#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import urllib
import copy
import re
import codecs


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


def gtranslate(text, lang_from='en', lang_to='es'):
    urllib.FancyURLopener.version = 'Mozilla/5.0 (X11; U; Linux i686; \
        en-US; rv:1.9.0.1) Gecko/2008070400 SUSE/3.0.1-0.1 Firefox/3.0.1'
    data = urllib.urlencode({'sl':lang_from, 'tl':lang_to, 'text':text.encode('utf-8')})
    page = urllib.urlopen('http://translate.google.com/translate_t', data)
    content = page.read().decode('utf-8')
    page.close()
    res = re.search('<.*?id=result_box.*?((<span.*?</span>)*)</span>',content)
    if not res:
      res
    res = re.sub('</*span.*?>','',res.group(1))
    return mejoraformato(htmldecode(res))


def asstranslate(ass_in, ass_out, lang_from='en', lang_to='es'):
  f_in = codecs.open(ass_in, encoding='utf-8')
  lines = f_in.readlines()
  n = len(lines)
  f_in.close()
  f_out = codecs.open(ass_out, mode='w', encoding='utf-8')
  for i in range(0, n):
    print 'Traduciendo linea: %d/%d\r' % (i+1, n),
    sys.stdout.flush()
    line = lines[i].strip()
    line = re.sub('\s*\\\\N\s*', ' ', line)
    line = re.sub('\{\\\\be\d+\}', '', line)
    m = re.search('Dialogue:((.*?,){9})(.*)', line)
    if m:
      f_out.write('Dialogue:')
      f_out.write(m.group(1))
      f_out.write(gtranslate(m.group(3), lang_from, lang_to))
    else:
      f_out.write(line)
    f_out.write("\n")
  f_out.close()
  print


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

