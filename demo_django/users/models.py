from django.db import models

# Create your models here.
class User(models.Model):
  name = models.CharField(max_length=20)
  password = models.CharField(max_length=100)
  is_admin = models.BooleanField()
  last_activity = models.DateTimeField()

  def __unicode__(self):
    return "[id=%d] %s" % (self.id, self.name)
