from google.appengine.ext import db

class UserLevel(db.Model):
  user = db.UserProperty()
  level = db.IntegerProperty()
  nick = db.StringProperty()
  
class AverageLevel(db.Model):
  total = db.IntegerProperty()
  count = db.IntegerProperty()