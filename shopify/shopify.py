'''Shopify API client library'''

__author__    = 'Paul Cechner'
__license__   = 'Boost Software License, Version 1.0'
__copyright__ = '2015, Paul Cechner <at cechner.com>'
__version__   = '0.1'

import requests
import urlparse
import pprint
import json

jsonHeaders = { 'content-type': 'application/json' }

class RequestBuilder:

  def __init__(self, baseUrl, apiKey, password, verbose=False):
    r = urlparse.urlparse( baseUrl )
    self.verbose = verbose
    self.apiKey = apiKey
    self.password = password
    self.scheme = r.scheme if r.scheme else 'https'
    self.location = r.netloc if r.netloc else r.path
    if not self.location:
      raise Exception( 'invalid URL' )

  def _debug(self, message):
    if self.verbose:
      print( message )

  def _buildUrl(self, basePath, entityId = ''):
    basePath = basePath.lstrip('/')
    pathSections = [ basePath ] + ( [ entityId ] if entityId else [] )
    path = '/'.join( pathSections ) + '.json'
    url = '{}://{}/{}'.format( self.scheme, self.location, path )
    return url

  def buildGet(self, basePath, entityId = ''):
    url = self._buildUrl( basePath, entityId )
    self._debug( 'GET {}'.format( url ) )
    results = requests.get( url, auth=( self.apiKey, self.password ) )
    self._debug( 'request results: {}'.format( results ) )
    return results

  def buildPost(self, basePath, entity):
    url = self._buildUrl( basePath )
    self._debug( 'POST {}'.format( url ) )
    results = requests.post( url, auth=( self.apiKey, self.password ), headers=jsonHeaders, data=json.dumps( entity ) )
    self._debug( 'request results: {}'.format( results ) )
    return results

  def buildPut(self, basePath, entityId, entity):
    url = self._buildUrl( basePath, entityId )
    self._debug( 'PUT {}'.format( url ) )
    results = requests.put( url, auth=( self.apiKey, self.password ), headers=jsonHeaders, data=json.dumps( entity ) )
    self._debug( 'request results: {}'.format( results ) )
    return results

  def buildDelete(self, basePath, entityId):
    url = self._buildUrl( basePath, entityId )
    self._debug( 'DELETE {}'.format( url ) )
    results = requests.delete( url, auth=( self.apiKey, self.password ) )
    self._debug( 'request results: {}'.format( results ) )
    return results

class Endpoint:
  def __init__(self, requestBuilder, entityName):
    self.requestBuilder = requestBuilder
    self.entityName = entityName
    self.basePath = '/admin/' + entityName

  def get(self, entityId = ''):
    results = self.requestBuilder.buildGet( self.basePath, entityId )
    json = results.json()
    return json[json.keys()[0]]

  def post(self, entity):
    results = self.requestBuilder.buildPost( self.basePath, entity )
    json = results.json()
    return json[json.keys()[0]]

  def put(self, entityId, entity):
    results = self.requestBuilder.buildPut( self.basePath, entityId, entity )
    json = results.json()
    return json[json.keys()[0]]

  def delete(self, entityId):
    results = self.requestBuilder.buildDelete( self.basePath, entityId )
    json = results.json()
    return json[json.keys()[0]]
