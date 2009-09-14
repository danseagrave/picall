import os
import re
import urllib
from urlparse import urlunparse
from google.appengine.api import urlfetch
from django.utils import simplejson

class twitter():
   
  def baseSearchURL(self):
    return 'http://search.twitter.com/search.json?page=1'
  
  def constructSearchURL(self, query, rpp=5):
    return self.baseSearchURL() + '&rpp=' + str(rpp) +'&q='+ urllib.quote_plus(query)
  
  def performSearch(self, url):
    result = urlfetch.fetch(url)
    if result.status_code == 200:
      return result.content
    
  def resultsFromJSON(self, results):
    #convert json results to dicts
    return simplejson.loads(results)

  def getTrendsJSON(self):
    #url = "http://search.twitter.com/trends/current.json?exclude=hashtags"
    url = "http://search.twitter.com/trends/current.json"

    result = urlfetch.fetch(url)
    if result.status_code == 200:
      return result.content
  
  def getTrendsData(self):
    #load the trends
    trendsJSON = self.getTrendsJSON()
    #convert to dicts
    trendsData = simplejson.loads(trendsJSON)
    
    #finished
    return trendsData
    
    
