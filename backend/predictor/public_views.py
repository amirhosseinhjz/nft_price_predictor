from rest_framework import generics
from rest_framework.response import Response
from .serializers import PublicNftItemSerializer
from .models import NftItem
from rest_framework.permissions import IsAuthenticated, AllowAny




class NftRankItemsView(generics.ListAPIView):
    serializer_class = PublicNftItemSerializer
    permission_classes = [AllowAny]
    DEFAULT_ITEMS_COUNT = 5

    def get_queryset(self):
        items_count = self.request.query_params.get('count', self.DEFAULT_ITEMS_COUNT)
        queryset = NftItem.objects.all().order_by('-price_level')[0:items_count]
        return queryset

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        '''
        Get a list of the top NFTs ranked by price level
        query params:
        - count: the number of items to return
        '''
        return self.list(request, *args, **kwargs)