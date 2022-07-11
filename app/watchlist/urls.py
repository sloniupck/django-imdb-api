from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register('stream', views.StreamPlatformViewSet, basename='stream')

urlpatterns = [
    path('list/', views.WatchListView.as_view(), name='movie-list'),
    path('<int:pk>', views.WatchListDetailView.as_view(), name='movie-detail'),
    path('stream/<int:pk>/review', views.ReviewView.as_view(), name='review-list'),
    path('stream/review/<int:pk>', views.ReviewDetailView.as_view(), name='review-detail'),
    path('stream/<int:pk>/review-create', views.ReviewCreateView.as_view(), name='review-create'),

    path('', include(router.urls)),
]
