
# Лабораторная работа 5
# !!! Привет! Буду начинать свои комментарии "# !!!"

```python
import os
from bs4 import BeautifulSoup
import re
from sklearn.feature_extraction.text import TfidfVectorizer
import json
import numpy as np
import math
import json
```

### 1. Загрузка данных


```python
path = '/data/share/lab05data/'
```


```python
# из личного кабинета
my_test_id = [514, 1539, 3588, 2570, 3587, 2575, 174, 1553, 3603, 2583, 538, 3612, 30, 2079, 2592, 2081, 2225, 548, 2603, 
              55, 2618, 572, 2621, 62, 3139, 2628, 3141, 1098, 587, 588, 589, 2639, 3665, 85, 1622, 1111, 1419, 1632, 1634, 
              1131, 2158, 1647, 624, 2579, 3188, 2166, 2682, 3708, 1387, 3712, 3265, 2692, 133, 3719, 2185, 3722, 3723, 3213, 
              144, 3730, 3223, 2712, 153, 3745, 1188, 678, 3239, 3699, 1711, 984, 177, 3763, 2232, 1211, 701, 1726, 3264, 705, 
              3267, 712, 1225, 1228, 717, 3279, 1747, 1748, 3285, 2265, 293, 219, 3804, 1757, 2275, 1767, 1257, 748, 3795, 
              2174, 3827, 724, 245, 2809, 1274, 766, 257, 231, 3332, 1798, 2826, 3852, 3931, 2323, 1302, 1816, 1323, 800, 290, 
              2339, 1829, 2855, 3368, 299, 2350, 2863, 3378, 2355, 311, 312, 2361, 3901, 2187, 324, 3405, 3299, 3481, 3920, 
              337, 2389, 854, 343, 967, 347, 3420, 3426, 358, 2144, 2878, 1394, 1911, 888, 377, 383, 1920, 386, 3052, 2950, 
              903, 1929, 907, 1006, 913, 402, 2372, 917, 409, 2463, 1441, 2538, 421, 2982, 427, 429, 2480, 2010, 3508, 2485, 
              1439, 955, 3516, 455, 2504, 3020, 2028, 2006, 3544, 2469, 1500, 1501, 2531, 3580, 2026, 3564, 1517, 2030, 2544, 
              3576, 2901, 2043, 1020, 598]
```


```python
len(my_test_id)
```




    200




```python
# base читаем все
base_text = []
for filename in os.listdir(path):
    if filename.startswith("base"):
        with open(os.path.join(path, filename), encoding='utf-8') as file:
            text = file.read()
            base_text.append(text.lower())
```


```python
base_text[1]
```




    '<p>netcracker technology corp., a large software development company and one of the world’s most respected toms solutions (telecommunications operations and management solutions) companies, has an opening for:</p> \xa0 <p><strong>technical manager</strong><br /><br /><strong>responsibilities:</strong></p> \xa0 <ul> <li>managing a team of 3-8 or more developers;</li> <li>carrying out various development projects of the duration from 1 week up to several months through the full cycle starting from the requirements gathering and up to product implementation and documentation preparation;</li> <li>participating customer implementation projects;</li> <li>carrying out presales demonstration projects, resulting in presenting demonstrations basing on customer requirements.</li> </ul> <p><strong>qualification:</strong></p> <ul> <li>high technical degree;</li> <li>minimum of 3 years experience as a developer/lead developer;</li> <li>minimum of 2 years technical management experience;</li> <li>excellent knowledge of java, j2ee;</li> <li>very good technical english verbal/writing skills;</li> <li>successful experience in managing it projects;</li> <li>excellent communication and team building abilities;</li> <li>business-like presence and ability to interact professionally with customers;</li> <li>willingness to work as a lead java developer for the starting period;</li> <li>experience in working in telecommunications areas;</li> <li>excellent english language;</li> <li>ability to travel both within the country and abroad.</li> </ul> <p><strong>we offer:</strong></p> <ul> <li>opportunities for career development;</li> <li>opportunities to make business trips (europe, canada, usa, australia, etc);</li> <li>professional growth in the international business environment;</li> <li>medical insurance for employees;</li> <li>friendly atmosphere, sports activities and corporate events;</li> <li>salary will be discussed individually with the successful candidate.</li> </ul>'




