from django.db import models
from .utils import create_new_ref_number

class Party(models.Model):
    party_id = models.CharField(max_length = 10, blank=False, editable=False, unique=True, default=create_new_ref_number)
    name = models.CharField(max_length=50, null=False)
    contact_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, default='ACTIVE')
    isDeleted = models.CharField(max_length=1, default='N')
    description = models.CharField(max_length=250)
    
    def __str__(self):
        return "{} - {}".format(self.party_id, self.name)

class PartyRegister(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    party = models.OneToOneField(Party, on_delete = models.CASCADE, null=False)


    def __str__(self):
        return self.party_username



class File(models.Model):
    title = models.CharField(max_length=30)
    document = models.FileField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, null=False)
 
    def __str__(self):
        return self.title
       
# Create your models here.
