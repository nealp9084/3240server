from django.db import models
from django.utils import timezone
from copy import deepcopy

from users.models import User

# Create your models here.
class File(models.Model):
  local_path = models.CharField(max_length=256)
  last_modified = models.DateTimeField()
  file_data = models.BinaryField()
  owner = models.ForeignKey('users.User')
  size = models.IntegerField()

  @staticmethod
  def create(local_path, last_modified, file_data, owner):
    """Factory method for creating a file with sane default values."""
    return File(local_path=local_path,
                last_modified=last_modified,
                file_data=file_data,
                owner=owner,
                size=len(file_data))

  def __unicode__(self):
    return "[id=%d] %s's %s (%d bytes)" % \
           (self.id, self.owner.name, self.local_path, self.size)

  def to_dict(self):
    result = {}
    result['id'] = deepcopy(self.id)
    result['local_path'] = deepcopy(self.local_path)
    result['last_modified'] = str(self.last_modified)
    result['owner_id'] = deepcopy(self.owner_id)
    result['size'] = deepcopy(self.size)
    return result

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

  def sync(self, user_timestamp, user_data, user_local_path):
    """
    Updates the contents of a particular file on the server.
    """
    assert self.is_sync_needed(user_timestamp) != 0

    self.last_modified = user_timestamp
    self.file_data = user_data
    self.size = len(user_data)
    self.local_path = user_local_path

# TODO: fix bug when deleting files (it deletes the history entry too!)
class History(models.Model):
  # which user performed this transaction?
  who = models.ForeignKey('users.User')
  # which file was affected by this transaction?
  what = models.ForeignKey('sync.File')
  # what type of transaction was this? Create, Retrieve, Update, or Delete?
  type = models.CharField(max_length=1)
  # when did this transaction occur?
  when = models.DateTimeField()

  def __unicode__(self):
    return "[id=%d] User %d accessed File %d (%s)" % \
           (self.id, self.who_id, self.what_id, self.type)

  def to_dict(self):
    result = {}
    result['id'] = deepcopy(self.id)
    result['who_id'] = deepcopy(self.who_id)
    result['what_id'] = deepcopy(self.what_id)
    result['type'] = deepcopy(self.type)
    result['when'] = str(self.when)
    return result

  @staticmethod
  def log_creation(who_, what_):
    h = History(who=who_, what=what_, type='C', when=timezone.now())
    h.save()

  @staticmethod
  def log_retrieval(who_, what_):
    h = History(who=who_, what=what_, type='R', when=timezone.now())
    h.save()

  @staticmethod
  def log_update(who_, what_):
    h = History(who=who_, what=what_, type='U', when=timezone.now())
    h.save()

  @staticmethod
  def log_deletion(who_, what_):
    h = History(who=who_, what=what_, type='D', when=timezone.now())
    h.save()

