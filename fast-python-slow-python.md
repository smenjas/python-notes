# [Fast Python, Slow Python](https://www.youtube.com/watch?v=7eeEf_rAJds)

Alex Gaynor
PyCon 2014 Montreal

A talk about 2 things:
- Performance
- Python
and the instersection of these.

What is performance?
Performance is specialization.

Integration vs. unit testing
Micro vs. macro benchmarks

What is Python?
Python is an abstract language, for which you can build different
machines, CPython is one of those machines.  Python isn't:
- Cython
- C
- Numba
- RPython

Dynamic languages are slow, supposedly.  Most of what you read in the
Dragon Book doesn't apply.

You can monkey patch anything.

Slow vs. Harder to optimize

Dynamic languages aren't hard to optimize.

What is PyPy?
PyPy is an implementation of Python.

I want to offer you guys a deal.
I said earlier that performance is specialization.
If you all specialize your code for the problems you're trying to solve,
I'll specialize the code you're writing for the machine it's executing on.
In other words, you choose good algorithms, and I'll make them run fast.
I hope that sounds like a fair deal.

What is specialization?
How can we specialize our code?

Let's talk about C.
It's basically a DSL for assembly.
```c
struct Point {
    double x;
    double y;
    double z;
}
```
```python
class Point(objet):
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

point = {
    "x": x,
    "y": y,
    "z": z,
}
```
A dictionary is not an object.
Classes are specialized, ditctionaries are only specialized at mapping.
```cpp
std::unordered_map<std::string, double> point;
point["x"] = x;
point["y"] = y;
point["z"] = z;
```
For a long time, there was no performance difference between dictionaries
and objects.
```python
if [hex, bytes, bytes_le, fields, int].count(None) != 4:
    raise TypeError('need exactly one argument')

if (
    (hex is None) + (bytes is None) + (bytes_le is None) +
    (fields is None) + (int is None)
) != 4:
    raise TypeError
```
```c
/* This is fast. */
char *data = malloc(1025);
while (true) {
    size_t n = read(fd, data, 1024);
    data[n] = '\0';
    char *start = data;
    while (start < data + n) {
        if (isspace(*start)) {
            break;
        }
        start++;
    }
    printf("%s\n", start);
}
```
```python
# This is slow.
while True:
    data = os.read(fd, 1024)
    print data.lstrip()
```
```python
from zero_buffer import Buffer
b = Buffer.allocate(8192)
with open(path, "rb") as f:
    b.read_from(f.fileno())
for part in b.view().split(b":"):
    part.write_to(sys.stdout.fileno())
    sys.stdout.write('\n')
```
- https://zero-buffer.readthedocs.org/
- https://warehouse.python.org/project/zero_buffer/

# A few more myths
- Function calls are really expensive
- Using only builtin data types will make your code fast
- Don't write Python in the style of Java or C

https://speakerdeck.com/alex/

# Q&A
## Q1
Q1: Is an object faster than a named tuple?

A1: No. A named tuple allows the interpreter to specialize on the fields.

## Q2
Q2: Pyramid has a view function, is this a good use of a dictionary?

A2: What we're specializing for depends on what perspective we have. From
    the perspective of the view author, the algorithm is about expressing a
    template and a data object.  From the perspective of the template engine
    author, your template works on some context that's got some data in it.
    I think it would be better if we could specialize for the use case of
    the view function author, but I understand how we've come to the
    conclusions we've com to in this case.

## Q3
Q3: Is there a conflict between mutable data and allocations and copies.

A3: When you allocate an integer in Python, you're allocating a whole integer
    object. That seems excessive, but we have tools to fix that for us.
    Mutability allows for parallelism. Closure's persisted hash map allows
    you to have a dictionary that's immutable, but without the incredible
    expense of copying all the time.

## Q4
Q4: You highlighted a couple of cases where our intuition about what is fast
    or slow in Python is either outdated or flat wrong. It seems like people
    often take an approach to performance analysis which is like an approach
    to cryptography, which is to say that it's very hard, and you should
    leave it to the experts. I'm wondering if you have advice for people who
    coming up in programming for tuning their intuition about what's actually
    fast or slow.

A4: We can build tools to help people understand the performance of their
    application. The standard library comes with cprofile which does a pretty
    good job of letting us see, at a function level, which functions in our
    application can be slow. There's a great package in the Python package
    index called lineprofiler, which lets us see at a line-by-line level,
    what's slow. The PyPy project has a tool called JIT Viewer whose objective
    is to let you see what the JIT sees about your code overlayed with what
    your code is. So you can see a line of Python code, overlayed with the
    Python bytecode that is executed, overlayed with the JIT's own
    representation of the code, overlayed with the machine code itself. It
    sounds a bit overwhelming, but these tools I found to be shockingly
    A level of knowledge about our code that we didn't have without it.

## Q5
Q5: The Haskell community has been annotating their libraries with their time
    and space complexity. Have you seen this kind of analysis being useful
    in figuring out how extremely dynamic languages behave.

A5: Absolutely. Before any sort of the optimizations I talk about here, the
    optimization of your algorithm itself will almost always dominate the
    performance of what you're trying to do. There's a great page on the
    Python wiki, which documents the time complexity of most of the methods
    on the built in types in Python. Specialized data structures that aren't
    present in the standard library (like skip lists, trees, heaps) can be
    useful.

## Q6
Q6: I'm confused about the difference of the performance between objects and
    dicts that you were talking about. When an instance of a class has the
    __dict__ method, at least when you're not using slots.

A6: Objects with __dict__, how could they possibly have different performance
    from dicts? Why do you believe everything you see? Just because you see
    a thing that looks like a dict, why does it have to be a dict? Python
    is an incredibly dynamic, reflective language, and it shows us all about
    its internals. But sometimes this can mislead us. Specifically under PyPy
    we expose a thing that looks like a dict, but a dict can be many things
    on PyPy which have totally different representations. This is the
    unfortunate case of heuristics. Where you see that and you assume it
    must be like the other dicts because we haven't exposed a different
    detail. In fact, it's represented entirely differently, using a notion
    called maps from a programming language called Self many years ago.
    There's other cases of this as well, of course. If we look a module
    object, looking at globals, we see that those live in what looks like a
    dictionary, but they have different properties. Globals almost never
    change. We probably want to optimize on that, and in fact PyPy does and
    for years there've been patches to let CPython optimize on this intuition
    that things rarely change. All without changing what it looks like to us,
    the Python programmer. It's unfortunate that the way things look is often
    not how they are.
    intuitive and can really provide, where the bulk of the instructions are.
