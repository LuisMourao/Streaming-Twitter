
# coding: utf-8

# In[ ]:


#Pesquisa tweets sobre um candidato em específico

import oauth2 #Biblioteca utilizada para autenticar a aplicação
import json #Utilizada para converter os arquivos no formato JSON
import pandas as pd #Utilizada na fase de testes do código, para visualizar e analisar as listas de palavras
import time #Controle dos tempos de execução e rate de acesso
from nltk.corpus import stopwords #utilizada para eliminar preposiçoes e pontuações 
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud #Responsável pela formatação do mapa de palavras
import matplotlib.pyplot as plt #Usada para plotar o mapa
import re #Retirar links 

Consumer_Key = 'eXxQB87RKtRyV6u4UOS9byFpM' 

Consumer_Secret = 'p6cav59spm3CKUNFJCUbrbcSJg0PK0EeYTjhQViRjnzswwJYsN'

Access_Token = '992218255375953922-kjB543QT8tDKhgTmNlHHpOx1NxMqs06'

AccessToken_Secret = 'CKAX7SMhSOZYdMPAuEGtik2XUfjEdtf3ayuk3Vebqyw5X'

consumer = oauth2.Consumer(Consumer_Key,Consumer_Secret)

token = oauth2.Token(Access_Token,AccessToken_Secret) #autenticação do acesso

cliente = oauth2.Client(consumer,token)


aux = 0 #indice do tweet
comp = str
lista = [] #lista que recebe o campo de texto dos tweets

pattern = r"http\S+"#utilizada para retirar os links

# loop para exibir e salvar em lista todos os tweets em um espaço de tempo

for j in range(0,40): #numero de loops até terminar a pesquisa
    request = cliente.request('https://api.twitter.com/1.1/search/tweets.json?q=bolsonaro&lang=pt&count=20') #20 tweets por requisição
    requestJ = json.loads(request[1].decode())
    time.sleep(0.5)
    if comp != requestJ['statuses'][0]['text']:
        for i in range(0,len(requestJ['statuses'])): 
            #if len(requestJ['statuses'][len(requestJ['statuses'])-1-i]['text']) < 139:
            print(aux)
            aux +=1
            print (requestJ['statuses'][len(requestJ['statuses'])-1-i]['created_at'])
            print (requestJ['statuses'][len(requestJ['statuses'])-1-i]['text'])
            lista.append(requestJ['statuses'][len(requestJ['statuses'])-1-i]['text'])
            comp = requestJ['statuses'][len(requestJ['statuses'])-1-i]['text']
            time.sleep(2)
    print('novoBLOCO')
    

for i in range(0,len(lista)): 
    lista[i] = re.sub(pattern,"",lista[i])
    
stop_words = set(stopwords.words('portuguese'))

lista2 = []

for i in lista: # Filtra as palavras, retirando preposições e etc.
    word_tokens = word_tokenize(i)
    filtered_sentence = [w for w in word_tokens if not w in stop_words]
    filtered_sentence = []

    for w in word_tokens:
        if w not in stop_words:
            filtered_sentence.append(w)

    lista2.append(filtered_sentence)
    
lst = []
for i in lista2:
    for j in i:
        if len(j) > 2:
            lst.append(j)

# Gera uma string unica com todas os tweets
            
a = ''
for i in lst:
    a = a + ' ' + i 


# Finalmente utilizando gera-se o mapa de palavras
    
a = a.lower()
text = a
wordcloud = WordCloud(max_font_size=100,width = 1520, height = 535).generate(text)
plt.figure(figsize=(16,9))
plt.imshow(wordcloud)
plt.axis("off")
plt.show()    

