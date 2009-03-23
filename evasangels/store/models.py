from django.db import models


class Item(models.Model):
	collection  = models.ForeignKey('Collection', related_name="items")
	name        = models.CharField(max_length=200)
	description = models.TextField()
	image       = models.ImageField(upload_to="items")
	thumbnail   = models.ImageField(upload_to="items")
	price       = models.FloatField()
	paypal_id   = models.CharField(max_length=16)

	def __unicode__(self):
		return self.name


class Collection(models.Model):
	name        = models.CharField(max_length=200)
	description = models.TextField()

	def __unicode__(self):
		return self.name
