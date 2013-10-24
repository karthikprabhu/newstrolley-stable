from django.db import models
from accounts.models import NTUser

# Create your models here.
class Feedback(models.Model):
	user = models.ForeignKey(NTUser)
	time = models.DateTimeField(auto_now_add=True)
	text = models.TextField()
	subject = models.CharField(max_length=100)
	
	def __str__(self):
		return self.subject
	
	def __unicode__(self):
		return self.__str__()