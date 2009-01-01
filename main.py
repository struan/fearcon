#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import wsgiref.handlers
import os
from google.appengine.ext import webapp
from google.appengine.ext.webapp import template
from google.appengine.ext import db
from google.appengine.api import users

class UserLevel(db.Model):
  user = db.UserProperty()
  level = db.IntegerProperty()
  
class AverageLevel(db.Model):
  total = db.IntegerProperty()
  count = db.IntegerProperty()

class MainHandler(webapp.RequestHandler):

  def get(self):
    level = UserLevel()
    login = ''
    logout = ''
    
    if users.get_current_user():
      level = UserLevel.get_by_key_name( users.get_current_user().email() )
      if not level:
        level = UserLevel( None, users.get_current_user().email() )
        level.user = users.get_current_user()
        level.level = 3
      logout = users.create_logout_url( '/' )
    else:
      avgs = AverageLevel.all()
      if avgs.count() > 0:
        avg = avgs[0]
        avg_level = int( avg.total / avg.count )
      else:
        avg_level = 3
      level.level = avg_level
      login = users.create_login_url( '/' )
        
    template_values = {
      'levels': [ 5, 4, 3, 2, 1 ],
      'current': level.level,
      'login': login,
      'logout': logout
    }
    path = os.path.join(os.path.dirname(__file__), 'tmpl/index.html')
    self.response.out.write(template.render(path, template_values))

class ChangeLevel(webapp.RequestHandler):
  def post(self):
    if users.get_current_user():
      level = UserLevel.get_by_key_name( users.get_current_user().email() )
      new_level = int( self.request.get('level') )
      avgs = AverageLevel.all()
      
      if avgs.count() > 0:
        avg = avgs[0]
      else:
        avg = AverageLevel()
        avg.total = 0
        avg.count = 0
      
      if not level:
        level = UserLevel( None, users.get_current_user().email() )
        level.user = users.get_current_user()
        avg.count += 1
        avg.total += new_level
      else:
        avg.total -= level.level
        avg.total += new_level
        
      level.level = new_level
      level.put()
      avg.put()
    self.response.out.write('OK')
    

def main():
  application = webapp.WSGIApplication([('/', MainHandler),
                                        ('/update', ChangeLevel)],
                                       debug=True)
  wsgiref.handlers.CGIHandler().run(application)


if __name__ == '__main__':
  main()
