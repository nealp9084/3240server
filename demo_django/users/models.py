from django.db import models
from copy import deepcopy

# Create your models here.
class User(models.Model):
  name = models.CharField(max_length=20)
  password = models.CharField(max_length=100)
  is_admin = models.BooleanField()
  last_activity = models.DateTimeField()

  def __unicode__(self):
    return "[id=%d] %s" % (self.id, self.name)

  def to_dict(self):
    result = {}
    result['name'] = deepcopy(self.name)
    result['password'] = deepcopy(self.password)
    result['is_admin'] = deepcopy(self.is_admin)
    result['last_activity'] = deepcopy(str(self.last_activity))
    return result
