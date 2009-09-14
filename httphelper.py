import os
import re
import urllib
from urlparse import urlunparse
from google.appengine.api import urlfetch
from django.utils import simplejson

class HTTPHelper:
  
  def extractURLs(self, text):
    found = []
    URLfinder = re.compile("([0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}\\.[0-9]{1,3}|(((news|telnet|nttp|file|http|ftp|https)://)|(www|ftp)[-A-Za-z0-9]*\\.)[-A-Za-z0-9\\.]+)(:[0-9]*)?/[-A-Za-z0-9_\\$\\.\\+\\!\\*\\(\\),;:@&=\\?/~\\#\\%]*[^]'\\.}>\\),\\\"]")
    
    for match in URLfinder.finditer(text):
      found.append(match.group(0))
    
    return found
