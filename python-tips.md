# Python Tips

## Use isinstance(), not type()
type() only tells you the name of the class lowest in the hierarchy.
isinstance() tells you whether the object inherits from the given class, so
it works for child classes.

## List, set, and dictionary comprehensions
```python
my_list = []
for i in range(4):
    my_list.append(i)

my_list = [i for i in range(4)]

my_dict = []
for i in range(4):
    my_dict.append(i)

names = ['Alice', 'Bob', 'Claire']
aliases = ['Angel', 'Bobo', 'Clack']
my_dict = {name: alias for name, alias in zip(names, aliases)}

my_set = set([i for i in range(4)])
```

## Generators
```python
for i in range(4):
    yield i

my_generator = (i for i in range(4))
```

## Iterators
Iterators are objects with __iter__() and __next__() methods.

The itertools module helps you efficiently loop through iterables.

```python
import itertools

counter = itertools.count()
```

## Web Scraping
Beautiful Soup makes it easy to parse HTML.

```bash
pip install beautifulsoup4
pip install lxml
pip install html5lib
pip install requests
```
```python
from bs4 import BeautifulSoup
import requests

with open('example.html') as html_file:
    soup = BeautifulSoup(html_file, 'lxml')

print(soup.prettify())

match = soup.title
print(match)
```
