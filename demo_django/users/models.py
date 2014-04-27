from django.db import models
from django.utils import timezone
from copy import deepcopy
import pbkdf2

class User(models.Model):
  """
  This class represents users who will be using our system (not to be confused with Django staff
  users!).

  Each user has his own set of files, set of files, and transaction history. There are two types of
  users: regular users and admin users. Admin users have elevated privileges, and you can probably
  guess where those privileges come into play.
  """
  name = models.CharField(max_length=20)
  password_hash = models.CharField(max_length=64)
  is_admin = models.BooleanField()
  last_activity = models.DateTimeField()
  bytes_transferred = models.IntegerField()

  @staticmethod
  def encrypt_password(password):
    return pbkdf2.crypt(password)

  @staticmethod
  def compare_password(real_password_hash, alleged_password):
    if real_password_hash == pbkdf2.crypt(alleged_password, real_password_hash):
      return True
    else:
      return False

  @staticmethod
  def create(name, password):
    """
    Factory method for creating a user with sane default values.
    This method is designed in such a way that it is compatible with PBKDF2.
    """
    password_hash = User.encrypt_password(password)
    return User(name=name, password_hash=password_hash,
                is_admin=False,
                last_activity=timezone.now(),
                bytes_transferred=0)

  @staticmethod
  def lookup(name, password):
    """
    Helper method for logging in. Returns a User object given the user's name and password.
    This method is designed in such a way that it is compatible with PBKDF2.
    """
    user = User.objects.filter(name__iexact=name).first()

    if user:
      if User.compare_password(user.password_hash, password):
        return user
      else:
        return None
    else:
      return None

  def __unicode__(self):
    return "[id=%d] %s" % (self.id, self.name)

  def to_dict(self):
    """Helper method for serializing user objects."""
    result = {}
    result['id'] = deepcopy(self.id)
    result['name'] = deepcopy(self.name)
    # result['password_hash'] = deepcopy(self.password_hash)
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

  def set_password(self, password):
    """Sets the password_hash field to the PBKDF2 hash computed for the given password."""
    self.password_hash = User.encrypt_password(password)
