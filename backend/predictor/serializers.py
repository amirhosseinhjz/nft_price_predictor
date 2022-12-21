from django.db.models import fields
from rest_framework import serializers
from .utils import validate_image
from .models import NftItem
from .predictor_model.resnet_model import ResnetModel
import requests
from PIL import Image
import base64
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site

class NftItemSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):
        image_name = obj.image.url.split('/')[-1]
        site = get_current_site(self.context['request'])
        return f'http://{site.domain}/{settings.ITEM_IMAGES_URL}{image_name}'

    class Meta:
        model = NftItem
        exclude = ["image"]

    def save(self, **kwargs):
        kwargs["owner"] = self.context["request"].user
        return super().save(**kwargs)


class PublicNftItemSerializer(serializers.ModelSerializer):
    url = serializers.SerializerMethodField('get_url')

    def get_url(self, obj):
        image_name = obj.image.url.split('/')[-1]
        site = get_current_site(self.context['request'])
        return f'http://{site.domain}/{settings.ITEM_IMAGES_URL}{image_name}'

    class Meta:
        model = NftItem
        fields = ["id", 'url', "price_level"]


class NftItemCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = NftItem
        fields = ["image", "name"]

    def save(self, **kwargs) -> dict:
        return self.create(self.validated_data)

    def create(self, validated_data) -> dict:
        item = NftItem()
        item.image = validate_image(validated_data["image"])
        item.owner = self.context["request"].user
        item.price_level = ResnetModel.predict(base64.b64encode(validated_data["image"].read()))#validated_data["image"].read())
        item.save()
        return {'id': item.id, 'message': 'success'}

    @staticmethod
    def create_from_url(request, url) -> dict:
        image = Image.open(requests.get(url, stream=True).raw)#requests.get(url).content
        name = url.split("/")[-1]
        request.data["image"] = validate_image(image, name=name).open()
        print(request.data)
        serializer = NftItemCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return serializer.save()
