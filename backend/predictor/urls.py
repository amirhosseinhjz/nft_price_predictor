from django.urls import path, re_path
from .views import NftItemListView, NftItemCreateView, NftItemDetailView
from .public_views import NftRankItemsView
app_name = 'predictor'

urlpatterns = [
    path('items/', NftItemListView.as_view(), name="list"),
    path('items/new/', NftItemCreateView.as_view(), name="create"),
    path('items/<int:pk>/', NftItemDetailView.as_view(), name="detail"),
    re_path(r'^items/ranks/', NftRankItemsView.as_view(), name="rank"),
]
