from textblob import TextBlob
from textblob.sentiments import NaiveBayesAnalyzer
# al momento de obtener la polaridad se da rangos para asignar
# el tipo de clasificacion del tweet
def senti(text):
    analysis2 = TextBlob(str(text), analyzer=NaiveBayesAnalyzer())
    if analysis2.sentiment[0] == 'pos' :
        return ('Positivo')
    elif analysis2.sentiment[0]  == 'neg' :
        return ('Negativo')