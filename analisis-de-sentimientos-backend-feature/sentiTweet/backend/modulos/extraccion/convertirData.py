from django.core.exceptions import ObjectDoesNotExist
from ..clasificacion.preProcesamiento import cleanText
from ..clasificacion.predecirPolaridad import senti
from ...models import Dataconsulta
from .peticionBD import *


def analizarJson(dia):
    d = list(Dataconsulta.objects.all().values("data"))
    for i in range(0, len(d)):
        try:
            estado = "original"
            try:
                print("actualizado")
                actualizarUsuario(dia, estado)
            except ObjectDoesNotExist:
                print("almacenado")
                almacenarUsuario(dia, estado)
            if dia["truncated"] == True:
                texto = dia["extended_tweet"]["full_text"]
            else:
                texto = dia["text"]
            try:
                print("actualizado")
                actualizarTweet(dia, estado, texto)
            except ObjectDoesNotExist:
                almacenarTweet(dia, estado, texto, senti(cleanText(texto)))
                asignarRetweet(dia, texto)
            if len(dia["entities"]["hashtags"]):
                hash = dia["entities"]["hashtags"]
                for ii in range(0, len(hash)):
                    try:
                        almacenarHashtag(dia, estado, texto, hash[i]["text"])
                    except ObjectDoesNotExist:
                        asignarHashtagTeet(dia, estado, texto, hash[i]["text"])
        except Exception:
            print(Exception)

        try:
            estado = "retweeted"
            try:
                print("actualizado")
                actualizarUsuario(dia, estado)
            except ObjectDoesNotExist:
                print("almacenado")
                almacenarUsuario(dia, estado)
            if dia["retweeted_status"]["truncated"] == True:
                texto = dia["retweeted_status"]["extended_tweet"]["full_text"]
            else:
                texto = dia["retweeted_status"]["text"]
            try:
                print("actualizado")
                actualizarTweet(dia, estado, texto)
            except ObjectDoesNotExist:
                almacenarTweet(dia, estado, texto, senti(cleanText(texto)))
                asignarRetweet(dia, texto)
            if len(dia["retweeted_status"]["entities"]["hashtags"]):
                hash = dia["retweeted_status"]["entities"]["hashtags"]
                for ii in range(0, len(hash)):
                    try:
                        almacenarHashtag(dia, estado, texto, hash[i]["text"])
                    except ObjectDoesNotExist:
                        asignarHashtagTeet(dia, estado, texto, hash[i]["text"])
        except Exception:
            print(Exception)

        try:
            estado = "quoted"
            try:
                print("actualizado")
                actualizarUsuario(dia, "quoted")
            except ObjectDoesNotExist:
                print("almacenado")
                almacenarUsuario(dia, "quoted")
            if dia["quoted_status"]["truncated"] == True:
                texto = dia["quoted_status"]["extended_tweet"]["full_text"]
            else:
                texto = dia["quoted_status"]["text"]
            try:
                print("actualizado")
                actualizarTweet(dia, estado, texto)
            except ObjectDoesNotExist:
                almacenarTweet(dia, estado, texto, senti(cleanText(texto)))
                print("asignado")
                asingarCita(dia, texto)
            if len(dia["quoted_status"]["entities"]["hashtags"]):
                hash = dia["quoted_status"]["entities"]["hashtags"]
                for iii in range(0, len(hash)):
                    try:
                        print("almacenado")
                        almacenarHashtag(dia, estado, texto, hash[i]["text"])
                    except ObjectDoesNotExist:
                        print("asignado")
                        asignarHashtagTeet(dia, estado, texto, hash[i]["text"])
        except Exception:
            print(Exception)
