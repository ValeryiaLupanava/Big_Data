Привет, Галина!

```python
import numpy as np
vocabulary = ("Apache", "Spark", "Hadoop")
numbers = np.random.randint(10, size=10000)
words = np.random.choice(vocabulary, size=10000)
collection = zip(numbers, words)
```
Старайся для code review убирать весь не используемый код. Просто не всегда понятно относится это к задаче или нет.

```python
ratings = myid.flatMap(lambda x: x[2].split())
res = ratings.countByValue()
my_sortedres = collections.OrderedDict(sorted(res.items()))
hist_film=[]
for x,y in my_sortedres.items():
    hist_film.append(y)
```

Помни про принцип DRY - Don't Repeat Yourself

В остальном очень локаничное и красивое решение задачи.