from rest_framework import generics
from rest_framework.response import Response
from .serializers import NftItemSerializer, NftItemCreateSerializer
from .models import NftItem
# from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner, IsLoggedIn
from.paginators import UserItemHistoryPagination
import requests
from io import BytesIO
from rest_framework_swagger import renderers

class NftItemListView(generics.ListAPIView):
    serializer_class = NftItemSerializer
    permission_classes = [IsLoggedIn]
    pagination_class = UserItemHistoryPagination

    def get_queryset(self):
        return NftItem.objects.filter(owner=self.request.user)

    def get(self, request, *args, **kwargs):
        '''
        Get a list of all the NFTs owned by the user

        query params:
        - page: the page number
        - page_size: the number of items per page
        '''
        return self.list(request, *args, **kwargs)

class NftItemCreateView(generics.CreateAPIView):
    serializer_class = NftItemCreateSerializer
    permission_classes = [IsLoggedIn]

    def perform_create(self, serializer) -> dict:
        return serializer.save(owner=self.request.user)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(response, status=201, headers=headers)

    def post(self, request, *args, **kwargs):
        '''
        Create a new NFT item:
        '''
        return self.create(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        '''
        Create a new NFT item from a URL:
        query params:
        - url: the url to the image
        *** This endpoint has some issues not fixed yet
        '''
        url = request.query_params.get('url')
        response = NftItemCreateSerializer.create_from_url(request, url)
        return Response(response, status=201)


class NftItemDetailView(generics.RetrieveAPIView):
    serializer_class = NftItemSerializer
    permission_classes = [IsOwner, IsLoggedIn]
    
    def get_queryset(self):
        return NftItem.objects.filter(owner=self.request.user, pk=self.kwargs['pk'])

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        '''
        Get a specific NFT item by ID
        Provide the ID of the NFT item in the URL:
        - id: the id of the NFT item
        - name: the name of the NFT item
        - image: the image of the NFT item
        - price_level: the price level of the NFT item
        - owner: the owner of the NFT item
        - date_created: the date the NFT item was created
        '''
        return self.retrieve(request, *args, **kwargs)