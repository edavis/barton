#!/usr/bin/env python

from SimpleXMLRPCServer import SimpleXMLRPCServer
from metaweblog import MetaWeblog

def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', default='localhost')
    parser.add_argument('-p', '--port', default=9005, type=int)
    args = parser.parse_args()

    print("Running MetaWeblog Server: http://%s:%s/" % (args.host, args.port))
    server = SimpleXMLRPCServer((args.host, args.port))
    server.register_instance(MetaWeblog())
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("")

