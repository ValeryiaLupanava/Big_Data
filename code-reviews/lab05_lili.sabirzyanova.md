Очень понравилась решение из за наглядности.
Жалко что не увидела функций перевода и анализ текстов по heatmap было бы очень интересно посмотреть и на это.

В замечаниях всякие мелочи

```python
import pandas as pd
import numpy as np
import re
import pymorphy2
import gensim
import os
import nltk
import json


from sklearn.metrics.pairwise import cosine_similarity
from nltk.stem import WordNetLemmatizer
from pymystem3 import Mystem
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from bs4 import BeautifulSoup
from pymystem3 import Mystem
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import pairwise_distances
import pymorphy2
from tqdm import tqdm_notebook as tqdm
from matplotlib import pyplot as plt
from json import JSONEncoder

pathBase = '/data/share/lab05data/'
```
Тут есть лишнии импорты. Это конечно же болезнь Jupyter, потому что IDE такие вещи показывает сразу


```python
# очиска текстов известной тематики
for i in range(len(dfText)):
    dfText.iloc[i].text = textBS(dfText.iloc[i].text)
```

```python
# формируем общий массив текстов
texts = []
for i in range(len(dfText)):
    texts.append(dfText.iloc[i].text)
                            
len(texts)
```
Где то есть инлайнеры, а где то код такой. Итеррироваться по датафрейму очень легко через iterrows()
