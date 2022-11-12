from rest_framework import generics
from rest_framework.response import Response
from .serializers import NftItemSerializer
from .models import NftItem
from rest_framework.permissions import IsAuthenticated

class NftItemListView(generics.ListAPIView):
    serializer_class = NftItemSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return NftItem.objects.filter(owner=self.request.user)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class NftItemCreateView(generics.CreateAPIView):
    serializer_class = NftItemSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
