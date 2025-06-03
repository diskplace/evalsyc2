from django.db import models
from django.contrib.auth.models import User
from webinar.models import ResponseQuestionaire, TestResponse

# Create your models here.

class TestResult(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    test=models.CharField(max_length=50)
    type=models.CharField(max_length=50)
    score=models.IntegerField()