```python
# тестовые тексты читаем только с нужными нам ID
test_text = []
for id_ in my_test_id:
    with open(os.path.join(path, "test_{}.txt".format(id_)), encoding='utf-8') as file:
        text = file.read()
        test_text.append(text.lower())
```


```python
test_text[1]
```




    '<p><strong>обязанности:</strong></p> <ul> <li>участие в качестве разработчика в проектах по разработке серверного программного обеспечения</li> </ul> <p><strong>требования:</strong></p> <ul> <li>хорошее знание c++, stl</li> <li>хорошее знание принципов ооп, паттернов проектирования</li> <li>знание стека tcp/ip, опыт написания сетевых приложений</li> <li>опыт разработки под linux/posix. уверенное владение bash и основными утилитами linux</li> <li>опыт многопоточного программирования</li> <li>технический английский язык</li> </ul> <p><strong>дополнительными преимуществами будут:</strong></p> <ul> <li>умение разбираться в чужом коде, производить рефакторинг и оптимизацию</li> <li>участие в разработке высоконагруженных приложений работающих в режиме «24х7»</li> <li>знание стека ss7, протоколов sctp, radius, sip, sigtran, camel, rtsp</li> <li>опыт работы с mysql, mongodb, redis</li> <li>знание cmake</li> <li>знание python</li> <li>знание boost, c++11</li> <li>опыт написания unit-тестов</li> </ul> <p> </p> <p><strong>условия:</strong></p> <ul> <li>полный рабочий день</li> <li>официальное трудоустройство, отпуск/больничные по тк рф</li> <li>гибкий график работы</li> <li>чай/кофе в офисе</li> <li>соц. пакет, обеды, бесплатная маршрутка от метро до офиса</li> <li>оплата 50% абонемента в фитнес клуб</li> <li>оплата парковочного места</li> </ul>'



### Почистим тексты от мусора

#  !!! Применение lower() здесь излишне, так как использовал данную функцию в предыдущем блоке, когда читал тексты
```python
clear_base_text = []
for text in base_text:
    text = BeautifulSoup(text).get_text()
    clear_base_text.append(text.lower())
     
clear_test_text = []
for text in test_text:
    text = BeautifulSoup(text).get_text()
    clear_test_text.append(text.lower())
```

    /opt/anaconda/envs/bd9/lib/python3.6/site-packages/bs4/__init__.py:181: UserWarning: No parser was explicitly specified, so I'm using the best available HTML parser for this system ("lxml"). This usually isn't a problem, but if you run this code on another system, or in a different virtual environment, it may use a different parser and behave differently.
    
    The code that caused this warning is on line 193 of the file /opt/anaconda/envs/bd9/lib/python3.6/runpy.py. To get rid of this warning, change code that looks like this:
    
     BeautifulSoup(YOUR_MARKUP})
    
    to this:
    
     BeautifulSoup(YOUR_MARKUP, "lxml")
    
      markup_type=markup_type))



```python
clear_base_text[1]
```




    'netcracker technology corp., a large software development company and one of the world’s most respected toms solutions (telecommunications operations and management solutions) companies, has an opening for: \xa0 technical managerresponsibilities: \xa0  managing a team of 3-8 or more developers; carrying out various development projects of the duration from 1 week up to several months through the full cycle starting from the requirements gathering and up to product implementation and documentation preparation; participating customer implementation projects; carrying out presales demonstration projects, resulting in presenting demonstrations basing on customer requirements.  qualification:  high technical degree; minimum of 3 years experience as a developer/lead developer; minimum of 2 years technical management experience; excellent knowledge of java, j2ee; very good technical english verbal/writing skills; successful experience in managing it projects; excellent communication and team building abilities; business-like presence and ability to interact professionally with customers; willingness to work as a lead java developer for the starting period; experience in working in telecommunications areas; excellent english language; ability to travel both within the country and abroad.  we offer:  opportunities for career development; opportunities to make business trips (europe, canada, usa, australia, etc); professional growth in the international business environment; medical insurance for employees; friendly atmosphere, sports activities and corporate events; salary will be discussed individually with the successful candidate. '




