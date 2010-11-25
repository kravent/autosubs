import socket
import re
import md5
import sys

# Rapidshare Uploader v 1.1 by Adam Poit
#
# Type these commands from the command line to use this script:
#
# python rsupload.py myfile.rar free (Uploads to rapidshare as a free user)
# python rsupload.py myfile.rar col Username Password (Uploads to a rapidshare collectors account)
# python rsupload.py myfile.rar prem Username Password (Uploads to a premium account)
#
# To upload multiple files, separate them with a # (number sign). Like this:
#
# python rsupload.py myfile.rar#anotherfile.rar#onemore.rar prem Username Password
#
# At the end, RSUploader will save all the urls to rsurls.txt

class RSUploader:
    def __init__(self, filename):
        self.filename = filename
        self.bufferlen = 0

    def upload(self):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("rapidshare.com", 80))

        sock.send('GET /cgi-bin/rsapi.cgi?sub=nextuploadserver_v1 HTTP/1.0\r\n\r\n')
        uploadserver = re.search('\r\n\r\n(\d+)', sock.recv(1000000000))
        uploadserver = uploadserver.group().lstrip()
        sock.close()

        f = open(self.filename)
        filecontent = f.read()
        size = len(filecontent)
        md5hash = md5.new(filecontent)
        f.close()

        print "MD5: " + md5hash.hexdigest().upper()
        print "Uploading to rs" + uploadserver + "l3.rapidshare.com...\n"

        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect(("rs" + uploadserver + "l3.rapidshare.com", 80))

        boundary = "---------------------632865735RS4EVER5675865"
        contentheader = boundary + "\r\nContent-Disposition: form-data; name=\"rsapi_v1\"\r\n\r\n1\r\n"

        if type == "prem":
            contentheader += boundary + "\r\nContent-Disposition: form-data; name=\"login\"\r\n\r\n" + username + "\r\n"
            contentheader += boundary + "\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n" + password + "\r\n"

        if type == "col":
            contentheader += boundary + "\r\nContent-Disposition: form-data; name=\"freeaccountid\"\r\n\r\n" + username + "\r\n"
            contentheader += boundary + "\r\nContent-Disposition: form-data; name=\"password\"\r\n\r\n" + password + "\r\n"

        contentheader += boundary + "\r\nContent-Disposition: form-data; name=\"filecontent\"; filename=\"" + self.filename + "\"\r\n\r\n"
        contenttail = "\r\n" + boundary + "--\r\n"
        contentlength = len(contentheader) + size + len(contenttail)

        header = "POST /cgi-bin/upload.cgi HTTP/1.0\r\nContent-Type: multipart/form-data; boundary=" + boundary + "\r\nContent-Length: " + str(contentlength) + "\r\n\r\n" + contentheader

        sock.send(header)

        f = open(self.filename)

        while True:
            chunk = f.read(64000)
            if not chunk:
	        break
            sock.send(chunk)
            self.bufferlen += len(chunk)
            pere = float(self.bufferlen) / float(size) * 100
            rnd = round(pere, 1)
            print "Sent " + str(self.bufferlen) + " of " + str(size) + " bytes / " + str(rnd) + "%"

        sock.send(contenttail)

        result = sock.recv(1000000000)
        f.close()
        sock.close()

        print "\nChecking MD5..."

        newhash = re.search('File1.4=(\w+)', result)
        oldhash = "File1.4=" + md5hash.hexdigest().upper()
        if newhash.group() == oldhash:
            upload = re.search('File1.1=(\S+)', result)
            print "File uploaded successfully: " + upload.group() + "\n\n"
            f = open("rsurls.txt", "a")
            f.write(upload.group() + "\n")
            f.close()
        else:
            print "Upload Failure\n"

#Start Program
print "Rapidshare Uploader v 1.1 by Thearium\n"

filename = sys.argv[1]
type = sys.argv[2]
if type != "free":
    username = sys.argv[3]
    password = sys.argv[4]

files = filename.split('#')

for file in files:
    rs = RSUploader(file)
    rs.upload()
