from django.db import models
import time
from copy import deepcopy
import random

from users.models import User

# Create your models here.
class Token(models.Model):
  user = models.ForeignKey('users.User')
  secret = models.BigIntegerField()

  def __unicode__(self):
    return "[id=%d] %s : %d" % \
           (self.id, self.user.name, self.secret)

  def to_dict(self):
    result = {}
    result['id'] = deepcopy(self.id)
    result['user'] = deepcopy(self.user.name)
    result['secret'] = deepcopy(self.secret)
    return result

  @staticmethod
  def create(user_obj):
    seed = time.time()
    rng = random.SystemRandom(seed)
    number = rng.randint(1, 1 << 256)
    return Token(user=user_obj, secret=number)

# TODO: awesome feature - we can use tokens as a way of avoiding password exchanges
# One of the implications is that if a user token is leaked, we can revoke it without ever having
# to inconvenience the user.
# Another implication is that we don't have to exchange the password back-and-forth in cleartext. So
# if someone is intercepting your traffic (after you have logged in), they won't be able to figure
# out your password.
