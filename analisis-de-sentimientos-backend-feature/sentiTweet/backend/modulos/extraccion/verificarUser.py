from tweepy import OAuthHandler
from tweepy import API
from ..APItwitter.credencial import credenciales

# llamar al metodo credenciales donde retorna los valores de las credenciales
consumer_key, consumer_secret, access_token, access_token_secret = credenciales()


def validarUsuario(usuario):
    try:
        if usuario[0] == "@":
            auth = OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
            api = API(auth)
            user = api.get_user(screen_name=usuario[1:])
            valor = True
        else:
            valor = False
    except:
        valor = False
    return valor


def validarHashtag(Hashtag):
    if Hashtag[0] == "#":
        valor = True
    else:
        valor = False
    return valor
