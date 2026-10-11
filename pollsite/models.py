from django.db import models
from django.utils import timezone

import datetime

class Tag(models.Model):
    name = models.CharField(max_length=50,unique=True)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.CharField(max_length= 200)
    pub_date = models.DateTimeField("date published")
    tags = models.ManyToManyField(Tag,blank=True,related_name="questions")

    def __str__(self):
        return self.question_text   

    def was_published_recently(self):
        return timezone.now() - datetime.timedelta(days=1) <= self.pub_date <= timezone.now()

class Choice(models.Model):
    Question = models.ForeignKey(Question,on_delete= models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text