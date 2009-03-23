from django.db import models


class Item(models.Model):
	name = models.CharField(max_length=200)
	price = models.FloatField()
	image = models.ImageField(upload_to="items")
	collection = models.ForeignKey('Collection', related_name="items")

	def __unicode__(self):
		return self.name


class Collection(models.Model):
	name = models.CharField(max_length=200)

	def __unicode__(self):
		return self.name
