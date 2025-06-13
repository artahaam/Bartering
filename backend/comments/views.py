from rest_framework import viewsets, mixins
from .models import Comment
from .serializers import CommentSerializer
from .permissions import IsAuthorOrReadOnly


class CommentViewSet(mixins.RetrieveModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin,
                     viewsets.GenericViewSet):

    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]
