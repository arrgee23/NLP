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
        
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        p = urlparse.parse_qs(self.path);
        #print(p);
        if(self.path=="/"):
            self.path="/index.html"
        if(self.path.startswith("/result.html")):
            self.path="/result.html"


        #print(self.raw_requestline)

        #Open the static file requested and send it
        print(curdir + sep + self.path)
        f = open(curdir + sep + self.path) 
        
        self.wfile.write(f.read())
        f.close()

    def do_HEAD(self):
        self._set_headers()
        
    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write("<html><body><h1>POST!</h1></body></html>")
        
def run(server_class=HTTPServer, handler_class=S, port=80):
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