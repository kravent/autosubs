#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import re
import urllib

mu_cstr = None

def muautentification(user, password):
  global mu_cstr
  if not mu_cstr:
    mu_cstr = 'ERMSIMYDAHIQWNQKQYYDR.DJTVAKVXWT'
    #TODO aquí debe autenficarse en el servicio y recoger la cadena de la coockie
  return mu_cstr

def muupload(filepath, description, user=None, password=None):
  print 'Subidendo...',
  sys.stdout.flush()

