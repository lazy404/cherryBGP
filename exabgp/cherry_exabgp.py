#!/usr/bin/env python
from SimpleXMLRPCServer import SimpleXMLRPCServer
import xmlrpclib, sys
from fcntl import fcntl, F_GETFL, F_SETFL
from os import O_NONBLOCK, read


def stdin_read():
    return read(sys.stdin.fileno(), 4096)

def write(buf):
    sys.stdout.write(buf)
    sys.stdout.flush()
    return True

flags = fcntl(sys.stdin, F_GETFL)
fcntl(sys.stdin, F_SETFL, flags | O_NONBLOCK)

server = SimpleXMLRPCServer(("0.0.0.0", 8000),logRequests=False)
server.register_function(stdin_read, 'read')
server.register_function(write, 'write')

server.serve_forever()
