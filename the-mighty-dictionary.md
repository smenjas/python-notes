# The Mighty Dictionary

Brandon Craig Rhodes
PyCon 2010 Atlanta
https://www.youtube.com/watch?v=C4Kc8xzcA68

---

Q: How can Python lists access every one of their items with equal speed?

A: Python lists use segments of RAM and RAM acts like a Python list!
- RAM is a vast array
- Addressed by sequential integers
- Its first address is zero!
- Easy to implement a list atop memory

# The Dictionary
Uses keys instead of indexes and keys can be almost anything (as long as
they are immutable).

How can we turn the keys dictionaries use into indexes that reach memory
quickly?

# The Three Rules
1. A dictionary is really a list
2. Keys are hashed to produce indexes.
3. If at first you don't succeed, try, try again.

Python lets you see hashing in action through the hash() builtin
```python
for key in 'Monty', 3.14159, (1, 3, 5):
    print(hash(key)), key
```

Quite similar values often have very different hashes.
```python
for key in 'Monty', 'Money':
    print(hash(key)), key
```

Hashes look crazy, but the same value always returns the same hash!

# Key and Indexes
To build an index, Python uses the bottom n bits of the hash.

# Consequence #1
Dictionaries tend to return their contents in a crazy order.

# Collision
When two keys in a dictionary want the same slot.

# Consequence #2
Because collisions move keys away from their natural hash values, key order
is quite sensitive to dictionary history.

# The same yet different
Although these two dictionaries are considered equal, their different
histories put their keys in a different order.
```python
d = {'smtp': 21, 'dict': 2628, 'svn': 3690, 'ircd': 6667, 'zope': 9673}
e = {'ircd': 6667, 'zope': 9673, 'smtp': 21, 'dict': 2628, 'svn': 3690}
d == e # True
d.keys() # ['svn', 'dict', 'zope', 'smtp', 'ircd']
e.keys() # ['ircd', 'zope', 'smtp', 'svn', 'dict']
```

# Consequence #3
The lookup algorithm is actually more complicated than "hash, truncate, look".
It's more like "until you find an empty slot, keep looking, it could be here
somewhere!"

# Stupid Dictionary Trick #1
Because integers hash as themselves, we can create unlimited collisions!
```python
threes = {3: 1, 3+8: 2, 3+16: 3, 3+24: 4, 3+32: 5}
```

# Consequence #5
When deleting a key, you need to leave "dummy" keys.
```python
del d['smtp']
```

# Dicts refuse to get full
To keep collisions rare, dicts resize when only 2/3 full.
When < 50k entries, size x4
When > 50k entries size x2

Let's watch a dictionary in action against words pulled from the standard
dictionary.
```python
wordfile = open('/usr/share/dict/words')
text = wordfile.read()
words = [ w for w in text.split()
    if w == w.lower() and len(w) < 6 ]
print(words)

d = dict.fromkeys(words[:5])
# collision rate 40% but now 2/3 full, on the verge of resizing.

d['abash'] = None
# Resizes x4 to 32, collision rate drops to 0%

d = dict.fromkeys(words[:21])
# 2/3 full again, collision rate 29%

d['abode'] = None
# Resizes x4 to 128, collision rate drops to 9%

d = dict.fromkeys(words[:85])
# 2/3 full again, collision rate 33%
```
Life cycle as dictionary fills: gradually more crowded as keys are added,
then suddenly less as dict resizes.

# Consequence #6
Average dictionary performance is excellent.

A dictionary of common words:
```python
wordfile = open('/usr/share/dict/words')
words = wordfile.read().split()[:1365]
words = [ w for w in text.split()
    if w == w.lower() and len(w) < 6 ]
print(words)
```

# Consequence #7
Because of reszing, a dictionary can completely reorder during an otherwise
innocent insert.
```python
d = {'Double': 1, 'double': 2, 'toil': 3, 'and': 4, 'trouble': 5}
d.keys() # ['toil', 'Double', 'and', 'trouble', 'double']
d['fire'] = 6
d.keys() # ['and', 'fire', 'Double', 'double', 'toil', 'trouble']
```

# Consequence #8
Because an insert can radically reorder a dictionary, key insertion is
prohibited during iteration.
```python
d = {'Double': 1, 'double': 2, 'toil': 3, 'and': 4, 'trouble': 5}
for key in d:
    d['fire'] = 6
```
The above code results in a "RuntimeError: dictionary changed size during
iteration."

