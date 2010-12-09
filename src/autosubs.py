#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os
import re
import autosubsDownloader
import autosubsTranslate
import autosubsEncode

FILEPROJECT_NAME = 'autosubs.project'

ALLOWED_CODES = [#TODO reg.exp. para los códigos permitidos en el archivo del proyecto
    'mkDir',
    'waitAndDownload\s+\w+$',
    'extractRAW\s+\w+\s+\w+$',
    'extractASS\s+\w+\s+\w+$',
    'translate\s+\w+\s+\w+$',
    'autotitle\s+\w+\s+\w+\s+\w+$',
    'encode\s+((mp4)|(avi))\s+\w+\s+\w+\s+\d+\s+(\w+)|(\*)\s+(\d+x\d+)|(\*)\s+(\w+)|(\*)\s+(True)|(False)$',
    'mkvmerge\s+\w+',
    'systemPAUSE$'
    ]

class Error(Exception):
  """Base class for exceptions in this module."""
  pass


class PharseError(Error):
  def __init__(self, filee, nline, line):
    self.filee = filee
    self.nline = nline
    self.line = line
    print self.__str__()
  def __str__(self):
    return '\n  Project source file:\n    Line %d: %s' % (self.nline, self.line)


class ExecuteError(Error):
  def __init__(self, description):
    self.description = description
  def __str__(self):
    return '\n' + self.description


class Project:
  def __init__(self, projectFile):
    self.data = {}
    self.code = {}
    self.etiquetas = []
    f = open(projectFile)
    nline = 0
    for line in f:
      nline += 1
      line = line.strip()
      if re.match('\[\s*\w+\s*\]',line):
        m = re.match('\[\s*(\w+)\s*\]',line).group(1)
        self.code[m] = []
        self.etiquetas.append(m)
      elif line != '':
        if len(self.etiquetas) > 0:
          self.addCode(self.etiquetas[-1], projectFile, nline, line)
        else:
          self.addData(projectFile, nline, line)
    f.close()
    #TODO pedir nº capitulo -> self.capitulo
    #TODO pedir etiquetas a ejecutar

  def addData(self, filee, nline, line):
    if re.match('\w+=',line):
      line  = line.split('=',1)
      self.data[line[0].strip()] = line[1].strip()
    else:
      raise PharseError(filee, nline, line)

  def addCode(self, etiqueta, filee, nline, line):
    if self.isValidCode(line):
      self.code[etiqueta].append(line.split(' '))
    else:
      raise PharseError(filee, nline, line)

  def isValidCode(self, line):
    for exp in ALLOWED_CODES:
      if re.match(exp, line):
        return True
    return False

  def getvar(self, var, default=''):
    """Si var=='*' o no existe en self.data devuelve default,
    y si no devuelve self.data[var]."""
    if var == '*' or (var != '' and not var in self.data):
      return default
    elif var in self.data:
      return self.data[var]
    else:
      raise ExecuteError('No existe la variable "%s"' % var)

  def savevar(self, var, data):
    """Guarda data en la variable var de self.data"""
    self.data[var] = data

  def execEtiqueta(self, etiqueta):
    for code in self.code[etiqueta]:
      self.execCode(code)

  def execCode(self, code):
    if code[0] == 'mkDir': # mkDir
      if not self.capitulo in os.listdir('./'):
        os.mkdir(self.capitulo)
    elif code[0] == 'waitAndDownload': # waitAndDownload
      aux = autosubsDownloader.waitfile(self.getvar('serie'), \
          self.getvar('fansub'), self.capitulo, \
          self.getvar('size', None), self.getvar('patrones', None))
      name = autosubsDownloader.downloadtorrent(aux[1], self.capitulo)
      self.savevar(code[1], name)
    elif code[0] == 'extractRAW': # extractRAW
      autosubsDownloader.mkv2raw(self.getvar(code[1]), self.getvar(code[2]), \
          self.getvar('fps', None))
    elif code[0] == 'extractASS': # extractASS
      autosubsDownloader.mkv2ass(self.getvar(code[1]), self.getvar(code[2]))
    elif code[0] == 'translate': # translate
      autosubsTranslate.asstranslate(self.getvar(code[1]), self.getvar(code[2]), \
          self.getvar('langin', 'en'))
    elif code[0] == 'autotitle': # autotitle
      self.savevar(code[1], '[%s] %s - %s (%sp).%s' % (\
          self.getvar('fansubS'), self.getvar('serie'), self.capitulo, \
          code[2], code[3]))
    elif code[0] == 'encode': # encode
      resize =  self.getvar(code[6], None)
      if resize:
        resize = resize.split('x')
      autosubsEncode.encodeAvidemux(self.getvar(code[2]), self.getvar(code[3]), \
          self.getvar(code[4]), self.getvar(code[1]), self.getvar(code[5], None), resize, \
          self.getvar(code[7], None), self.getvar(code[8], True))
    elif code[0] == 'mkvmerge': #mkvmerge
      files = []
      for var in code[2:]:
        files = files + [self.getvar(var)]
      autosubsEncode.mergeMkv(self.getvar(code[1]), files)
    elif code[0] == 'systemPAUSE': # systemPAUSE
      while True:
        if raw_input("PAUSADO, escriba 'continuar': ") == 'continuar':
          break


  def ejecuta(self):
    while True:
      self.capitulo = raw_input('Nº del capítulo: ')
      if self.capitulo.isdigit():
        break
    print '\nTIQUETAS:'
    i = 0
    while i < len(self.etiquetas):
      print '  %d- %s' % (i, self.etiquetas[i])
      i += 1
    print 'Escribe el número de las etiquetas a ejecutar separadas por espacios'
    get = raw_input('>> ')
    lista = []
    for e in get.split(' '):
      if e.isdigit():
        if int(e) >= 0 and int(e) < len(self.etiquetas) and int(e) not in lista:
          lista.append(int(e))
    lista.sort()
    for e in lista:
      self.execEtiqueta(self.etiquetas[e])



if __name__ == '__main__':
  f = os.path.join(os.path.abspath(os.getcwd()), FILEPROJECT_NAME)
  if not os.path.isfile(f):
    print >> sys.stderr, "No existe el archivo de proyecto '%s' en el directorio" % FILEPROJECT_NAME
    exit(-2)
  proyecto = Project(f)
  proyecto.ejecuta()




#NOTE Integrar y ejecutar aquí texto de otro archivo
#fp = open(file_to_include)
#exec fp in globals()
#fp.close()


