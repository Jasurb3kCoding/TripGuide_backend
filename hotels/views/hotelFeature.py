from hotels.models import HotelFeature
from hotels.serializers import HotelFeatureSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class HotelFeatureList(APIView):

    def get(self, request, format=None):
        hotel_feature = HotelFeature.objects.all()
        serializer = HotelFeatureSerializer(hotel_feature, many=True)
        return Response(serializer.data)

    def post(self, request, format=None):
        serializer = HotelFeatureSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class HotelFeatureDetail(APIView):

    def get_object(self, pk):
        try:
            return HotelFeature.objects.get(pk=pk)
        except HotelFeatureSerializer.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        hotel_feature = self.get_object(pk)
        serializer = HotelFeatureSerializer(hotel_feature)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        hotel_feature = self.get_object(pk)
        serializer = HotelFeatureSerializer(hotel_feature, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        hotel_feature = self.get_object(pk)
        hotel_feature.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
