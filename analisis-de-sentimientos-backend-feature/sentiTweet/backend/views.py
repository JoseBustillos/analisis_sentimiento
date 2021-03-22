from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse, JsonResponse
from django.db.models import F
from django.db.models import Count
from rest_framework.parsers import JSONParser
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response
import threading

from .models import Usuario
from .models import Dataconsulta
from .models import Tweet
from .models import TweetHashtag
from .serializer import UsuarioSerializer
from .serializer import DataconsultaSerializer
from .modulos.extraccion.verificarUser import validarUsuario
from .modulos.extraccion.verificarUser import validarHashtag
from .modulos.extraccion.obtenerData import extraccion
from .modulos.notificacion.reputacionOnline import reputacion

"""
    API endpoint que permite ver o editar
"""


@csrf_exempt
def Usuario_list(request):
    """
    Enumere todos los usuarios del código o cree un nuevo fragmento.
    """
    if request.method == "GET":
        usuario = Usuario.objects.all()
        serializer = UsuarioSerializer(usuario, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == "POST":
        data = JSONParser().parse(request)
        serializer = UsuarioSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


@api_view(["GET"])
def Tweets_detail(request, tweet, format=None):
    if request.method == "GET":
        # consultar tweets donde contengan dicha data consulta
        dato = TweetHashtag.objects.filter(tweet_id_tweet__texto__icontains=tweet)
        # consultar el sentimiento hashtag
        hashtag = dato.values("tweet_id_tweet__sentimiento_id_sentimiento__sentimiento")
        # contar sentimiento hashtag y cambiar nombre de valores
        cuentaHash = hashtag.annotate(
            total=Count("tweet_id_tweet__sentimiento_id_sentimiento__sentimiento"),
            hashtag=F("hashtag_id_hashtag__hashtag"),
            sentimiento=F("tweet_id_tweet__sentimiento_id_sentimiento__sentimiento"),
        )
        # escoger las columnas
        sentiHash = cuentaHash.values("total", "hashtag", "sentimiento")
        # escoger los 10 primeros hashtag en base a los sentimientos
        sentiHash = sentiHash.order_by("-total")[:10]
        # consultar los tweets con los sentimientos
        tweetSenti = dato.values(
            "tweet_id_tweet__sentimiento_id_sentimiento__sentimiento"
        )
        # contar hashtag sentimientos
        tweetSenti = tweetSenti.annotate(
            sentimiento=F("tweet_id_tweet__sentimiento_id_sentimiento__sentimiento"),
            total=Count("tweet_id_tweet__sentimiento_id_sentimiento__sentimiento"),
        )
        tweetSenti = tweetSenti.values("sentimiento", "total")
        # obtener cantidad de tweets negativos y positivos
        post = 0
        negt = 0
        print(len(tweetSenti))
        for i in range(0, len(list(tweetSenti))):
            print(tweetSenti[i])
            if tweetSenti[i]["sentimiento"] == "Positivo":
                post = tweetSenti[i]["total"]
            elif tweetSenti[i]["sentimiento"] == "Negativo":
                negt = tweetSenti[i]["total"]

        # total de tweets consultados
        total = negt + post
        # metodo para calcular el nivel de recomendacion enviando la cantidad de tweets positivos y negativos
        # retorna el valor de porccentaje de cada uno positivo - negativo
        pos, neg = reputacion(post, negt)

        # cambios de nombre de los campos
        dato3 = dato.annotate(
            usuario=F("tweet_id_tweet__usuario_id_usuario__nombre"),
            seguidores=F("tweet_id_tweet__usuario_id_usuario__numseguidor"),
            imagen=F("tweet_id_tweet__usuario_id_usuario__imgusuario"),
            verificado=F("tweet_id_tweet__usuario_id_usuario__verificado"),
            url=F("tweet_id_tweet__usuario_id_usuario__urlusuario"),
            idUser=F("tweet_id_tweet__usuario_id_usuario__id_usuario"),
        ).distinct()
        # obtenmos los datos necesarios
        dato3 = dato3.values(
            "usuario", "seguidores", "imagen", "verificado", "url", "idUser"
        )
        # ordenamos lista de usuario de forma decendente en base a la cantidad de sequidores
        # y escojemos los 20 primeros
        dato3 = dato3.order_by("-seguidores")[:10]
        # construccion del diccionario para ser consumido por el front end
        dict = {
            "usuarios": dato3,
            "hastag": sentiHash,
            "totalTweet": total,
            "reputacion": {"posPorcentaje": pos, "negPorcentaje": neg},
            "posTotal": post,
            "negTotal": negt,
        }
        return Response(dict)


@api_view(["GET"])
def sentimientoHashtag(self, senti, hashtag, tweet, format=None):
    # datos de entrada el hashtag y el sentimeinto consulta
    # construccion del hashtag
    hasht = "#" + hashtag + " "
    # consultamos los tweets que poseen dicho hashtag y el sentimiento de consulta
    dato = (
        Tweet.objects.filter(
            texto__contains=hasht.replace(" ", ""),
            sentimiento_id_sentimiento__sentimiento=senti,
        )
        .filter(texto__contains=tweet.replace(".json", ""))
        .distinct()
    )
    # obtener los tweets que no son retweet
    dato1 = dato.exclude(texto__contains="RT @").values()
    # obtener tweets originales
    dato2 = dato.filter(texto__icontains="RT @").values()
    dato1 = dato1.annotate(
        sentimiento=F("sentimiento_id_sentimiento__sentimiento"),
        usuario=F("usuario_id_usuario_id__imgusuario"),
        nombre=F("usuario_id_usuario_id__nombre"),
        verificado=F("usuario_id_usuario_id__verificado"),
    )
    dato1 = dato1.values(
        "texto",
        "sentimiento",
        "url",
        "numlikes",
        "numcitado",
        "numretweet",
        "numrespuesta",
        "usuario",
        "nombre",
        "verificado",
    )
    dato2 = dato2.annotate(
        sentimiento=F("sentimiento_id_sentimiento__sentimiento"),
        usuario=F("usuario_id_usuario_id__imgusuario"),
        nombre=F("usuario_id_usuario_id__nombre"),
        verificado=F("usuario_id_usuario_id__verificado"),
    )
    dato2 = dato2.values(
        "texto",
        "sentimiento",
        "url",
        "numlikes",
        "numcitado",
        "numretweet",
        "numrespuesta",
        "usuario",
        "nombre",
        "verificado",
    )
    data = {"original": dato1, "ret": dato2}
    return Response(data)


@api_view(["GET"])
def sentimientoTweet(self, senti, tweet, format=None):
    dato = TweetHashtag.objects.filter(
        tweet_id_tweet__texto__icontains=tweet.replace(".json", "")
    )
    tweetSenti = (
        dato.values("tweet_id_tweet__sentimiento_id_sentimiento__sentimiento")
        .filter(tweet_id_tweet__sentimiento_id_sentimiento__sentimiento=senti)
        .distinct()
    )
    tweetSenti = tweetSenti.values("tweet_id_tweet__texto")
    tweetSenti = tweetSenti.annotate(
        texto=F("tweet_id_tweet__texto"),
        url=F("tweet_id_tweet__url"),
        numlikes=F("tweet_id_tweet__numlikes"),
        numcitado=F("tweet_id_tweet__numcitado"),
        numretweet=F("tweet_id_tweet__numretweet"),
        numrespuesta=F("tweet_id_tweet__numrespuesta"),
        nombre=F("tweet_id_tweet__usuario_id_usuario__nombre"),
        usuario=F("tweet_id_tweet__usuario_id_usuario__imgusuario"),
        verificado=F("tweet_id_tweet__usuario_id_usuario__verificado"),
        fecha=F("tweet_id_tweet__fecha"),
    )
    tweetSenti1 = tweetSenti.exclude(tweet_id_tweet__texto__contains="RT @").values()
    tweetSenti1 = tweetSenti1.values(
        "texto",
        "url",
        "numlikes",
        "numcitado",
        "numretweet",
        "numrespuesta",
        "nombre",
        "usuario",
        "verificado",
        "fecha",
    )
    tweetSenti1 = tweetSenti1.order_by("-fecha")[:20]
    tweetSenti2 = tweetSenti.filter(tweet_id_tweet__texto__contains="RT @").values()
    tweetSenti2 = tweetSenti2.values(
        "texto",
        "url",
        "numlikes",
        "numcitado",
        "numretweet",
        "numrespuesta",
        "nombre",
        "usuario",
        "verificado",
        "fecha",
    )
    tweetSenti2 = tweetSenti2.order_by("-fecha")[:20]
    data = {"original": tweetSenti1, "ret": tweetSenti2}
    return Response(data)


@api_view(["GET"])
def usuarioTweet(self, usuario, tweet, format=None):
    dato = TweetHashtag.objects.filter(
        tweet_id_tweet__texto__icontains=tweet.replace(".json", "")
    ).filter(tweet_id_tweet__usuario_id_usuario__id_usuario=usuario)
    tweet = dato.annotate(
        tweet=F("tweet_id_tweet__texto"), url=F("tweet_id_tweet__url")
    )
    tweet = tweet.values("tweet", "url")
    return Response(tweet)


def bien():
    return Response(status=status.HTTP_200_OK)


@api_view(["GET", "POST"])
def Dataconsulta_list(request, format=None):
    if request.method == "GET":
        dato = Dataconsulta.objects.all()
        serializer = DataconsultaSerializer(dato, many=True)
        return Response(serializer.data)
    elif request.method == "POST":
        serializer = DataconsultaSerializer(data=request.data)
        if serializer.is_valid():
            dataConsulta = request.data["data"]
            # condicion para funciones de usuario validado
            if len(dataConsulta) == 0:
                content1 = {"error": "Ingresar data de consulta"}
                return Response(content1)
            else:
                # validador de usuario
                validado = validarUsuario(dataConsulta)
                # validar hashtag
                validadoH = validarHashtag(dataConsulta)
                if validado == True or validadoH == True:
                    # validador si el usuario o hashtag se encuentra almacenado
                    if Dataconsulta.objects.filter(data=dataConsulta).exists():
                        pass
                    else:
                        # crea bojeto Dataconsulta
                        datC = Dataconsulta(data=dataConsulta)
                        # almacena en la base de datos
                        datC.save()
                    # metodo para la extracción de twittes
                    # hilos codigo recurrente
                    # hilos en python
                    t1 = threading.Thread(
                        name="hilo1", target=extraccion, args=(dataConsulta,)
                    )
                    t2 = threading.Thread(name="hilo2", target=bien)
                    t1.start()
                    t2.start()
                else:
                    content = {"error": "Dato ingresado es incorrecto"}
                    return Response(content)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response({"status": "details"}, status=status.HTTP_400_BAD_REQUEST)


def sentim(request):
    # valor = cleanText("RT @utplradio: Este jueves en #ForoAbierto nuestro tema es: Acreditación universitaria en el Ecuador junto a @NikolayAguirre rector de @UN…")
    # print(valor)
    test = "“Mañana cumplimos 44 años de Educación a Distancia”. 🎉📚 La @utpl ratifica su liderazgo en Educación Superior. #UTPLFuturo👌🏻 https://t.co/fts7OLDLA1"
    print(test.lower())
    print("utpl" in test.lower())

    return HttpResponse("bien")
