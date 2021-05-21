from django.db import models
from party_register.models import Party
from party_register.utils import create_new_ref_number

class Admin(models.Model):
    admin_id = models.CharField(max_length = 10, blank=False, editable=False, unique=True, default=create_new_ref_number)
    name = models.CharField(max_length=50, null=False)
    contact_number = models.CharField(max_length=15)
    status = models.CharField(max_length=10, default='ACTIVE')
    isDeleted = models.CharField(max_length=1, default='N')
    description = models.CharField(max_length=250)
    
    def __str__(self):
        return  "{} - {}".format(self.admin_id, self.name)


class AdminRegister(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    created_date = models.DateTimeField(auto_now_add=True)
    admin = models.OneToOneField(Admin, on_delete = models.CASCADE, null=False)


    def __str__(self):
        return self.admin_username


class Document(models.Model):
    item = models.CharField(max_length=30)
    counts = models.CharField(max_length=30)
    category = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(null=True)
    valid_to_date = models.DateTimeField(null=True)
    description = models.CharField(max_length=30)
    admin = models.ForeignKey(Admin, on_delete=models.SET_NULL, null=True)
    party = models.ForeignKey(Party, on_delete=models.CASCADE, null=False)
 
    def __str__(self):
        return '__all__'