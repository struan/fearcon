#!/usr/bin/env python

import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from fearcon.db import *

class MainHandler(webapp.RequestHandler):
  def __init__(self):
    self.global_only = False

  def get(self):
    level = UserLevel()
    login = ''
    logout = ''
    
    if users.get_current_user() and not self.global_only:
      level = UserLevel.get_by_key_name( users.get_current_user().email() )
      if not level:
        level = UserLevel( None, users.get_current_user().email() )
        level.user = users.get_current_user()
        level.nick = level.user.nickname()
        level.level = 3
      logout = users.create_logout_url( '/' )
      title = 'fearcon : ' + level.user.nickname()
    else:
      avgs = AverageLevel.all()
      if avgs.count() > 0:
        avg = avgs[0]
        avg_level = int( avg.total / avg.count )
      else:
        avg_level = 3
      level.level = avg_level
      if users.get_current_user():
        logout = users.create_logout_url( '/' )
      else:
        login = users.create_login_url( '/' )
      title = 'fearcon : global'
        
    template_values = {
      'levels': [ 5, 4, 3, 2, 1 ],
      'current': level.level,
      'title': title,
      'login': login,
      'logout': logout
    }
    
    if self.global_only:
      template_values[ 'home' ] = '/'
      template_values[ 'noglobal' ] = 1
      
    path = os.path.join(os.path.dirname(__file__), 'tmpl/index.html')
    self.response.out.write(template.render(path, template_values))

class GlobalHandler(MainHandler):
  def __init__(self):
    self.global_only = True

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/global/', GlobalHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
