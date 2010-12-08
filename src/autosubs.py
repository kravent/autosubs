#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import autosubsDownloader
import autosubsTranslate
import autosubsEncode


ALLOWED_CODES=[#TODO reg.exp. para los códigos permitidos en el archivo del proyecto
    'mkDir',
    'waitAndDownload\s+\w+$',
    'extractRAW\s+\w+\s+\w+$',
    'extractASS\s+\w+\s+\w+$',
    'translate\s+\w+\s+\w+$',
    'encode\s+(mp4)|(avi)\s+\w+\s+\w+\s+\d+\s+(\w+)|(\*)\s+(\d+x\d+)|(\*)\s+(\w+)|(\*)\s+(True)|(False)$',
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
  def __str__(self):
    return 'File %s:\n  Line %d: %s' % (filee, nline, line)


class ExecuteError(Error):
  def __init__(self, description):
    self.description = description
  def __str__(self):
    return self.description


class Project:
  def __init__(self, projectFile):
    self.data = {}
    self.code = {}
    etiqueta = None
    f = open(projectFile)
    nline = 0
    for line in f:
      nline += 1
      line = line.strip()
      if re.match('\[\s*\w+\s*\]',line):
        m = re.match('\[\s*(\w+)\s*\]',line).group(1)
        self.code[m] = []
        etiqueta = m
        else:
          print >> sys.stderr, 'ERROR en: "%s"' % line
          print >> sys.stderr, 'La palabra clave \'%s\' no existe' % m
      else:
        if etiqueta:
          self.addCode(etiqueta, projectFile, nline, line)
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
    if isValidCode(line):
      self.code[etiqueta].append(line.split(' '))
    else:
      raise PharseError(filee, nline, line)

  def isValidCode(line):
    for exp in self.ALLOWED_CODES:
      if re.match(exp, line):
        return True
    return False

  def getvar(var, default=''):
    """Si var=='*' o no existe en self.data devuelve default,
    y si no devuelve self.data[var]."""
    if var == '*' or (var != '' and not var in self.data):
      return default
    elif var in self.data:
      return self.data[var]
    else:
      raise ExecuteError('No existe la variable "%s"' % var)

  def savevar(var, data):
    """Guarda data en la variable var de self.data"""
    self.data[var] = data

  def execEtiqueta(etiqueta)
    for code in self.code[etiqueta]:
      execCode(code):

  def execCode(code):
    if code[0] == 'mkDir': # mkDir
      if not self.capitulo in os.listdir('./'):
        os.mkdir(self.capitulo)
    elif code[0] == 'waitAndDownload': # waitAndDownload
      aux = autosubsDownloader.waitfile(getvar('serie'), \
          getvar('fansub'), self.capitulo, \
          getvar('size', None), getvar('patrones', None))
      name = autosubsDownloader.downloadtorrent(aux[1], self.capitulo)
      savevar(code[1], name)
    elif code[0] == 'extractRAW': # extractRAW
      autosubsDownloader.mkv2raw(getvar(code[1]), getvar(code[2]), \
          getvar('fps', None))
    elif code[0] == 'extractASS': # extractASS
      autosubsDownloader.mkv2ass(getvar(code[1]), getvar(code[2]))
    elif code[0] == 'translate': # translate
      autosubsTranslate.asstranslate(getvar(code[1]), getvar(code[2]), \
          getvar('langin', 'en'))
    elif code[0] == 'encode': # encode
      resize =  getvar(code[6], None)
      if resize:
        resize = resize.split('x')
      autosubsEncode.encodeAvidemux(getvar(code[2]), getvar(code[3]), \
          getvar(code[4]), getvar(code[1]), getvar(code[5], None), resize, \
          getvar(code[7], None), getvar(code[8], True))
    elif code[0] == 'mkvmerge': #mkvmerge
      files = []
      for var in code[2:]:
        files = files + [getvar(var)]
      autosubsEncode.mergeMkv(getvar(code[1]), files)
    elif code[0] == 'systemPAUSE': # systemPAUSE
      while True:
        if raw_input("PAUSADO, escriba 'continuar': ") == 'continuar':
          break










#NOTE Integrar y ejecutar aquí texto de otro archivo
#fp = open(file_to_include)
#exec fp in globals()
#fp.close()


