import os
import re
import urllib
from urlparse import urlunparse
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from django.utils import simplejson

from twitter import twitter
from picfall import Picfall
from picfall import TrendEncoder
from picfall import TrendPicsData
from httphelper import HTTPHelper


#globals
twitter = twitter()
picfallHelper = Picfall()
httphelper = HTTPHelper()


class TrendsHandler(webapp.RequestHandler):
  
  def get(self):
    #get trends
    trendsData = twitter.getTrendsData()
    #get the date key of the trends
    #timeKey = trendsData['trends'].keys()[0]
    #get the trends
    #trendsData = trendsData['trends'][timeKey]
    #DONT NEED
    #create a csv list of trend names for use in a js array
    #trendlist = ','.join(["'" + trend['name'] + "'" for trend in trends])
    #parse the trends
    trendCollection = picfallHelper.parseTrendsData(trendsData);
    #json trend names
    #trendsjson = simplejson.JSONEncoder().encode(trendCollection.trends);
    lenbefore = len(trendCollection.trends)
    trendsjson = TrendEncoder().encode(trendCollection.trends);
    lenafter = len(trendCollection.trends)
    
    #trendsHTML = self.getTrendsHTML()
    #setup template
    template_values = {
      'title': "Trending Topics",
      'time': trendCollection.twitterTime,
      'trends': trendCollection.trends,
#      'trendlist': trendlist,
      'trendsjson': trendsjson,
      'lenbefore': lenbefore,
      'lenafter': lenafter,
      'lendata': trendCollection.lendata,
      }

    path = os.path.join(os.path.dirname(__file__), 'trends.html')
    self.response.out.write(template.render(path, template_values))

class SaveTweetsHandler(webapp.RequestHandler):
  
  def get(self):
    #get query
    query = self.request.get('q')
    sinceid = self.request.get('since')
    rpp = 25
    
    #get tweets
    url = picfallHelper.constructPicSearch(query, sinceid, rpp)
    results = twitter.performSearch(url)
    resultsData = twitter.resultsFromJSON(results)
    tweets = picfallHelper.parseResults(resultsData['results'])
    ##just extract the pics
    #from itertools import chain
    #listofpics = [tweet.pics for tweet in tweets]
    #justpics = list(chain(*listofpics))
    
    #setup template
    urlAsHTML = '<a href="' +url + '">' + url + '</a>'
    template_values = {
      'trend': query,
      'tweets': tweets,
    }

    #path = os.path.join(os.path.dirname(__file__), 'justpics.html')
    path = os.path.join(os.path.dirname(__file__), 'pictweets.html')
    self.response.out.write(template.render(path, template_values))


class SaveCurrentTrendsHandler(webapp.RequestHandler):
  def get(self):    
    #get the raw trends
    trendsData = twitter.getTrendsData()
    #parse the trends
    trendCollection = picfallHelper.parseTrendsData(trendsData);
    #save the trends
    trendCollection.save()
    
    self.response.out.write("Trends Saved")
    