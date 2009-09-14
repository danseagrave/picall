import os
import re
import urllib
from urlparse import urlunparse
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from django.utils import simplejson

from twitter import twitter
from httphelper import HTTPHelper
from picServices import PicServiceCollection

twitter = twitter()
httphelper = HTTPHelper()
picservices = PicServiceCollection()


class Pic:
  url = ''
  id = ''
  pictype = ''
  thumburl = ''
  fullurl = ''
  picservice = None
  
  def __init__(self, url):
    #setup url
    self.url = url
    #get service
    picservice = picservices.getServiceForURL(self.url)
    #get data via service
    self.picType = picservice.name
    self.id = picservice.getPicID(self.url)
    self.thumburl = picservice.thumbnailURL(self.url) 
    self.fullurl = picservice.fullURL(self.url)
    

class Tweet:
  id = ''
  from_user = ''
  user_id = ''
  created_at = ''
  text = ''
  pics = []
  
  def __init__(self, jsonResult):
    self.id = jsonResult['id']
    self.from_user = jsonResult['from_user'].encode('utf-8')
    self.user_id = jsonResult['from_user_id']
    self.created_at = jsonResult['created_at'].encode('utf-8')
    self.text = jsonResult['text'].encode('utf-8')
    self.pics = self.extractPicData(self.text)
  
  def extractPicData(self, text):
    #get all urls
    allurls = httphelper.extractURLs(text)
    #filter put all non pic urls and collect them into 
    picdata = [
                Pic(url)
                for url in allurls 
                if picservices.isPicURL(url)
                ]
    #done
    return picdata

class Trend(db.Model):
  name = db.StringProperty()
  position = db.IntegerProperty()
  twitterTime = db.StringProperty()
  dateAdded = db.DateTimeProperty(auto_now_add=True)
   
class SimpleTrend():
  name = ''
  position = 0
  twitterTime = ''
  
  def save(self):
    #setup 
    dbTrend = Trend()
    dbTrend.name = self.name
    dbTrend.position = self.position
    dbTrend.twitterTime = self.twitterTime
    #save
    dbTrend.put()

class TrendCollection():
  twitterTime = None
  trends = None
  
  def __init__(self):
    self.trends = []
  
  def append(self, trend):
    self.trends.append(trend)
  
  def saveAll(self):
    #save all trends in the trend collection...
    x = 1

class TrendPicsData:
  requestedat = None
  trends = None
  
  def __init__(self,):
    #set request time
    requestedat = now()
    #get tweets
    url = flitter.constructPicSearch(query)
    results = twitter.performSearch(url)
    resultsData = twitter.resultsFromJSON(results)
    tweets = flitter.parseResults(resultsData['results'])
    
    return tweets

class TrendEncoder(simplejson.JSONEncoder):
  def default(self, trend):
    # Convert objects to a dictionary of their representation
    d = { 'name': trend.name, 
            'position': trend.position,
          }
    #d.update(trend.__dict__)
    return d

class Picfall:
  
  def constructPicSearch(self, query, sinceid, rpp):
    
    orParam = "&ors=" + '%20'.join(picservices.basePicURLs)
    
    sinceParam = ''
    if len(sinceid) > 0:
      sinceParam = "&since_id=" + sinceid
    
    
    return twitter.constructSearchURL(query, rpp) + orParam + sinceParam
     
  def parseResults(self, results):
    tweets = []    
    for jsonTweet in results:
      tweets.append(
        #{
        #  'from_user': tweet['from_user'],
        #  'text': tweet['text'],
        #  'time': tweet['created_at'],
        #  'pics': self.extractPicData(tweet['text']),
        #}
        Tweet(jsonTweet)
        )
    
    return tweets
    
  def parseTrendsData(self, trendsData, saveToStore=False):
    
    #setup default return val
    trends = TrendCollection()
    
    #get the date key of the trends
    timeKey = trendsData['trends'].keys()[0]
    
    #set date in retrun
    trends.twitterTime = timeKey
    
    trends.lendata = len(trendsData['trends'][timeKey])
    
    #collect all the trends
    position = 1
    for trendData in trendsData['trends'][timeKey]:
      #create new trend
      trend = SimpleTrend()
      # - add a position number
      trend.position = position;
      # - corrrectly encode the name
      trend.name = trendData['name'].encode('utf-8');
      # - set the twittertime
      trend.twitterTime = timeKey 
      #add the trend to the result set
      trends.append(trend)
      #inc the position counter
      position = position + 1;
      #Save if askded to
      if saveToStore:
        trend.put();
    
    
    return trends
  
  def addHTMLIDsToTrends(self, trends):
    for trend in trends.trends:
      trend.id = 'trend-' + str(trend.position)
    
    return trends
    
  def getPicService(self, url):    
    return picservices.getServiceForURL(url)
  
  def getPicTweets(self, query):
    url = self.constructPicSearch(query)
    results = twitter.performSearch(url)
    resultsData = twitter.resultsFromJSON(results)
    tweets = self.parseResults(resultsData['results'])
    
    return tweets
  
  def AddTweetsToTrends(self, trends):    
    for trend in trends:
      trend['pics'] = self.getPicTweets(trend['name'])
    return trends
    