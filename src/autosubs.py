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

  def execEtiqueta(etiqueta)
    for code in self.code[etiqueta]:
      if code[0] == 'mkDir':
        if not self.capitulo in os.listdir('./'):
          os.mkdir(self.capitulo)
      elif code[0] == 'waitAndDownload':
        if 'size' in self.data:
          size = self.data['size']
        else:
          size = None
        if 'patrones' in self.data:
          patrones = self.data['patrones'].split('%%%')
        else:
          patrones = None
        var = autosubsDownloader.waitfile(self.data['serie'], \
            self.data['fansub'], self.capitulo, size, patrones)
        name = autosubsDownloader.downloadtorrent(var[1], self.capitulo)
        self.data[code[1]] = name
      elif XXXXXXXXXXXXXXXXXXX:








#NOTE Integrar y ejecutar aquí texto de otro archivo
#fp = open(file_to_include)
#exec fp in globals()
#fp.close()


