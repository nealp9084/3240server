from django.db import models
from users.models import User

# Create your models here.
class File(models.Model):
  path = models.CharField(max_length=256)
  last_modified = models.DateTimeField()
  data = models.BinaryField()
  owner = models.ForeignKey('users.User')

  def __unicode__(self):
    return "[id=%d] %s's %s" % (self.id, self.owner.name, self.path)

  def is_sync_needed(self, user_timestamp):
    """
    Determines whether a particular file needs to be synced using the timestamp
    value from the user's file.
    """
    if self.last_modified < user_timestamp:
      # The file on the user's filesystem is newer than the one stored online
      # must sync: replace the file on the server
      return True
    elif self.last_modified == user_timestamp:
      # The file on the user's filesystem has the same timestamp as the one
      # stored online
      # do not sync
      return False
    else:
      # The file on the user's filesystem is older than the one stored online
      # must sync: replace the file on the user's filesystem
      return True

  def sync(self, user_timestamp, user_data):
    """
    Updates the contents of a particular file on the server.
    """
    assert self.is_sync_needed(user_timestamp)

    self.last_modified = user_timestamp
    self.data = user_data
