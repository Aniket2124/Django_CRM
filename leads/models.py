from django.db import models

from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    pass


class Lead(models.Model):   
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    age = models.IntegerField(default=0)
    agent = models.ForeignKey("Agent", on_delete = models.CASCADE)

class Agent(models.Model):
    user = models.OneToOneField(User,on_delete = models.CASCADE)


    # def __str__(self):
    #     pass

    # class Meta:
    #     db_table = ''
    #     managed = True
    #     verbose_name = 'Lead'
    #     verbose_name_plural = 'Leads'