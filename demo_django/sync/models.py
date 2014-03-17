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
    Returns 0, 1, or 2, depending on what kind of sync is needed.
    """
    if self.last_modified < user_timestamp:
      # The file on the user's filesystem is newer than the one stored online
      # must sync: replace the file on the server
      return 1
    elif self.last_modified == user_timestamp:
      # The file on the user's filesystem has the same timestamp as the one
      # stored online
      # do not sync
      return 0
    else:
      # The file on the user's filesystem is older than the one stored online
      # must sync: replace the file on the user's filesystem
      return 2

  def sync(self, user_timestamp, user_data):
    """
    Updates the contents of a particular file on the server.
    """
    assert self.is_sync_needed(user_timestamp) != 0

    self.last_modified = user_timestamp
    self.data = user_data
