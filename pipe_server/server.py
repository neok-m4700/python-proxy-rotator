#!/usr/bin/env python
from http.server import HTTPServer, BaseHTTPRequestHandler
from socketserver import ThreadingMixIn
from .handler import ProxiedRequestHandler
from proxy.proxier import ProxyManager
from .ca_generator import CertificateAuthority

class PipeServer(HTTPServer):
    def __init__(self, server_address=('', 8080), try_local_proxylist=True, chainlength=0, DEBUG=False):
        HTTPServer.__init__(self, 
                        server_address, 
                        ProxiedRequestHandler,
                    )
        self.ca = CertificateAuthority()
        self.proxy_fetcher = ProxyManager(try_local_proxylist)
        self.CHAIN = chainlength
        self.DEBUG = DEBUG


class ThreadedPipeServer(ThreadingMixIn, PipeServer):
    def stop_proxy(self):
        self.proxy_fetcher.terminate()
    
    def terminate(self):
        self.stop_proxy() # stop loading proxies
        self.socket.close()
    
    def setchainlength(self,length):
        self.CHAIN = length