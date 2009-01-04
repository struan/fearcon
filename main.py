#!/usr/bin/env python

import wsgiref.handlers
import os
from urllib import quote_plus
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
    user = ''
    is_new_user = 0
    
    if users.get_current_user() and not self.global_only:
      level = UserLevel.get_by_key_name( users.get_current_user().email() )
      if not level:
        is_new_user = 1
        level = UserLevel( None, users.get_current_user().email() )
        level.user = users.get_current_user()
        level.nick = level.user.nickname()
        level.level = 3
      logout = users.create_logout_url( '/' )
      title = 'fearcon : ' + level.user.nickname()
      user = '/user/' + quote_plus( level.user.nickname() )
    else:
      avgs = AverageLevel.all()
      if avgs.count() > 0:
        avg = avgs[0]
        avg_level = int( avg.total / avg.count )
      else:
        avg_level = 3
      level.level = avg_level
      if users.get_current_user():
        user = '/user/' + quote_plus( users.get_current_user().nickname() )
        logout = users.create_logout_url( '/' )
      else:
        login = users.create_login_url( '/' )
      title = 'fearcon : global'
        
    template_values = {
      'levels': [ 5, 4, 3, 2, 1 ],
      'current': level.level,
      'is_new_user': is_new_user,
      'user': user,
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
    
class AboutHandler(webapp.RequestHandler):
  def get(self):
    template_values = {
      'home': '/',
      'noglobal': 1,
      'noabout': 1
    }
    path = os.path.join(os.path.dirname(__file__), 'tmpl/about.html')
    self.response.out.write(template.render(path, template_values))

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/global/', GlobalHandler),
                                        ('/about/', AboutHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
