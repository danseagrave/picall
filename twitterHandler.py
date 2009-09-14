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

defaultNumTweets = 5


class SearchHandler(webapp.RequestHandler):
  
  basePicURLs = ["yfrog.com", "twitpic.com"]  
  picURLMatcher = re.compile("^http://("+"|".join(basePicURLs)+")")
  
  def get(self):
    #get query
    query = self.request.get('q')
    sinceid = self.request.get('since')
    
    numTweets = defaultNumTweets
    
    #get tweets
    url = picfallHelper.constructPicSearch(query, sinceid, numTweets)
    results = twitter.performSearch(url)
    resultsData = twitter.resultsFromJSON(results)
    tweets = picfallHelper.parseResults(resultsData['results'])
    
    #setup template
    urlAsHTML = '<a href="' +url + '">' + url + '</a>'
    template_values = {
        'title': "Twitter Search",
        #'tweets': resultsData['results'],
        'tweets': tweets,
        'query': query,
        'searchType': "pics",
        'searchTechData': [
          {'name': 'url', 'data': urlAsHTML},
          {'name': 'json', 'data': results},
          ],
    }
    
    path = os.path.join(os.path.dirname(__file__), 'search.html')
    self.response.out.write(template.render(path, template_values))
  

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

class JustPicsHandler(webapp.RequestHandler):
  
  def get(self):
    #get query
    query = self.request.get('q')
    sinceid = self.request.get('since')
    
    numTweets = defaultNumTweets
    
    #get tweets
    url = picfallHelper.constructPicSearch(query, sinceid, numTweets)
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


class JustTrendsHandler(webapp.RequestHandler):
  def get(self):    
    #json encode
    jsonTrends = twitter.getTrendsJSON()
    self.response.out.write(jsonTrends)
    
    trendsData = twitter.getTrendsData()
    #get the date key of the trends
    timeKey = trendsData['trends'].keys()[0]
    trends = trendsData['trends'][timeKey]
    self.response.out.write("<ol>")
    import urllib
    for trend in trends:
        self.response.out.write("<li>" + trend['name'] + " - url encoded: " + urllib.quote_plus(trend['name'].encode('utf-8')) + "</li>")
    self.response.out.write("</ol>")
    
    
    
class TrendTweetsHandler(webapp.RequestHandler):
  def get(self):
    #get query
    query = self.request.get('q')
    sinceid = self.request.get('since')
    
    #get tweets
    tweets = TrendPicsData(query, sinceid)
    
    #json encode
    jsonTweets = None
    
    #resonse
    self.response.out.write(jsonTweets)