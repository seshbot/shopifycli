#!/usr/bin/env python
'''Shopify command line client'''

__author__    = 'Paul Cechner'
__license__   = 'Boost Software License, Version 1.0'
__copyright__ = '2015, Paul Cechner <at cechner.com>'
__version__   = '0.1'

import requests
import urlparse
import pprint

class RequestBuilder:
  def __init__(self, baseUrl, apiKey, password):
    r = urlparse.urlparse( baseUrl )
    self.apiKey = apiKey
    self.password = password
    self.scheme = r.scheme if r.scheme else 'https'
    self.location = r.netloc if r.netloc else r.path
    if not self.location:
      raise Exception( 'invalid URL' )

  def buildUrl(self, basePath, entityId = ''):
      basePath = basePath.lstrip('/')
      pathSections = [ basePath ] + ( [ entityId ] if entityId else [] )
      path = '/'.join( pathSections ) + '.json'
      url = '{}://{}/{}'.format( self.scheme, self.location, path )
      return url

  def buildGet(self, basePath, entityId = ''):
      url = self.buildUrl( basePath, entityId )
      print( 'requesting URL {}'.format( url ) )
      return requests.get( url, auth=( self.apiKey, self.password ) )

class Endpoint:
  def __init__(self, requestBuilder, entityName):
    self.requestBuilder = requestBuilder
    self.entityName = entityName
    self.basePath = '/admin/' + entityName

  def get(self, entityId = ''):
    results = self.requestBuilder.buildGet( self.basePath, entityId )
    print( 'request results: {}'.format( results ) )
    json = results.json()
    return json[json.keys()[0]]

if __name__ == '__main__':
  import argparse
  import os

  parser = argparse.ArgumentParser()
  parser.add_argument('-a', '--address', default='', help='store address (default: SHOPIFY_ADDRESS)')
  parser.add_argument('-k', '--apiKey', default='', help='store API key (default: SHOPIFY_APIKEY)')
  parser.add_argument('-p', '--password', default='', help='store API password (default: SHOPIFY_PASSWORD)')
  parser.add_argument('-j', '--json', action='store_true', help='output in JSON format')
  parser.add_argument('command', choices=['get', 'post'])
  parser.add_argument('entity', choices=['orders', 'products', 'customers', 'carrier_services'])
  parser.add_argument('entityIds', nargs='*')

  args = parser.parse_args()

  command = args.command
  entity = args.entity
  entityIds = args.entityIds if len( args.entityIds ) > 0 else ['']

  address = args.address if args.address else os.environ['SHOPIFY_ADDRESS']
  apiKey = args.apiKey if args.apiKey else os.environ['SHOPIFY_APIKEY']
  password = args.password if args.password else os.environ['SHOPIFY_PASSWORD']

  requestBuilder = RequestBuilder( address, apiKey, password )
  endPoint = Endpoint( requestBuilder, entity )

  for entityId in entityIds:
    pprint.pprint( endPoint.get( entityId ) )