# Take-away #1
Hopefully "the rules" now make a bit more sense and seem less arbitrary.
- Don't rely on order.
- Don't insert while iterating.
- Can't have mutable keys.

# Take-away #2
Dictionaries trade space for time.  If you need more space, there are
alternatives.
- Tuples or namedtuples (Python 2.6)
- Give classes __slots__

# Take-away #3
If your class needs its own __hash__() method you now know how hashes
should behave.
- Scatter bits like crazy
- Equal instances must have equal hashes
- Must also implement __eq__() method
- Make hash and equality quick!
You can often get away with ^ xor'ing the hashes of your instance
variables.

# Hashing your own classes
```python
class Point(object):
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, p):
        return self.x == p.x and self.y == p.y

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)
```

# Take-away #4
Equal values should have equal hashes regardless of their type!
```python
hash(9) # 9
hash(9.0) # 9
hash(complex(9, 0)) # 9
```
All values that can represent an integer, use the same hash as the integer.

May your hashes be unique, your hash tables never full, and may your keys
rarely collide.

---

# Q&A

Q1: Do dictionaries resize themselves back down as entries are deleted?
A1: No they are only resized upwards on insert.  Copy data into a new one
    to reduce memory usage.

Q2: Does a set work the same as a dictionary?
A2: Yes. A set is a dictionary without storage for the value.

Q3: What if there is a true hash collision, where two different keys return
    the same hash value?
A3: After comparing the hashes, Python will compare the keys, and look for
    another slot.

Q4: Is there a way to preallocate a large dictionary?
A4: In C it's possible, but I don't know how to do it in Python.

Q5: Is it true that every time the hash table is resized, it forces the keys
    to reorder?
A6: In general yes, but you could contrive an example where that wouldn't
    happen because of the next bits taken into account don't affect the order.

Q5: Is it an expensive operation to do the reordering?
A6: It's like copying into a new dictionary.  It's a malloc of new memory.
    It has to do an insert of every entry.  The expense of the reordering on
    average costs nothing.  It just makes those particular moments expensive,
    but there are so many inserts that are free, that on average it's not
    time you need to worry about.

---

# My Notes

# Python Lists
In Python, lists are contiguous segments of memory, so they are very fast.
The indexing matches the way memory is indexed.

# Python Dictionaries.
Dictionaries are just lists, where the index relates to a hash function.

A hash table in contiguous memory, containing 8 rows by default, with an
index, a hash, the key, and the value.

# Hashing
Integers hash to themselves.  Anything else has a hash computed.

First, an 8 element list is created.  By default, the last 3 bits of the
key's hash corresponds to the index.

If there's a collision, the algorithm uses
the highest bits to find another empty slot.  This continues until a slot
is found, up to 16 times in the worst case.  On average, an element can
be found in less than 2 tries.  Finding an element in the worst case, at
16 tries, only takes 1.7x longer than the best case.  Retries are cheap.

When the dictionary is 2/3 full, it grows.  If it's < 50k elements, it
grows by 4x.  If it's > 50k elements, it grows by 2x.  When the dictionary
grows, all the elements are reindexed, changing their order.  This is why
you cannot add to a dictionary while using an iterator.

A dictionary's order depends on the order in which the elements were added.

This code shows the first 9 quadruplings:
```
$ python3
Python 3.7.3 (default, Nov 15 2019, 04:04:52)
[Clang 11.0.0 (clang-1100.0.33.16)] on darwin
Type "help", "copyright", "credits" or "license" for more information.
>>> for i in range(1, 10):
...     bits = (2 * i) + 1
...     size = 2 ** bits
...     print(str(bits) + " " + str(size))
...
3 8
5 32
7 128
9 512
11 2048
13 8192
15 32768
17 131072
19 524288
```

A dictionary only grows, it will not shrink when you delete entries.  To
shrink it, you must copy the keys and values into a new dictionary.

When you delete an entry that beat other entries to that slot, Python
holds that slot with a dummy record, so the other entries can be found.
New entries can overwrite the dummy record.

# Space & Time
A dictionary trades off memory space against processing time.  By storing
data sparesely, collisions are uncommon, making lookups fast on average.

Caching is another example where we can trade off space against time.  By
allocating memory to caching, we avoid having to regenerate the output each
time.

# Sets
A set is just a dictionary without storage for the values.

# Examples
```python
protocols = {
    'ftp': 21,
    'www': 80,
    'smtp': 25,
    'ssh': 22,
    'time': 37,
    'dict': 2628,
    'svn': 3690,
    'ircd': 6667,
    'zope': 9673}
```
