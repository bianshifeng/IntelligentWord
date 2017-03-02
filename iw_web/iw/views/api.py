from ..models import Word, QuesRecord
from ..serializers import WordSerializer, UserSerializer, QuesRecordSerializer
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.filters import OrderingFilter,SearchFilter
from django_filters.rest_framework import DjangoFilterBackend
import django_filters


# -----------------------------------

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    """
    This viewset automatically provides `list` and `detail` actions.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer


# -----------------------------------

class WordFilter(django_filters.rest_framework.FilterSet):
    min_id = django_filters.NumberFilter(name="id", lookup_expr='gte')
    max_id = django_filters.NumberFilter(name="id", lookup_expr='lte')

    class Meta:
        model = Word
        fields = ['id', 'word', 'min_id', 'max_id']


class WordViewSet(viewsets.ModelViewSet):
    """
    This viewset automatically provides `list`, `create`, `retrieve`,
    `update` and `destroy` actions.
    """
    queryset = Word.objects.get_word_list()
    serializer_class = WordSerializer
    filter_backends = (DjangoFilterBackend, SearchFilter,OrderingFilter,)
    filter_class = WordFilter
    filter_fields = ('word', 'id')
    ordering_fields = ('word', 'id')
    search_fields = ('word',)

    def perform_create(self, serializer):
        serializer.save()


# --------------------------------

class QuesRecordFilter(django_filters.rest_framework.FilterSet):
    min_id = django_filters.NumberFilter(name="id", lookup_expr='gte')
    max_id = django_filters.NumberFilter(name="id", lookup_expr='lte')

    class Meta:
        model = QuesRecord
        fields = ['id', 'word', 'min_id', 'is_right', 'max_id', 'word__id', 'word_id']


class QuesRecordViewSet(viewsets.ModelViewSet):
    queryset = QuesRecord.objects.all()
    serializer_class = QuesRecordSerializer
    filter_backends = (DjangoFilterBackend, OrderingFilter,)
    filter_class = QuesRecordFilter
    ordering_fields = ('record_time',)

    # filter_fields = ('word', 'id')

    def perform_create(self, serializer):
        serializer.save()
