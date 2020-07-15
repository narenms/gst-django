from rest_framework import serializers
from .models import Item

# Item Serializer
class ItemSerializer(serializers.ModelSerializer):
  class Meta:
    model = Item
    fields = ('id', 'name', 'price', 'gstSlab', 'gstPrice')