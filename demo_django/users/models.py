from django.db import models
from django.utils import timezone
from copy import deepcopy

class User(models.Model):
  """
  This class represents users who will be using our system (not to be confused with Django staff
  users!).

  Each user has his own set of files, set of files, and transaction history. There are two types of
  users: regular users and admin users. Admin users have elevated privileges, and you can probably
  guess where those privileges come into play.
  """
  name = models.CharField(max_length=20)
  password = models.CharField(max_length=100)
  is_admin = models.BooleanField()
  last_activity = models.DateTimeField()
  bytes_transferred = models.IntegerField()

  @staticmethod
  def create(name, password):
    """Factory method for creating a user with sane default values."""
    return User(name=name, password=password,
                is_admin=False,
                last_activity=timezone.now(),
                bytes_transferred=0)

  def __unicode__(self):
    return "[id=%d] %s" % (self.id, self.name)

  def to_dict(self):
    """Helper method for serializing user objects."""
    result = {}
    result['id'] = deepcopy(self.id)
    result['name'] = deepcopy(self.name)
    # result['password'] = deepcopy(self.password)
    result['is_admin'] = deepcopy(self.is_admin)
    result['last_activity'] = str(self.last_activity)
    result['bytes_transferred'] = deepcopy(self.bytes_transferred)
    return result

  def touch(self):
    """Updates the last_activity field on the current user (a la UNIX)."""
    self.last_activity = timezone.now()

  def save(self, *args, **kwargs):
    """
    This overrides the Django model save method.
    It always updates the last_activity field before saving the user.
    """
    self.touch()
    super(User, self).save(*args, **kwargs)
