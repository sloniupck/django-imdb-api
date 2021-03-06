from .models import Watch, StreamPlatform, Review
from .serializers import WatchListSerializer, StreamPlatformSerializer, ReviewSerializer
from rest_framework import generics, viewsets
from rest_framework.exceptions import ValidationError
from .permissions import IsReviewUserOrReadOnly, IsAdminOrReadOnly
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from .paginnation import WatchListPagination


class ReviewCreateView(generics.CreateAPIView):

    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        watch = Watch.objects.get(pk=pk)
        user = self.request.user
        user_review = Review.objects.filter(watch=watch, review_user=user)

        if user_review.exists():
            raise ValidationError("You have commented this watch!")

        if watch.avg_rating == 0:
            watch.avg_rating = serializer.validated_data['rating']
        else:
            watch.avg_rating = (watch.avg_rating + serializer.validated_data['rating']) / 2

        watch.ratings_number += 1
        watch.save()
        serializer.save(watch=watch, review_user=user)


class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsReviewUserOrReadOnly]


class ReviewView(generics.ListAPIView):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watch=pk)


class StreamPlatformViewSet(viewsets.ModelViewSet):

    queryset = StreamPlatform.objects.all()
    serializer_class = StreamPlatformSerializer
    permission_classes = [IsAdminOrReadOnly]


class WatchListView(generics.ListCreateAPIView):

    queryset = Watch.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['title', 'platform__name']
    pagination_class = WatchListPagination


class WatchListDetailView(generics.RetrieveUpdateDestroyAPIView):

    queryset = Watch.objects.all()
    serializer_class = WatchListSerializer
    permission_classes = [IsAdminOrReadOnly]