```python
clear_test_text[1]
```




    'обязанности:  участие в качестве разработчика в проектах по разработке серверного программного обеспечения  требования:  хорошее знание c++, stl хорошее знание принципов ооп, паттернов проектирования знание стека tcp/ip, опыт написания сетевых приложений опыт разработки под linux/posix. уверенное владение bash и основными утилитами linux опыт многопоточного программирования технический английский язык  дополнительными преимуществами будут:  умение разбираться в чужом коде, производить рефакторинг и оптимизацию участие в разработке высоконагруженных приложений работающих в режиме «24х7» знание стека ss7, протоколов sctp, radius, sip, sigtran, camel, rtsp опыт работы с mysql, mongodb, redis знание cmake знание python знание boost, c++11 опыт написания unit-тестов    условия:  полный рабочий день официальное трудоустройство, отпуск/больничные по тк рф гибкий график работы чай/кофе в офисе соц. пакет, обеды, бесплатная маршрутка от метро до офиса оплата 50% абонемента в фитнес клуб оплата парковочного места '



### TF-IDF


```python
#Попробуем свой Tokenazer
import pymystem3
from pymystem3 import Mystem
#from nltk.stem import WordNetLemmatizer
#from nltk.corpus import wordnet
from nltk.tokenize import RegexpTokenizer
```


```python
m = Mystem()
#wordnet_lemmatizer = WordNetLemmatizer()
```

# !!! В репозитории в инструкции, как делать код ревью отмечали, что закомментированные блоки, лучше удалять!
# !!! Но я и сама про это забываю 

```python
#def text_to_wordlist(text):
#    text = re.sub('n\'t', ' not', text)
#    text = re.sub('[^a-zA-Zа-яА-Я]', ' ', text)
#    words = text.lower().split()
#    return words
```


```python
#prepared_base_text = []
#for item in clear_base_text:
#    new_item = text_to_wordlist(item)
#    lemm_mystem = [m.lemmatize(x)[0] for x in new_item]
#    tokens_stem = [wordnet_lemmatizer.lemmatize(x, pos=wordnet.VERB) for x in lemm_mystem]
#    prepared_base_text.append(tokens_stem)
```


```python
#prepared_test_text = []
#for item in clear_test_text:
#    new_item = text_to_wordlist(item)
#    lemm_mystem = [m.lemmatize(x)[0] for x in new_item]
#    tokens_stem = [wordnet_lemmatizer.lemmatize(x, pos=wordnet.VERB) for x in lemm_mystem]
#    prepared_test_text.append(tokens_stem)
```


```python
tokenizer = RegexpTokenizer('[A-Za-zА-Яа-яёЁ]+')
def my_tokenize(text):
    tokens = tokenizer.tokenize(text)
    for i in tokens:
        if len(i)>3:
            yield m.lemmatize(i)[0]
```


