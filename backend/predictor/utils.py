from django.conf import settings
from PIL import Image
import random
import string
from .models import NftItem
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile


def get_random_fname(fmt, length=30):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length)) + '.' + fmt

def resize_image(image, name, size=settings.ITEM_IMAGE_SIZE):
    img = image if isinstance(image, Image.Image) else Image.open(image)
    img = img.resize(size)
    temp = BytesIO()
    # temp.name = name or img.name
    # print((temp.name, img.format))
    name = name or image.name
    format = name.split('.')[-1]
    format = format if format.upper() != 'JPG' else 'jpeg'
    img.save(temp, format)
    temp.seek(0)
    return InMemoryUploadedFile(temp, 'ImageField', name, format, temp.tell(), None)

def get_new_item_image_name(image):
    fmt = image.name.split('.')[-1]
    name = get_random_fname(fmt)
    while NftItem.objects.filter(image__icontains=name).exists():
        name = get_random_fname(fmt)
    return name

def validate_image(image, name=None):
    image = resize_image(image, name=name)
    image.name = get_new_item_image_name(image)
    return image
