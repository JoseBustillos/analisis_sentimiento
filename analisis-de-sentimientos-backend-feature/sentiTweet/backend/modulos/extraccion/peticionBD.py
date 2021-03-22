from ...models import Usuario
from ...models import Tweet
from ...models import TweetHashtag
from ...models import Sentimiento
from ...models import Hashtag
import datetime


def actualizarUsuario(dia, tweet):
    if tweet == "original":
        Usuario.objects.get(nombre=dia["user"]["name"]).update(
            numseguidor=dia["user"]["followers_count"],
            verificado=dia["user"]["verified"],
            numtweet=dia["user"]["statuses_count"],
            imgusuario=dia["user"]["profile_image_url"],
        )
    if tweet == "retweeted":
        Usuario.objects.get(nombre=dia["retweeted_status"]["user"]["name"]).update(
            numseguidor=dia["retweeted_status"]["user"]["followers_count"],
            verificado=dia["retweeted_status"]["user"]["verified"],
            numtweet=dia["retweeted_status"]["user"]["statuses_count"],
            imgusuario=dia["retweeted_status"]["user"]["profile_image_url"],
        )
    if tweet == "quoted":
        Usuario.objects.get(nombre=dia["quoted_status"]["user"]["name"]).update(
            numseguidor=dia["quoted_status"]["user"]["followers_count"],
            verificado=dia["quoted_status"]["user"]["verified"],
            numtweet=dia["quoted_status"]["user"]["statuses_count"],
            imgusuario=dia["quoted_status"]["user"]["profile_image_url"],
        )
    return True


def almacenarUsuario(dia, tweet):
    # instancia de la clase Usuario
    usuario = Usuario()
    usuario.id_usuario
    if tweet == "original":
        # enviar las propiedades de la clase
        url = "https://twitter.com/" + dia["user"]["screen_name"]
        usuario.nombre = dia["user"]["name"]
        usuario.numseguidor = dia["user"]["followers_count"]
        usuario.numtweet = dia["user"]["statuses_count"]
        usuario.imgusuario = dia["user"]["profile_image_url"]
        usuario.verificado = dia["user"]["verified"]
    if tweet == "retweeted":
        # enviar las propiedades de la clase
        url = "https://twitter.com/" + dia["retweeted_status"]["user"]["screen_name"]
        usuario.nombre = dia["retweeted_status"]["user"]["name"]
        usuario.numseguidor = dia["retweeted_status"]["user"]["followers_count"]
        usuario.numtweet = dia["retweeted_status"]["user"]["statuses_count"]
        usuario.imgusuario = dia["retweeted_status"]["user"]["profile_image_url"]
        usuario.verificado = dia["retweeted_status"]["user"]["verified"]
        # llamar metodo save para almacenar en bd
        usuario.save()
    if tweet == "quoted":
        url = "https://twitter.com/" + dia["quoted_status"]["user"]["screen_name"]
        usuario.nombre = dia["quoted_status"]["user"]["name"]
        usuario.numseguidor = dia["quoted_status"]["user"]["followers_count"]
        usuario.numtweet = dia["quoted_status"]["user"]["statuses_count"]
        usuario.imgusuario = dia["quoted_status"]["user"]["profile_image_url"]
        usuario.verificado = dia["quoted_status"]["user"]["verified"]
    usuario.urlusuario = url.replace(" ", "")
    # llamar metodo save para almacenar en bd
    usuario.save()
    return True


def actualizarTweet(dia, tweet, texto):
    if tweet == "original":
        # consulta si tweet existe en la bd
        u = Usuario.objects.get(nombre=dia["user"]["name"])
        Tweet.objects.get(texto=texto, usuario_id_usuario=u).update(
            url="https://twitter.com/"
            + dia["user"]["screen_name"]
            + "/status/"
            + dia["id_str"],
            numlikes=dia["favorite_count"],
            numcitado=dia["quote_count"],
            numretweet=dia["retweet_count"],
            numrespuesta=dia["reply_count"],
        )
    if tweet == "retweeted":
        u = Usuario.objects.get(nombre=dia["retweeted_status"]["user"]["name"])
        Tweet.objects.get(texto=texto, usuario_id_usuario=u).update(
            url="https://twitter.com/"
            + dia["retweeted_status"]["user"]["screen_name"]
            + "/status/"
            + dia["retweeted_status"]["id_str"],
            numlikes=dia["retweeted_status"]["favorite_count"],
            numcitado=dia["retweeted_status"]["quote_count"],
            numretweet=dia["retweeted_status"]["retweet_count"],
            numrespuesta=dia["retweeted_status"]["reply_count"],
        )
    if tweet == "quoted":
        u = Usuario.objects.get(nombre=dia["quoted_status"]["user"]["name"])
        Tweet.objects.get(texto=texto, usuario_id_usuario=u).update(
            url="https://twitter.com/"
            + dia["quoted_status"]["user"]["screen_name"]
            + "/status/"
            + dia["quoted_status"]["id_str"],
            numlikes=dia["quoted_status"]["favorite_count"],
            numcitado=dia["quoted_status"]["quote_count"],
            numretweet=dia["quoted_status"]["retweet_count"],
            numrespuesta=dia["quoted_status"]["reply_count"],
        )
    return True


