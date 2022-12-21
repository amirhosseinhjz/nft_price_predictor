from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class NftItem(models.Model):
    name = models.CharField(max_length=200, null=True)
    image             = models.ImageField(upload_to=settings.ITEM_IMAGES_DIR)
    price_level       = models.IntegerField()
    owner             = models.ForeignKey(User, on_delete=models.CASCADE)
    date_created      = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name