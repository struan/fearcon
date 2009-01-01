#!/usr/bin/env python

import wsgiref.handlers
import os
from urllib import unquote
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.api import users
from fearcon.db import *

class MainHandler(webapp.RequestHandler):

  def get(self):
    level = None
    login = ''
    logout = ''
    msg = ''
    tmpl = 'tmpl/index.html'
    
    if users.get_current_user():
      logout = users.create_logout_url( self.request.path )
    else:
      login = users.create_login_url( self.request.path )
    
    nickname = self.request.path
    nickname = nickname.replace( '/user/', '' )
    nickname = unquote( nickname )
      
    levels = UserLevel.gql( 'WHERE nick = :1', nickname )
    if levels.count() > 0:
      level = levels[0]
      
    if not level:
      msg = "ruh roh: no such user - " + nickname
      title = 'fearcon'
      tmpl = 'tmpl/error.html'
    else:
      title = 'fearcon : ' + level.user.nickname()
        
    template_values = {
      'levels': [ 5, 4, 3, 2, 1 ],
      'title': title,
      'msg': msg,
      'login': login,
      'logout': logout
    }
    
    if level:
      template_values[ 'current' ] = level.level
      
    path = os.path.join(os.path.dirname(__file__), tmpl )
    self.response.out.write(template.render(path, template_values))



def main():
  application = webapp.WSGIApplication([('/user/.*', MainHandler)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
