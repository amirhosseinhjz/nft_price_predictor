from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NftItem(models.Model):
    name = models.CharField(max_length=200)
    image             = models.ImageField(upload_to='item_images/')
    price_level       = models.IntegerField()
    owner             = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created      = models.DateTimeField(auto_now_add=True)
    # description = models.TextField()

    def __str__(self):
        return self.name