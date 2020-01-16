# Python Iterables
This covers Python's [built in iterable data types](https://docs.python.org/3/library/stdtypes.html):
- Lists
- Tuples
- Dictionaries
- Sets
Also see Python's standard library [collections](https://docs.python.org/3/library/collections.html).

## Lists
- Lists are ordered collections of values, indexed starting at zero.
- Lists are mutable. You can change their contents and their order.
- Lists can contain any data type.
- Lists have a sort method, that reorders them in place.
- Lists are contiguous memory allocations, stored just like the list.
```python3
my_list = list()
my_list = []
my_list.sort()
```

## Tuples
- Tuples are ordered collections of values, indexed starting at zero.
- Tuples are immutable. You cannot change their contents or their order.
- Tuples can contain any other data type.
- Tuples can contain lists. The list entries can change, but not the address.
- Tuples don't have a sort method. Use sorted(), to copy into a list.
```python3
my_tuple = tuple()
my_tuple = ()
my_tuple = 0,
my_sorted_list = sorted(my_tuple)
```

## Dictionaries
- Dictionaries are collections of keys mapped to values, indexed by hash.
- Dictionary order is based on history, and changes when the dictionary grows.
- Dictionary keys must be immutable: numbers, strings, and some tuples.
- Dictionary keys are unique, you cannot have duplicates.
- Dictionary values can be any data type.
- Dictionaries don't have a sort method. Use sorted(), to copy into a list.
- Dictionaries are implemented using a hash map/table.
```python3
my_dict = dict()
my_dict = {}
my_sorted_dict = sorted(my_dict)
```

## Sets
- Sets are dictionaries without values.
- Set keys are unique, you cannot have duplicates.
```python3
my_set = set()
my_set = {0} # Empty braces create a dictionary.
my_sorted_set = sorted(my_set)
unique_entries = set(my_list) # Easy way to remove duplicates.
```