```python
stop_words_russia = ["c","а","алло","без","белый","близко","более","больше","большой","будем","будет","будете","будешь","будто",
              "буду","будут","будь","бы","бывает","бывь","был","была","были","было","быть","в","важная","важное","важные",
              "важный","вам","вами","вас","ваш","ваша","ваше","ваши","вверх","вдали","вдруг","ведь","везде","вернуться",
              "весь","вечер","взгляд","взять","вид","видел","видеть","вместе","вне","вниз","внизу","во","вода","война",
              "вокруг","вон","вообще","вопрос","восемнадцатый","восемнадцать","восемь","восьмой","вот","впрочем",
              "времени","время","все","все еще","всегда","всего","всем","всеми","всему","всех","всею","всю","всюду","вся",
              "всё","второй","вы","выйти","г","где","главный","глаз","говорил","говорит","говорить","год","года","году",
              "голова","голос","город","да","давать","давно","даже","далекий","далеко","дальше","даром","дать","два",
              "двадцатый","двадцать","две","двенадцатый","двенадцать","дверь","двух","девятнадцатый","девятнадцать",
              "девятый","девять","действительно","дел","делал","делать","делаю","дело","день","деньги","десятый",
              "десять","для","до","довольно","долго","должен","должно","должный","дом","дорога","друг","другая",
              "другие","других","друго","другое","другой","думать","душа","е","его","ее","ей","ему","если","есть","еще",
              "ещё","ею","её","ж","ждать","же","жена","женщина","жизнь","жить","за","занят","занята","занято","заняты",
              "затем","зато","зачем","здесь","земля","знать","значит","значить","и","иди","идти","из","или","им","имеет",
              "имел","именно","иметь","ими","имя","иногда","их","к","каждая","каждое","каждые","каждый","кажется","казаться",
              "как","какая","какой","кем","книга","когда","кого","ком","комната","кому","конец","конечно","которая",
              "которого","которой","которые","который","которых","кроме","кругом","кто","куда","лежать","лет","ли",
              "лицо","лишь","лучше","любить","люди","м","маленький","мало","мать","машина","между","меля","менее","меньше",
              "меня","место","миллионов","мимо","минута","мир","мира","мне","много","многочисленная","многочисленное",
              "многочисленные","многочисленный","мной","мною","мог","могу","могут","мож","может","может быть",'можно',"можхо",
              "мои","мой","мор","москва","мочь","моя","моё","мы","на","наверху","над","надо","назад","наиболее","найти",
              "наконец","нам","нами","народ","нас","начала","начать","наш","наша","наше","наши","не","него","недавно",
              "недалеко","нее","ней","некоторый","нельзя","нем","немного","нему","непрерывно","нередко","несколько","нет",
              "нею","неё","ни","нибудь","ниже","низко","никакой","никогда","никто","никуда","ним","ними","них","ничего",
              "ничто","но","новый","нога","ночь","ну","нужно","нужный","нх","о","об","оба","обычно","один","одиннадцатый",
              "одиннадцать","однажды","однако","одного","одной","оказаться","окно","около","он","она","они","оно","опять",
              "особенно","остаться","от","ответить","отец","откуда","отовсюду","отсюда","очень","первый","перед","писать",
              "плечо","по","под","подойди","подумать","пожалуйста","позже","пойти","пока","пол","получить","помнить",
              "понимать","понять","пор","пора","после","последний","посмотреть","посреди","потом","потому","почему",
              "почти","правда","прекрасно","при","про","просто","против","процентов","путь","пятнадцатый","пятнадцать",
              "пятый","пять","работа","работать","раз","разве","рано","раньше","ребенок","решить","россия","рука",
              "русский","ряд","рядом","с","с кем","сам","сама","сами","самим","самими","самих","само","самого","самой",
              "самом","самому","саму","самый","свет","свое","своего","своей","свои","своих","свой","свою","сделать","сеаой",
              "себе","себя","сегодня","седьмой","сейчас","семнадцатый","семнадцать","семь","сидеть","сила","сих","сказал",
              "сказала","сказать","сколько","слишком","слово","случай","смотреть","сначала","снова","со","собой",
              "собою","советский","совсем","спасибо","спросить","сразу","стал","старый","стать","стол","сторона",
              "стоять","страна","суть","считать","т","та","так","такая","также","таки","такие","такое","такой","там",
              "твои","твой","твоя","твоё","те","тебе","тебя","тем","теми","теперь","тех","то","тобой","тобою",
              "товарищ","тогда","того","тоже","только","том","тому","тот","тою","третий","три","тринадцатый",
              "тринадцать","ту","туда","тут","ты","тысяч","у","увидеть","уж","уже","улица","уметь","утро","хороший",
              "хорошо","хотел бы","хотеть","хоть","хотя","хочешь","час","часто","часть","чаще","чего","человек","чем",
              "чему","через","четвертый","четыре","четырнадцатый","четырнадцать","что","чтоб","чтобы","чуть",
              "шестнадцатый","шестнадцать","шестой","шесть","эта","эти","этим","этими","этих","это","этого","этой","этом",
              "этому","этот","эту","я","являюсь",'a','the','there','and','but','to','too','if','then']
```


```python
from nltk.corpus import stopwords 
from nltk.tokenize import word_tokenize 
stop_words_english = list(stopwords.words('english'))
```


