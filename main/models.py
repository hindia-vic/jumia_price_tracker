from django.db import models

from django.contrib.auth.models import User

# Create your models here.


class ProductSearch(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE)
    search=models.CharField(max_length=1000)
    price=models.IntegerField()
    status=models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} {self.price}'
