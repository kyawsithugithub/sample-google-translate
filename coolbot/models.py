from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Photo(models.Model):
    image = models.ImageField('Label', upload_to='path/')
    
    
class fbUser(models.Model):
    fbID=models.CharField(max_length = 50)
    firstName=models.CharField(max_length = 50)
    lastName=models.CharField(max_length = 50)
    gender=models.CharField(max_length = 50)
    timeZone=models.CharField(max_length = 50)
    locale=models.CharField(max_length = 50)
    preferLanguage=models.CharField(max_length = 50,default='en')
    
    class Meta:
        db_table = "fbUser"
        
        
class language(models.Model):
    languageName=models.CharField(max_length = 20)
    code=models.CharField(max_length = 20)
    
    class Meta:
        db_table = "language"