from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Webinar(models.Model): 

    title=models.CharField(max_length=20)
    description=models.CharField(max_length=1000)
    number_of_speaker=models.IntegerField(default=1)
    event_type=models.CharField(max_length=20, null=True ,blank=True)
    start_date=models.DateField(null=True ,blank=True)
    until_date=models.DateField(null=True, blank=True)
    time=models.CharField(max_length=20)
    banner=models.ImageField(upload_to='banner')
    venue=models.CharField(max_length=40)

    def __str__(self):
        return f"{self.title} - {self.venue}"
    


class Speaker(models.Model):
    webinar=models.ForeignKey(Webinar, on_delete=models.CASCADE)
    speaker_name=models.CharField(max_length=30)
    speaker_email=models.EmailField(max_length=30, null=True)


class WebinarAttendees(models.Model):
    webinar=models.ForeignKey(Webinar, on_delete=models.CASCADE)
    school_id=models.CharField(max_length=20, null=True)
    email=models.EmailField()


class ResponseQuestionaire(models.Model):
      webinar=models.ForeignKey(Webinar, on_delete=models.CASCADE)
      user=models.ForeignKey(User, on_delete=models.CASCADE)
      q1=models.IntegerField()
      q2=models.IntegerField()
      q3=models.IntegerField()
      q4=models.IntegerField()
      q5=models.IntegerField()
      q6=models.IntegerField()

    