```python
type(stop_words_english), type(stop_words_russia)
```



# !!! Не увидела блока, где приводишь к начальной форме, используешь lemmatizer в зависимости от языка

# !!! Не понятно, к чему относится следующая строчка?
    (list, list)




```python
vectorizer = TfidfVectorizer(token_pattern='[A-Za-zА-Яа-яёЁ]+',
                             stop_words = stop_words_russia + stop_words_english,
                             norm=None, 
                             smooth_idf=False,
                             tokenizer = my_tokenize)
```


```python
base = vectorizer.fit_transform(clear_base_text).toarray()
test = vectorizer.transform(clear_test_text).toarray()
```

косинусная мера: http://akorsa.ru/2017/01/vektornaya-model-i-kosinusnoe-shodstvo-cosine-similarity/

# Хорошо бы добавить больше комментариев и описаний функций

```python
def simmilarity (a, b):
    a = np.array(a)
    b = np.array(b)
    return sum(a*b)/math.sqrt(sum(a**2)*sum(b**2))
```


```python
score_matrix = []
for test_vector in test:
    score = sum([simmilarity(base_vector, test_vector) for base_vector in base])
    score_matrix.append(score)
```


```python
score_matrix[1:10]
```




    [3.3446550669975785,
     2.6543669137144725,
     2.6227812721900734,
     0.9538506353653254,
     3.1167859885018965,
     1.2993023373792156,
     0.9933846062405225,
     3.4665203349378153,
     2.446214742378762]




```python
sum(score_matrix), len(score_matrix)
```




    (416.58867801534524, 200)




```python
avg_threshold = sum(score_matrix)/len(score_matrix)
avg_threshold
```




    2.0829433900767262




```python
# разбиваем по кучкам 
defined = []
other = []
for i in range(len(my_test_id)):
    if score_matrix[i] >= avg_threshold: 
        defined.append(my_test_id[i])
    else: 
        other.append(my_test_id[i])
defined = sorted(defined)
other = sorted(other)
```


```python
final_result = {"defined": defined,
                "other": other}
```


```python
print(final_result)
```

    {'defined': [30, 55, 153, 219, 245, 257, 299, 324, 347, 358, 402, 421, 427, 429, 455, 514, 572, 589, 678, 701, 705, 712, 800, 854, 907, 955, 1098, 1188, 1211, 1225, 1228, 1274, 1387, 1517, 1539, 1622, 1632, 1647, 1726, 1747, 1748, 1757, 1767, 1816, 1920, 1929, 2006, 2026, 2030, 2043, 2081, 2144, 2158, 2166, 2185, 2275, 2350, 2355, 2504, 2531, 2570, 2575, 2583, 2592, 2621, 2628, 2639, 2692, 2809, 2826, 2855, 2863, 2950, 3020, 3139, 3141, 3188, 3213, 3223, 3239, 3267, 3285, 3332, 3368, 3405, 3426, 3516, 3544, 3588, 3603, 3612, 3708, 3712, 3719, 3723, 3730, 3745, 3763, 3804, 3901], 'other': [62, 85, 133, 144, 174, 177, 231, 290, 293, 311, 312, 337, 343, 377, 383, 386, 409, 538, 548, 587, 588, 598, 624, 717, 724, 748, 766, 888, 903, 913, 917, 967, 984, 1006, 1020, 1111, 1131, 1257, 1302, 1323, 1394, 1419, 1439, 1441, 1500, 1501, 1553, 1634, 1711, 1798, 1829, 1911, 2010, 2028, 2079, 2174, 2187, 2225, 2232, 2265, 2323, 2339, 2361, 2372, 2389, 2463, 2469, 2480, 2485, 2538, 2544, 2579, 2603, 2618, 2682, 2712, 2878, 2901, 2982, 3052, 3264, 3265, 3279, 3299, 3378, 3420, 3481, 3508, 3564, 3576, 3580, 3587, 3665, 3699, 3722, 3795, 3827, 3852, 3920, 3931]}



```python
with open("/data/home/alexander.dorofeyev/lab05.json", "w") as file:
    json.dump(final_result, file)
```
