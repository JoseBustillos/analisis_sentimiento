from tweepy.streaming import StreamListener
from tweepy import OAuthHandler, Stream
from urllib3.exceptions import ProtocolError
import sys
import json
from ..APItwitter.credencial import credenciales
from .convertirData import analizarJson

# llamar al metodo credenciales donde retorna los valores de las credenciales
consumer_key, consumer_secret, access_token, access_token_secret = credenciales()

# clase de tweepy para la extraccion de tweets
class StdOutListener(StreamListener):
    def on_data(self, data):
        # tweet obtenido de la API y convertido en formato JSON
        dia = json.loads(data)
        # obtener solo el texto de tweet
        age = dia.get("text")
        if age:
            analizarJson(dia)
        return True

    # imprimir error al conectarse con el API twitter
    def on_error(self, status):
        print(sys.exc_info()[0])


# metodo para la extracción de tweets mediante filtro de la palabra clave
def extraccion(palabra):
    listener = StdOutListener()
    # autenticacsion de usuario Twitter
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    twitterStream = Stream(auth, listener)
    # control de errores al protocolo de la API
    while True:
        try:
            # extraccion de tweets solo con palabras claves y en idioma español
            twitterStream.filter(track=[palabra], languages=["es"])
        except (ProtocolError, AttributeError):
            continue
