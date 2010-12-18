#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import re
import autosubsDownloader
import autosubsTranslate
import autosubsEncode

# CLASES DE ERROR

class Error(Exception):
  """Base class for exceptions in this module."""
  pass

class NoVariableError(Error):
  def __init__(self, variable):
    self.variable = variable
    print '\n  Se ha intentado acceder a la variable "%s" que no exixte' % variable

# CARGA DE LOS DATOS DEL PROYECTO

global code
global data
code = {}
data = {}


RE_LABEL = 'label\s+(.+)'

def pharse(project_file):
  global code
  f = open(project_file)
  lines = f.readlines()
  f.close()
  code['__labels__'] = ['__init__']
  code['__init__'] = []
  actual_label = '__init__'
  for line in lines:
    label = re.match(RE_LABEL, line)
    if label:
      label = label.group(1).strip()
      if label not in code['__labels__']:
        code['__labels__'].append(label)
        code[label] = []
      actual_label = label
    else:
      code[actual_label].append(line)

def ejectuta(label):
  global code
  if type(label) == int:
    label = code['__labels__'][label]
  for line in code[label]:
    try:
      exec line
    except:
      print >> sys.stderr, "ERROR en el archivo de proyecto:" 
      print >> sys.stderr, "  línea del error: \"%s\"" % line.rstrip()
      raise #Esto lanza la misma excepción que se acaba de producir

def getcap():
  'SERIE: %s' % getvar('serie')
  while True:
    capitulo = raw_input('Nº del capítulo: ')
    if capitulo.isdigit():
      break
  tovar('capitulo', capitulo)

def getlabels2exec():
  global code
  print 'ETIQUETAS:'
  for i in range(1,len(code['__labels__'])):
    print '  %d- %s' % (i, code['__labels__'][i])
  print 'Escribe el número de las etiquetas a ejectuar'
  get = raw_input('>> ')
  salida = []
  warnings = False
  for palabra in get.split(' '):
    if palabra.isdigit():
      num = int(palabra)
      if num > 0 and num <= len(code['__labels__']):
        salida.append(num)
      else:
        warnings = True
        print 'warning: %d está fuera de rango' % num
    else:
      if palabra in code['__labels__']:
        salida.append(palabra)
      else:
        warnings = True
        print 'warning: la etiqueta "%s" no existe' % palabra
  if warnings:
    print 'Hay varias etiquetas no válidas que no se tendrán en cuenta.'
    cont = raw_input("¿Desea continuar? (N/s): ").lower()
    if cont != s:
      exit(2)
  return salida

def makecapdir():
  d = os.path.join(getvar('dir', './'), getvar('capitulo'))
  if not os.path.lexists(d):
    os.mkdir(d)
  for x in getvar('subdirs', []):
    dd = os.path.join(d, x)
    if not os.path.lexists(dd):
      os.mkdir(dd)



# -----------------------------------------
# | FUNCIONES UTILIZABLES POR EL PROYECTO |
# -----------------------------------------

def tovar(var, valor):
  global data
  data[var] = valor

def getvar(var, valor_por_defecto='\0'):
  global data
  if var not in data:
    if valor_por_defecto == '\0':
      raise NoVariableError(var)
    else:
      return valor_por_defecto
  else:
    return data[var]

def pausa():
  """Realiza una pausa en el programa hasta que el usuario escriba 'continuar'"""
  while True:
    if raw_input("PAUSADO, escriba 'continuar': ") == 'continuar':
      break

def wait_and_download(size=None, otros_patrones=None):
  torrent =autosubsDownloader.waitfile(getvar('serie'), getvar('fansubfrom'), \
      getvar('capitulo'), getvar('size', None), getvar('patrones', None))
  return downloadtorrent(torrent[1])

def extractraw(file_from, raw_file):
  autosubsDownloader.mkv2raw(file_from, raw_file, getvar('fps', None))

def extractass(file_from, ass_file):
  autosubsDownloader.mkv2ass(file_from, ass_file)

def asstranslate(ass_from, ass_to):
  langin = getvar('langin', None)
  langout = getvar('langout', None)
  if langin and langout:
    autosubsTranslate.asstranslate(ass_from, ass_to, langin, langout)
  elif langin:
    autosubsTranslate.asstranslate(ass_from, ass_to, lang_from=langin)
  elif langout:
    autosubsTranslate.asstranslate(ass_from, ass_to, lang_to=langout)
  else:
    autosubsTranslate.asstranslate(ass_from, ass_to)

def assdefaultstyle(ass_file, fontname='Arial', fontsize='30', \
    primarycolour='&H00FFFFFF', secondarycolour='&H000000FF', \
    outlinecolour='&H00000000', backcolour='&H00000000', bold='-1', \
    italic='0', underline='0', strikeout='0', scalex='100', scaley='100', \
    spacing='1', angle='0', borderstyle='1', outline='2', shadow='0', \
    alignment='2', marginl='15', marginr='30', marginv='15', encoding='1'):
  autosubsTranslate.assStyleClear(ass_file)
  autosubsTranslate.assStyleSet(ass_file, 'Default', fontname, fontsize, \
    primarycolour, secondarycolour, \
    outlinecolour, backcolour, bold, \
    italic, underline, strikeout, scalex, scaley, \
    spacing, angle, borderstyle, outline, shadow, \
    alignment, marginl, marginr, marginv, encoding)

if __name__ == '__main__':
  if len(sys.argv) > 1:
    project_file = sys.argv[1]
  else:
    project_file = 'autosubs.project'
  if not os.path.isfile(project_file):
    print >> sys.stderr, 'ERROR no existe el archivo de proyecto "%s"' % project_file
    exit(-1)
  pharse(project_file)
  ejectuta('__init__')
  getcap()
  makecapdir()
  labels = getlabels2exec()
  for label in labels:
    ejectuta(label)

