from django.db import models

'''class User:
    user

class ChallengeTag:
    id =
    name
    description

class UserChallenge:
    id
    user
    challenge
'''
class Challenge(models.Model):
    #id =
    name = models.CharField(256)
    description = models.TextField()
    #tags
