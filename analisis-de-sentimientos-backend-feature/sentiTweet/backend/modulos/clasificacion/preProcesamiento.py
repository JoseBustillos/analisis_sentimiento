from nltk.corpus import stopwords
from nltk.tokenize import RegexpTokenizer
tokenizer = RegexpTokenizer(r'\w+')
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
import re
from textblob import TextBlob
# stemming
porter = PorterStemmer()
# lema
lemmatizer = WordNetLemmatizer()
import emoji

def cleanText(dato):
    c=[]
    # transformar emoticones a string
    datos = emoji.demojize(dato, delimiters=(" ", " "))
    # eliminar enlaces, eliminar hastag tranformar a minusculas
    tr = re.sub('http://\S+|https://\S+|#\S+|&\S+|{\S+|@\S+|RT|_\S+', '', datos).lower()
    v = tokenizer.tokenize(tr)
    # ciclo for para lematizacion
    for i in range(0,len(v)):
        c.append(lemmatizer.lemmatize(v[i]))
    # trabajamos con las palabras de parada registradas en el corpus de nltk en idioma español
    stops = set(stopwords.words('spanish'))
    # eliminamos las palabras de parada del texto
    words = [w for w in c if not w in stops]
    # retornamos el texto con todo el proceso de PNL
    blob = TextBlob(" ".join(words))
    # traduccion de español a ingles
    ingles = blob.translate(to='en')
    return (ingles)
