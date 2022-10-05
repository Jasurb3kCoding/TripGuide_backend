from hotels.models import Hotel
from hotels.serializers import HotelSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HotelList(APIView):

    def get(self, request, format=None):
        hotel = Hotel.objects.all()
        serializer = HotelSerializer(hotel, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HotelSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelDetail(APIView):

    def get_object(self, pk):
        try:
            return Hotel.objects.get(pk=pk)
        except HotelSerializer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        hotel = self.get_object(pk)
        serializer = HotelSerializer(hotel)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        hotel = self.get_object(pk)
        serializer = HotelSerializer(hotel, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        hotel = self.get_object(pk)
        hotel.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
