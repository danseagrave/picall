import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template

from picfall import Picfall

#globals
picfallHelper = Picfall()



class ShowLatestTrendsHandler(webapp.RequestHandler):
  def get(self):    
    
    #fetch latest trends
    trends {'name': 'NOTHING TO SEE HERE'}
    
    import urllib
    for trend in trends:
        self.response.out.write("<li>" + trend['name'] + " - url encoded: " + urllib.quote_plus(trend['name'].encode('utf-8')) + "</li>")
    self.response.out.write("</ol>")
    