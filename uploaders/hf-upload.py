###############################################################################
## Tucan Project
##
## Copyright (C) 2008-2010 Fran Lupion crak@tucaneando.com
##                         Elie Melois eliemelois@gmail.com
##
## This program is free software; you can redistribute it and/or modify
## it under the terms of the GNU General Public License as published by
## the Free Software Foundation; either version 3 of the License, or
## (at your option) any later version.
##
## This program is distributed in the hope that it will be useful,
## but WITHOUT ANY WARRANTY; without even the implied warranty of
## MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
## GNU General Public License for more details.
##
## You should have received a copy of the GNU General Public License
## along with this program; if not, write to the Free Software
## Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
###############################################################################

import urllib
import urllib2
import cookielib

from poster.encode import multipart_encode
from poster.streaminghttp import register_openers

HEADER = {"User-Agent":"Mozilla/5.0 (X11; U; Linux i686) Gecko/20081114 Firefox/3.0.4"}

class UploadParser():
        """"""
        def __init__(self, file_name, description):
                """"""
                up_done_action = None
                file_id = None
                url = None

                opener = register_openers()
                cookie = cookielib.CookieJar()
                opener.add_handler(urllib2.HTTPCookieProcessor(cookie))

                it = opener.open(urllib2.Request("http://www.hotfile.com/",{},HEADER))
                for line in it:
                        if 'multipart/form-data' in line:
                                up_done_action = line.split('action="')[1].split('"')[0]
                if up_done_action:
                        print up_done_action

                        form = {"uploads[]": open(file_name, "rb")}

                        datagen, headers = multipart_encode(form,None,self.progress)
                        headers = dict(headers.items() + HEADER.items())
                        result = opener.open(urllib2.Request(up_done_action, datagen, headers))

                        for line in result:
                                if 'name="url"' in line:
                                        url = line.split('value="')[1].split('"')[0]
                                        print url

        def progress(self,se,current,total):
                print "%d : %d" % (current,total)

if __name__ == "__main__":
        c = UploadParser("/home/elie/upload.png", "mierda")
