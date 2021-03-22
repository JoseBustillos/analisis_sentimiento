from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import Tweets_detail
from .views import Usuario_list
from .views import Dataconsulta_list
from .views import sentimientoHashtag
from .views import sentimientoTweet
from .views import usuarioTweet
from .views import sentim

urlpatterns = [
    path('usuario/', Usuario_list),
    path('tweets/<str:tweet>/', Tweets_detail),
    path('data/', Dataconsulta_list),
    path('hashtag/<str:senti>/<str:hashtag>/<str:tweet>', sentimientoHashtag),
    path('tweets/<str:senti>/<str:tweet>', sentimientoTweet),
    path('usuarios/<int:usuario>/<str:tweet>/', usuarioTweet),
    path('senti/', sentim)
]
urlpatterns = format_suffix_patterns(urlpatterns)
