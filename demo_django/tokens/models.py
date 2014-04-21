from django.db import models
from copy import deepcopy
import random

from users.models import User

class Token(models.Model):
  """
  This class represents access tokens, similar to the ones in authentications schemes like OAuth.
  We can use access tokens as a way of avoiding password exchanges.

  One of the implications is that if a user token is leaked or otherwise stolen, we can always
  revoke it without ever having to inconvenience the user.

  Another implication is that we don't have to exchange the password back-and-forth in cleartext.
  This means that if someone is intercepting your traffic, they won't be able to figure out your
  password (unless they intercepted right as you logged in).
  """
  user = models.ForeignKey('users.User')
  secret = models.CharField(max_length=130)

  @staticmethod
  def create(user):
    """
    Factory method for creating an access token. The token will pretty much always be long and
    unpredictable. Due to the access token's length, it will be resistant to birthday attacks.
    """
    rng = random.SystemRandom()
    number = rng.randint(1 << 256, 1 << 512)
    secret = format(number, 'x')
    return Token(user=user, secret=secret)

  def __unicode__(self):
    return "[id=%d] %s: %s" % \
           (self.id, self.user.name, self.secret)

  def to_dict(self):
    """Helper method for serializing token objects."""
    result = {}
    result['id'] = deepcopy(self.id)
    result['user_id'] = deepcopy(self.user.id)
    result['secret'] = deepcopy(self.secret)
    return result

  @staticmethod
  def get_current_user(secret):
    """Helper method for obtaining the user associated with a particular access token."""
    token = Token.objects.filter(secret=secret).first()

    if token:
      return token.user
    else:
      return None
