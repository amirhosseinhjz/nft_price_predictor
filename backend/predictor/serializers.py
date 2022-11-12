from django.db.models import fields
from rest_framework import serializers
from .models import NftItem


class NftItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = NftItem
        fields = "__all__"
