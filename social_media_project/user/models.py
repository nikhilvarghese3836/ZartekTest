from django.db import models
from posts.models import Posts
from django.contrib.auth.models import User as AuthUser
from django.contrib.postgres.fields import JSONField
# Create your models here.
class Reacts(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_user = models.ForeignKey(AuthUser, models.DO_NOTHING, blank=True, null=True)
    fk_post = models.ForeignKey(Posts, models.DO_NOTHING, blank=True, null=True)
    react = models.NullBooleanField(null=True)
    timestamp = models.DateTimeField(null=True)

    class Meta:
        managed = True
        db_table = 'reacts'
