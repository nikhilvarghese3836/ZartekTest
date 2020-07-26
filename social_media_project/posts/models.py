from django.db import models
from django.contrib.postgres.fields import JSONField

# Create your models here.
class Posts(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    title = models.CharField(max_length=50,blank=True, null=True)
    description = models.CharField(max_length=500,blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        managed = True
        db_table = 'posts'

class TagWeight(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_post = models.ForeignKey(Posts, models.DO_NOTHING, blank=True, null=True)
    tag = models.CharField(max_length=50,blank=True, null=True)
    weight = models.IntegerField(blank=True, null=True)
    class Meta:
        managed = True
        db_table = 'tagweight'

class PostImage(models.Model):
    pk_bint_id = models.BigAutoField(primary_key=True)
    fk_post = models.ForeignKey(Posts, models.DO_NOTHING, blank=True, null=True)
    images = models.ImageField(blank=True, null=True)

    class Meta:
        managed = True
        db_table = 'postimages'



