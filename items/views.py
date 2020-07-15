from django.shortcuts import render
from items.models import Item
from items.serializers import ItemSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import urllib

# Create your views here.
class ItemList(APIView):
    """
    List all items, or create a new item.
    """
    def get(self, request, format=None):
        items = Item.objects.all()
        serializer = ItemSerializer(items, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        request_data = request.data
        # Fetch from Math.js api
        expr_data = "{}+({}*{}/{})".format(request_data['price'], request_data['price'], request_data['gstSlab'], 100)
        url = "http://api.mathjs.org/v4/?" + urllib.parse.urlencode({'expr': expr_data})
        res = requests.request("GET", url)
        # Update Gst Price from POST request
        request_data['gstPrice'] = res.text
        serializer = ItemSerializer(data=request_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ItemDetail(APIView):
    """
    Retrieve, update or delete a item instance.
    """
    def get_object(self, pk):
        try:
            return Item.objects.get(pk=pk)
        except Item.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item)
        return Response(serializer.data)

    # Yet to update gstPrice before put
    def put(self, request, pk, format=None):
        item = self.get_object(pk)
        serializer = ItemSerializer(item, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        item = self.get_object(pk)
        item.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)