import os
from google.appengine.ext import webapp
from google.appengine.ext import db
from google.appengine.ext.webapp import template


class Message(db.Model):
  content = db.StringProperty(multiline=True)
  date = db.DateTimeProperty(auto_now_add=True)


class DSTestHandler(webapp.RequestHandler):
  
  def saveSomeData(sefl):
    for i in range(10):
      #crete new msg
      msg = Message()
      msg.content = "Test Msg " + str(i)
      #save the msg to the data store
      msg.put()

  def get(self):
    
    #save some dummy data
    self.saveSomeData()
    
    #get msgs
    msgs = db.GqlQuery("SELECT * FROM Message ORDER BY date DESC, content DESC")
    
    #setup template
    template_values = {
        'title': "Datasotre Test",
        'msgs': msgs
    }
    
    path = os.path.join(os.path.dirname(__file__), 'dstest.html')
    self.response.out.write(template.render(path, template_values))

