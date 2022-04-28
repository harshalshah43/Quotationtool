from django.db import models
from django.contrib.auth.models import User

e_type_choices = [
    ('CRM','CustomerRelationShipMgr'),
    ('MD','MD')
]

class Employee(models.Model):
    employee = models.ForeignKey(User,on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    e_type = models.CharField(max_length = 50,choices=e_type_choices)

    def __str__(self):
        return f'{self.name} {self.e_type}'