#!/usr/bin/env python
'''Shopify command line client'''

__author__    = 'Paul Cechner'
__license__   = 'Boost Software License, Version 1.0'
__copyright__ = '2015, Paul Cechner <at cechner.com>'
__version__   = '0.1'

from shopify import Shopify
import pprint
import json

if __name__ == '__main__':
  import argparse
  import os

  parser = argparse.ArgumentParser()
  parser.add_argument('-a', '--address', default='', help='store address (default: SHOPIFY_ADDRESS)')
  parser.add_argument('-k', '--apiKey', default='', help='store API key (default: SHOPIFY_APIKEY)')
  parser.add_argument('-p', '--password', default='', help='store API password (default: SHOPIFY_PASSWORD)')
  parser.add_argument('-v', '--verbose', action='store_true', help='verbose output (requests and responses)')
  parser.add_argument('-j', '--json', action='store_true', help='output in JSON format')
  parser.add_argument('-f', '--file', help='input file in JSON format (for POST, PUT)')
  parser.add_argument('--pretty-print', action='store_true', help='print JSON output nicely')
  parser.add_argument('command', choices=['get', 'post', 'put', 'delete'])
  parser.add_argument('entity', choices=['orders', 'products', 'customers', 'carrier_services'])
  parser.add_argument('entityIds', nargs='*')

  args = parser.parse_args()

  verbose = args.verbose
  prettyPrint = args.pretty_print

  command = args.command
  entity = args.entity
  entityIds = args.entityIds if len( args.entityIds ) > 0 else ['']

  address = args.address if args.address else os.environ['SHOPIFY_ADDRESS']
  apiKey = args.apiKey if args.apiKey else os.environ['SHOPIFY_APIKEY']
  password = args.password if args.password else os.environ['SHOPIFY_PASSWORD']

  requestBuilder = Shopify.RequestBuilder( address, apiKey, password, verbose )
  endPoint = Shopify.Endpoint( requestBuilder, entity )

  def output(entity):
    if prettyPrint:
      pprint.pprint( entity )
    else:
      print json.dumps( entity )

  if command.upper() == 'GET':
    for entityId in entityIds:
      output( endPoint.get( entityId ) )

  if command.upper() == 'POST':
    filename = args.file
    file = open( filename, 'r' )
    output( endPoint.post( json.loads( file.read() ) ) )
    file.close()

  if command.upper() == 'PUT':
    entityId = entityIds[0]
    filename = args.file
    file = open( filename, 'r' )
    output( endPoint.put( entityId, json.loads( file.read() ) ) )
    file.close()

  if command.upper() == 'DELETE':
    for entityId in entityIds:
      output( endPoint.delete( entityId ) )
