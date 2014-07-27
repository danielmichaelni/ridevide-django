from django.db import models
from django.contrib.auth.models import User
from allauth.socialaccount.models import SocialAccount

class UserProfile(models.Model):
    user = models.OneToOneField(User, related_name='profile')

    def __unicode__(self):
        return "{}'s profile".format(self.user.username)

    def get_url(self):
        uid = SocialAccount.objects.filter(user_id=self.user.id)
        if len(uid):
            return uid[0].extra_data['link']
        else:
            return "#"

    class Meta:
        db_table = 'user_profile'

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])

class Ride(models.Model):
    departure = models.CharField(max_length=200)
    destination = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    riders = models.ManyToManyField(UserProfile)
    from_campus = models.BooleanField()

    def __unicode__(self):
        return "from %s to %s" % (self.departure, self.destination)