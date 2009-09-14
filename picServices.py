import os
import re

"""
    Each pic sservice will implement
    .name
    .thumbnailURL(url)
    .fullURL(url)
    .getPicID(url)
    .isThisType(url)
"""


class Twitpic:
    name = "twitpic.com"
    
    def thumbnailURL(self, url):
      picid = self.getPicID(url)
      url = "http://" + self.name + "/show/thumb/" + picid + ".jpg"
      
      return url
    
    def fullURL(self, url):
      picid = self.getPicID(url)
      url = "http://" + self.name + "/show/full/" + picid + ".jpg"
      
      return url
    
    def getPicID(self, url):
      #regex to match the ID part - first group should be the id
      match = re.match("^http://" + self.name +"/(\w*)", url)
      
      #if there is a match return the first group
      if match:
        return match.group(1)
        
      #no match - return false
      return False
    
    def isThisType(self, url):
      return re.match("^http://" + self.name, url)

class Yfrog:
    name = "yfrog.com"
    
    def thumbnailURL(self, url):
      picid = self.getPicID(url)
      url = "http://" + self.name + "/" + picid + ".th.jpg"
      
      return url
    
    def fullURL(self, url):
      picid = self.getPicID(url)
      #using the iPhone version because otherwise we have to 
      #fetch and parse some xml from yfrog to get the propper full image url
      #TODO: parse the XML data from http://yfrog.com/api/xmlinfo?path=[picid]
      url = "http://" + self.name + "/" + picid + ":iphone"
      
      return url
    
    def getPicID(self, url):
      #regex to match the ID part - first group should be the id
      match = re.match("^http://" + self.name +"/(\w*)", url)
      
      #if there is a match return the first group
      if match:
        return match.group(1)
        
      #no match - return false
      return False
    
    def isThisType(self, url):
      return re.match("^http://" + self.name, url)

"""
now we need a collection to hold them...
"""
class PicServiceCollection:
    
    basePicURLs = ["yfrog.com", "twitpic.com"]  
    picURLMatcher = re.compile("^http://("+"|".join(basePicURLs)+")")
    
    services = {
      'twitpic.com': Twitpic(),
      'yfrog.com': Yfrog(),
      }
    
    def names(self):
        return self.services.keys()
    
    def getServiceForURL(self, url):
        """
        itterate over all services - calling isThisType(url)
        - return service if found
        - return false if not
        """
        
        for (name, service) in self.services.iteritems():
          if service.isThisType(url):
            return service
        
        #if we got this far then we have no service for that url
        return False
    
    def getService(self, name):
      """
      do we have a service for this name?
       - if yes - return the service
       - if not return false
      """
      if serviceExists(name):
        return self.services[name]
      
      return False
    
    def serviceExists(name):
      return name in self.services
    
    def isPicURL(self, url):
        #todo ##REPLACE THIS WITH CALLS TO getServiceForURL()##
        #return true if it is a pic url
        if self.picURLMatcher.match(url):
            return True
            
        return False
