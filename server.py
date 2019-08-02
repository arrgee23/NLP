#!/usr/bin/env python2
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
from os import curdir, sep
import cgi
from urllib2 import urlparse
#import SocketServer

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.send_header('charset','utf-8')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        outputStr = '<table style="width:50%"><tr><th>Character</th><th>Count</th></tr>'
        isFIleOutput = 0
        newpath = self.path
        if(self.path=="/"):
            isFIleOutput = 1
            newpath="/index.html"
            
        if(self.path.startswith("/result.html")):
            isFIleOutput = 0
            p = urlparse.parse_qs(self.path)
            extractedStr = p['/result.html?taName'][0]
            #print("parsedResult: \n]")
            print("decoded")
            #newpath="/result.html"
            #decoded = (extractedStr.decoded('utf-8'))
            decoded = extractedStr.decode('utf8')
            print(decoded)
            d = {}
            for char in decoded:
                d[char] = 0
            
            for c in decoded:
                d[c] = d[c]+1
            
            
            print("_________")
            print(d)

            
            for elem in d.keys():
                outputStr = outputStr +"<tr>" + "<td>"+elem.encode('utf-8') +"</td>"+ "<td>"+str(d[elem])+"<td>" +"<tr>"
            



        #print(self.raw_requestline)

        #Open the static file requested and send it
        if (isFIleOutput == 1):
            print("constructed url")
            print(curdir + sep + newpath)
            f = open(curdir + sep +newpath) 
            self.wfile.write(f.read())
            f.close()
        else:
            self.wfile.write(outputStr)

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        post_data = self.rfile.read(content_length) # <--- Gets the data itself
        print("post data")
        print(post_data)
        self._set_headers()
        self.wfile.write(post_data)
        
        
def run(server_class=HTTPServer, handler_class=S, port=1835):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    
    print ('Starting httpd...')
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv
    
    if len(argv) == 2:
        run(port=int(argv[1]))
    else:
        run()
