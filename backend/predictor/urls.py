from django.urls import path
from .views import NftItemListView

app_name = 'predictor'

urlpatterns = [
    path('items/', NftItemListView.as_view(), name="list"),
]