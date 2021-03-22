from rest_framework import serializers
from .models import Usuario
from .models import Tweet
from .models import Hashtag
from .models import Sentimiento
from .models import Dataconsulta
from .models import TweetHashtag

class UsuarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Usuario
        fields = ['id_usuario','nombre','numseguidor','numtweet','imgusuario','verificado','urlusuario']


class TweetSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tweet
        fields = ['id_tweet','url','numlikes','numcitado','numretweet','numrespuesta','texto','fecha','hora',
                  'id_retweeted','id_citado','usuario_id_usuario','sentimiento_id_sentimiento']

class TweetHashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = TweetHashtag
        fields = ['id_tweet_hashtag', 'tweet_id_tweet','hashtag_id_hashtag']


class HashtagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hashtag
        fields = ['id_hashtag','hashtag']


class SentimientoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sentimiento
        fields = ['id_sentimiento','sentimiento']


class DataconsultaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Dataconsulta
        fields = ['id_dataconsulta','data']
