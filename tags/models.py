from django.db import models
from taggit.models import Tag

class Rule(models.Model):
	antecedents = models.ManyToManyField(Tag, related_name='antecedents')
	subsequents = models.ManyToManyField(Tag, related_name='subsequents')
	confidence  = models.DecimalField(max_digits=3, decimal_places=2)

	def __str__(self):
		return '('+str(self.antecedents)+')  -->  ('+str(self.subsequents)+')  ['+str(self.confidence)+']'