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

$code = {}
$data = {}


RE_LABEL = 'label\s+(.+)'

def pharse(project_file):
  f = open(project_file)
  $code['__labels__'] = ['__init__']
  $code['__init__'] = []
  actual_label = '__init__'
  for line in f.readline():
    label = re.match(RE_LABEL, line)
    if label:
      label = label.group(1).strip()
      if label not in code['__labels__']:
        $code['__labels__'].append(label)
        $code[label] = []
      actual_label = label
    else:
      $code[label].append(line)
  f.close()

def ejectuta(label):
  if type(label) == int:
    label = $code['__labels__'][label]
  for line in $code[label]:
    exec line

def getcap():
  'SERIE: %s' % getvar('serie')
  while True:
    capitulo = raw_input('Nº del capítulo: ')
    if capitulo.isdigit():
      break
  tovar('capitulo', capitulo)

def getlabels2exec():
  print 'ETIQUETAS:'
  for i in range(1,len($code['__labels__'])):
    print '  %d- %s' % (i, $code['__labels__'])
  print 'Escribe el número de las etiquetas a ejectuar'
  get = raw_input('>> ')
  salida = []
  for palabra in get.split(' '):
    if palabra.isdigit():
      num = int(palabra)
      if num > 0 and num <= len($code['__labels__'])
        salida.append(num)
  return salida

def makecapdir():
  root = getvar('dir','./')
  d = os.path.join(root, getvar('capitulo'))
  if not getvar('capitulo') in os.listdir(root):
    os.mkdir(d)
    for x in getvar('subdirs', [])
      os.mkdir(os.path.join(d, x))



# -----------------------------------------
# | FUNCIONES UTILIZABLES POR EL PROYECTO |
# -----------------------------------------

def tovar(var, valor):
  $data[var] = valor

def getvar(var, valor_por_defecto='\0'):
  if var not in $data:
    if valor_por_defecto == '\0':
      raise NoVariableError(var)
    else:
      return valor_por_defecto
  else:
    return $data[var]

def pausa():
  """Realiza una pausa en el programa hasta que el usuario escriba 'continuar'"""
  while True:
    if raw_input("PAUSADO, escriba 'continuar': ") == 'continuar':
      break

def wait_and_download(size=None, otros_patrones=None):
  autosubsDownloader.waitfile(getvar('serie'), getvar('fansubfrom'), \
      getvar('capitulo'), getvar('size', None), getvar('patrones', None))
      
def extractraw(file_from, raw_file):
  autosubsDownloader.mkv2raw(file_from, raw_file, getvar('fps', None))

def extractass(file_from, ass_file):
  autosubsDownloader.mkv2ass(file_from, ass_file)



if __name__ == '__main__':
  if len(sys.argv) > 1:
    project_file = sys.argv[1]
  else:
    project_file = 'autosubs.project'
  pharse(project_file)
  ejectuta('__init__')
  getcap()
  makecapdir()
  labels = getlabels2exec()
  for label in labels:
    ejectuta(label)

