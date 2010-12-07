#!/usr/bin/env python
# -*- coding: utf-8 -*-
import sys, os
import subprocess

PATH = os.path.abspath(os.path.join(os.path.dirname(sys.argv[0]))) 
TEMPLATE_MP4HD = os.path.join(PATH,'data','template-mp4hd.js')
TEMPLATE_AVI = os.path.join(PATH,'data','template-avi.js')


def makeAvidemuxScript(scriptout, videofile, exitsize, extension, \
    assfile=None, resize=None, fps1000=None):
  if extension == 'avi':
    template = TEMPLATE_AVI
  else:
    template = TEMPLATE_MP4HD
  f = open(template)
  data = f.read()
  f.close()
  data = data.replace('%VIDEO_FILE%', os.path.abspath(videofile))
  data = data.replace('%EXIT_SIZE%', exitsize)
  if assfile:
    data = data.replace('%ASS%', \
        'app.video.addFilter("ass","font_scale=1,000000","line_spacing=0,100000","top_margin=0","bottom_margin=0","subfile=%s","fonts_dir=/tmp/","extract_embedded_fonts=1");' % os.path.abspath(assfile))
  else:
    data = data.replace('%ASS%', '')
  if resize:
    data = data.replace('%RESIZE%', \
        'app.video.addFilter("resize","w=%s","h=%s","algo=0");' % (resize[0],resize[1]))
  else:
    data = data.replace('%RESIZE%', '')
  if fps1000:
    data = data.replace('%FPS%', 'app.video.fps1000 = %s;' % fps1000)
  else:
    data = data.replace('%FPS%', '')
  f = open(scriptout,'w')
  f.write(data)
  f.close()


def encodeAvidemuxScript(scriptfile, videofile, securex264=True):
  """
  videofile = Archivo donde guardar el resultado
  """
  cmd = 'avidemux2_cli'
  if securex264:
    cmd = cmd + ' --force-alt-h264'
  else:
    cmd = cmd + ' --autoindex' #TODO forzar a no usar el modo alternativo
  cmd = cmd + " --run '%s' --save '%s'" % (scriptfile, videofile)
  process = subprocess.Popen(cmd, shell=True)
  process.wait()
  #process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
  #line = process.stdout.readline()
  #while line:
  #  print line,
  #  sys.stdout.flush()
  #  line = process.stdout.readline()



def encodeAvidemux(videoOut, videoIn, exitsize, extension, \
    assfile=None, resize=None, fps1000=None, securex264=True):
  makeAvidemuxScript(videoOut+'.ps', videoIn, exitsize, extension, \
    assfile, resize, fps1000)
  encodeAvidemuxScript(videoOut+'.ps', videoOut, securex264)


def mergeMkv(mkvfile, files):
  """
  mkvfile = output mkv file
  files = [] #Array width files
  """
  cmd = "mkvmerge -v -o '%s'" % mkvfile
  for f in files:
    cmd = cmd + " '%s'" % f
  process = subprocess.Popen(cmd, shell=True)
  process.wait()
  #process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
  #line = process.stdout.readline()
  #while line:
  #  print line,
  #  sys.stdout.flush()
  #  line = process.stdout.readline()


if __name__ == '__main__':
  if len(sys.argv)<5:
    print 'USO: autosubs-encode type video_in video_out size_out [ass] [fps1000]'
    print 'type = mkv|mp4|avi'
    print 'para type=mkv no se tendrá en cuenta el valor de size_out'
    exit(-1)
  if sys.argv[1] == 'mkv':
    if len(sys.argv)>5:
      mergeMkv(sys.argv[3],[sys.argv[2],sys.argv[5]])
    else:
      mergeMkv(sys.argv[3],[sys.argv[2]])
  elif sys.argv[1] == 'mp4' or sys.argv[1] == 'avi':
    if len(sys.argv) > 5:
      ass = sys.argv[5]
    else:
      ass = None
    if len(sys.argv) < 6:
      fps1000 = sys.argv[6]
    else:
      fps1000 = None
    makeAvidemuxScript(sys.argv[3]+'.js', sys.argv[2], sys.argv[4], \
        sys.argv[1], ass, None, fps1000)
    encodeAvidemuxScript(sys.argv[3]+'.js', sys.argv[3])
  else:
    print 'ERROR: el tipo debe ser mkv|mp4|avi'
    exit(-2)




