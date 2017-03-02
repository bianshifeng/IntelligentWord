from rest_framework import serializers
from .models import Word, QuesRecord
from django.contrib.auth.models import User


class WordSerializer(serializers.HyperlinkedModelSerializer):
    # random_choose = serializers.HyperlinkedIdentityField(format='html')

    class Meta:
        model = Word
        # fields = ('word','fromLang')
        fields = "__all__"

class QuesRecordSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = QuesRecord
        # fields = ('word','wordId','owner')
        fields = "__all__"


class UserSerializer(serializers.HyperlinkedModelSerializer):
    words = serializers.HyperlinkedRelatedField(many=True, view_name='word-detail', read_only=True)

    class Meta:
        model = User
        fields = ('url', 'id', 'username', 'words')