def almacenarTweet(dia, tweetEstado, texto, sen):
    tweet = Tweet()
    tweet.id_tweet
    if tweetEstado == "original":
        # enviar las propiedades de la clase
        tweet.url = (
            "https://twitter.com/"
            + dia["user"]["screen_name"]
            + "/status/"
            + dia["id_str"]
        )
        tweet.numlikes = dia["favorite_count"]
        tweet.numcitado = dia["quote_count"]
        tweet.numretweet = dia["retweet_count"]
        tweet.numrespuesta = dia["reply_count"]
        # buscar usuario del tweet realizado y llenar la clase Usuario
        idUser = Usuario.objects.get(nombre=dia["user"]["name"])
    if tweetEstado == "retweeted":
        tweet.url = (
            "https://twitter.com/"
            + dia["retweeted_status"]["user"]["screen_name"]
            + "/status/"
            + dia["retweeted_status"]["id_str"]
        )
        tweet.numlikes = dia["retweeted_status"]["favorite_count"]
        tweet.numcitado = dia["retweeted_status"]["quote_count"]
        tweet.numretweet = dia["retweeted_status"]["retweet_count"]
        tweet.numrespuesta = dia["retweeted_status"]["reply_count"]
        idUser = Usuario.objects.get(nombre=dia["retweeted_status"]["user"]["name"])
    if tweetEstado == "quoted":
        tweet.url = (
            "https://twitter.com/"
            + dia["quoted_status"]["user"]["screen_name"]
            + "/status/"
            + dia["quoted_status"]["id_str"]
        )
        tweet.numlikes = dia["quoted_status"]["favorite_count"]
        tweet.numcitado = dia["quoted_status"]["quote_count"]
        tweet.numretweet = dia["quoted_status"]["retweet_count"]
        tweet.numrespuesta = dia["quoted_status"]["reply_count"]
        idUser = Usuario.objects.get(nombre=dia["quoted_status"]["user"]["name"])
    tweet.usuario_id_usuario = idUser
    # buscar sentimiento del tweet obtenido en bd y llenar la clase Sentimiento
    idSenti = Sentimiento.objects.get(sentimiento=sen)
    tweet.sentimiento_id_sentimiento = idSenti
    tweet.texto = texto
    tweet.fecha = datetime.datetime.now().date()
    tweet.hora = datetime.datetime.now().time()
    # llamar metodo save para almacenar en bd
    tweet.save()
    return True


def asignarRetweet(dia, texto):
    u = Usuario.objects.get(nombre=dia["retweeted_status"]["user"]["name"])
    t = Tweet.objects.get(texto=texto.replace("RT ", ""), usuario_id_usuario=u)
    Tweet.objects.filter(texto=texto).update(id_retweeted=t)
    return True


def asingarCita(dia, texto):
    u = Usuario.objects.get(nombre=dia["quoted_status"]["user"]["name"])
    t = Tweet.objects.get(texto=texto, usuario_id_usuario=u)
    Tweet.objects.filter(texto=texto).update(id_citado=t)
    return True


def almacenarHashtag(dia, tweetEstado, texto, hashtag):
    hastwe = TweetHashtag()
    # buscando hashtag en la bd
    idHash = Hashtag.objects.get(hashtag=hashtag)
    if tweetEstado == "original":
        # buscando texto que posee dicho hashtag
        u = Usuario.objects.get(nombre=dia["user"]["name"])
        idTweet = Tweet.objects.get(texto=texto, usuario_id_usuario=u)
    if tweetEstado == "retweeted":
        u = Usuario.objects.get(nombre=dia["retweeted_status"]["user"]["name"])
        idTweet = Tweet.objects.get(texto=texto, usuario_id_usuario=u)
    if tweetEstado == "quoted":
        u = Usuario.objects.get(nombre=dia["quoted_status"]["user"]["name"])
        idTweet = Tweet.objects.get(texto=texto, usuario_id_usuario=u)
    hastwe.id_tweet_hashtag
    hastwe.hashtag_id_hashtag = idHash
    hastwe.tweet_id_tweet = idTweet
    hastwe.save()
    return True


def asignarHashtagTeet(dia, tweetEstado, texto, hashtag):
    hashtag = Hashtag()
    hashtag.id_hashtag
    hashtag.hashtag = hashtag
    hashtag.save()
    # buscando hashtag en la bd
    idHash = Hashtag.objects.get(hashtag=hashtag)
    # buscando texto que posee dicho hashtag
    if tweetEstado == "original":
        u = Usuario.objects.get(nombre=dia["user"]["name"])
    if tweetEstado == "retweeted":
        u = Usuario.objects.get(nombre=dia["retweeted_status"]["user"]["name"])
    if tweetEstado == "quoted":
        u = Usuario.objects.get(nombre=dia["quoted_status"]["user"]["name"])
    idTweet = Tweet.objects.get(texto=texto, usuario_id_usuario=u)
    # instancia de la clase Hasstagtweet
    hastwe = TweetHashtag()
    hastwe.id_tweet_hashtag
    hastwe.hashtag_id_hashtag = idHash
    hastwe.tweet_id_tweet = idTweet
    hastwe.save()
    return True
