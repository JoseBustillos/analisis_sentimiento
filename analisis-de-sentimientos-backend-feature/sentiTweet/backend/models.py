# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Dataconsulta(models.Model):
    id_dataconsulta = models.AutoField(db_column='ID_DATAcONSULTA', primary_key=True)  # Field name made lowercase.
    data = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'DATAcONSULTA'


class Hashtag(models.Model):
    id_hashtag = models.AutoField(db_column='ID_HASHTAG', primary_key=True)  # Field name made lowercase.
    hashtag = models.CharField(max_length=200, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'HASHTAG'


class Sentimiento(models.Model):
    id_sentimiento = models.AutoField(db_column='ID_SENTIMIENTO', primary_key=True)  # Field name made lowercase.
    sentimiento = models.CharField(max_length=40, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'SENTIMIENTO'


class Tweet(models.Model):
    id_tweet = models.AutoField(db_column='ID_TWEET', primary_key=True)  # Field name made lowercase.
    url = models.CharField(max_length=400, blank=True, null=True)
    numlikes = models.IntegerField(db_column='numLikes', blank=True, null=True)  # Field name made lowercase.
    numcitado = models.IntegerField(db_column='numCitado', blank=True, null=True)  # Field name made lowercase.
    numretweet = models.IntegerField(db_column='numRetweet', blank=True, null=True)  # Field name made lowercase.
    numrespuesta = models.IntegerField(db_column='numRespuesta', blank=True, null=True)  # Field name made lowercase.
    texto = models.CharField(max_length=800, blank=True, null=True)
    fecha = models.DateField(blank=True, null=True)
    hora = models.TimeField(blank=True, null=True)
    id_retweeted = models.ForeignKey('self', related_name="tags", on_delete=models.CASCADE, db_column='id_retweeted',
                                     blank=True, null=True)
    id_citado = models.ForeignKey('self', on_delete=models.CASCADE, db_column='id_citado', blank=True, null=True)
    usuario_id_usuario = models.ForeignKey('Usuario', models.DO_NOTHING, db_column='usuario_ID_USUARIO', blank=True,
                                           null=True)  # Field name made lowercase.
    sentimiento_id_sentimiento = models.ForeignKey(Sentimiento, models.DO_NOTHING,
                                                   db_column='sentimiento_ID_SENTIMIENTO', blank=True,
                                                   null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TWEET'

    def __str__(self):
        return '%s %s' % (self.id_tweet, self.texto)


class TweetHashtag(models.Model):
    id_tweet_hashtag = models.AutoField(db_column='ID_TWEET_HASHTAG', primary_key=True)  # Field name made lowercase.
    tweet_id_tweet = models.ForeignKey(Tweet, models.DO_NOTHING, db_column='tweet_ID_TWEET', blank=True,
                                       null=True)  # Field name made lowercase.
    hashtag_id_hashtag = models.ForeignKey(Hashtag, models.DO_NOTHING, db_column='hashtag_ID_HASHTAG', blank=True,
                                           null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TWEET_HASHTAG'


class Usuario(models.Model):
    id_usuario = models.AutoField(db_column='ID_USUARIO', primary_key=True)  # Field name made lowercase.
    nombre = models.CharField(max_length=200, blank=True, null=True)
    numseguidor = models.IntegerField(db_column='numSeguidor', blank=True, null=True)  # Field name made lowercase.
    numtweet = models.IntegerField(db_column='numTweet', blank=True, null=True)  # Field name made lowercase.
    imgusuario = models.CharField(db_column='imgUsuario', max_length=400, blank=True,
                                  null=True)  # Field name made lowercase.
    verificado = models.BooleanField(blank=True, null=True)
    urlusuario = models.CharField(db_column='urlUsuario', max_length=300, blank=True,
                                  null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'USUARIO'
