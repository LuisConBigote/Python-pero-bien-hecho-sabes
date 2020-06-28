
# =============================================================================
# ===== A GUIDE TO DOs AND DON'Ts =============================================
# =============================================================================

# ===== GENERALS ==============================================================

# LOOPING OVER A RANGE OF NUMBERS

# Don't
for i in [0, 1, 2, 3, 4, 5]:
    print(i**2)

# Do
for i in range(6):
    print(i**2)


# LOOPING OVER A COLLECTION 

colors = ['red', 'green', 'blue', 'yellow']

# Don't 
for i in range(len(colors)):
    print(colors[i])

# Do
for color in colors:
    print(colors)


# LOOPING BACKWARDS 

# Don't
for i in range(len(colors) - 1, -1, -1):
    print(colors[i])

# Do
for color in reversed(colors):
    print(color)


# LOOPING OVER A COLLECTION AND INDICES 

# Don't
for i in range(len(colors)):
    print(i, '-->', colors[i])

# Do 
for i, color in enumerate(colors):
    print(i, '-->', color)


# LOOPING OVER TWO COLLECTIONS 

names = ['raymond', 'rachel', 'matthew']

# Don't
n = min(len(names), len(colors))
for i in range(n):
    print(names[i], '-->', colors[i])

# Do
for name, color in zip(names, colors):
    print(name, '-->', color)


# LOOPING IN SORTED ORDER 

for color in sorted(colors):
    print(color)

for color in sorted(colors, reverse=True):
    print(color)


# CUSTOM SORT ORDER 

# Don't
def compare_length(c1, c2):
    if len(c1) < len(c2): return -1
    if len(c1) > len(c2): return 1
    return 0
# print(sorted(colors, cmp=compare_length))

# Do
print(sorted(colors, key=len))


# DISTINGUISHING MULTIPLE EXIT POINTS IN LOOPS

# Don't
def find(seq, target):
    found = False
    for i, value in enumerate(seq):
        if value == target:
            found = True
            break
    if not found:
        return -1
    return i

# Do
def find2(seq, target):
    for i, value in enumerate(seq):
        if value == target:
            break
    else: # Some poeple would love to rename it to 'nobreak'
        return -1
    return i

# ===== DICTIONARIES ==========================================================

d = { 'matthew': 'blue', 'rachel': 'green', 'raymond':'red' } 

# LOOPING OVER DICTIONARIES

for k in d:
    print(k)

#Don't
for k in d:
    print(k, '-->', d[k])

# Do
for k,v in d.items():
    print(k, '-->', v)

# CONSTRUCT A DICTIONARY FROM PAIRS

d = dict(zip(names,colors))

d = dict(enumerate(names))

# COUNTING WITH DICTIONARIES

# Don't
d = {}
for color in colors:
    if color not in d:
        d[color] = 0
    d[color] += 1

# Do
d = {}
for color in colors:
    d[color] = d.get(color, 0) + 1

# GROUPING WITH DICTIONARIES PART I

names = ['raymond', 'rachel', 'matthew', 'roger', 'betty', 'melissa',
        'judith', 'charlie']

d = {}
for name in names:
        key = len(name)
        if key not in d:
            d[key] = []
        d[key].append(name)

# GROUPING WITH DICTIONARIES PART II

d = {}
for name in names:
    key = len(name)
    d.setdefault(key, []).append(name)

# IS A DICTIONARY POPITEM() ATOMIC?

d = {'matthew': 'blue', 'rachel': 'green', 'raymond': 'red'}

while d:
    key, value = d.popitem()
    print(key, '-->', value)

# KEYWORD ARGUMENTS

# Don't
# twitter_search('@obama', False, 20, True)

# Do
# twitter_search('@obama', retweets=False, numtweets=20, popular=True)

# CLARIFY MULTIPLE RETURN VALUES WITH NAMED TUPLES

from collections import namedtuple
TestResults = namedtuple('TestResults', ['failed', 'attempted'])

# UNPACKING SEQUENCES

p = 'Raymond', 'Hettinger', 0x30, 'python@example.com'

# Don't
fname = p[0]
lname = p[1]
age = p[2]
email = p[3]

# Do
fname, lname, age, email = p


# UPDATING MULTIPLE STATE VARIABLES

# Don't
def fibonacci(n):
    x = 0
    y = 1
    for i in range(n):
        print(x)
        t = y
        y = x + y
        x = t

# Do
def fibonacci(n):
    x, y = 0, 1
    for i in range(n):
        print(x)
        x, y = y, x+y


# SIMULTANEOUS STATE UPDATES

# Don't
"""
tmp_x = x + dx * t
tmp_y = y + dy * t
tmp_dx = influence(m,x,y,dx,dy,partial='x')
tmp_dy = influence(m,x,y,dx,dy,partial='y')
x = tmp_x
y = tmp_y
dx = tmp_dx
dy = tmp_dy
"""
# Do
"""
x, y, dx, dy =  (x + dx * t, y + dy * t,
                influence(m, x, y, dx, dy, 'x'),
                influence(m, x, y, dx, dy, 'y'))
"""

# ===== EFFICIENCY ============================================================

# CONCATENATING STRINGS

# Don't
s = names[0]
for name in names[1:]:
    s += ', ' + name
print(s)

# Do
s = ', '.join(names)
print(s)

# UPDATING SEQUENCES

# Don't
del names[0]
names.pop(0)
names.insert(0, 'mark')
print(names)

# Do
from collections import deque
names_dq = deque(names) # Deques have a O(1) when changing its f-l items

del names_dq[0] # O(1)
names_dq.popleft() # O(1)
names_dq.appendleft('mark') # O(1)


# ===== DECORATORS AND CONTEXT MANAGERS =======================================

# USING DECORATOS TO FACTOR-OUT ADMINISTRATIVE LOGIC

import urllib

# Don't
def web_lookup(url, saved={}):
    if url in saved:
        return saved[url]
    page = urllib.urlopen(url).read()
    saved[url] = page
    return page

# Do
from functools import wraps
def cache(func):
    saved = {}
    @wraps(func)
    def newfunc(*args):
        if args in saved:
            return newfunc(*args)
        result = func(*args)
        saved[args] = result
        return result
    return newfunc

@cache
def web_lookup(url):
    return urllib.urlopen(url).read()

# FACTOR-OUT TEMPORARY CONTEXTS

from decimal import *

# Don't
old_context = getcontext().copy()
getcontext().prec = 50
print(Decimal(355) / Decimal(113))
setcontext(old_context)

# Do
with localcontext(Context(prec=50)):
    print(Decimal(355) / Decimal(113))

# HOW TO OPEN AND CLOSE FILES

# Don't
f = open("ejemplo.txt")
try:
    data = f.read()
finally:
    f.close()

# Do
with open('ejemplo.txt') as f:
    data = f.read()

# HOW TO USE LOCKS
import threading
lock = threading.Lock()

# Don't
lock.acquire()
try:
    print('Critical section 1')
    print('Critical section 2')
finally:
    lock.release()

# Do
with lock:
    print('Critical section 1')
    print('Critical section 2')

# FACTOR-OUT TEMPORARY CONTEXTS

import os

# Don't
try:
    os.remove('somefile.tmp')
except OSError:
    pass

# Do
from contextlib import suppress

with suppress(OSError):
    os.remove('somefile.tmp')

from contextlib import redirect_stdout
import sys

# Don't
with open('help.txt', 'w') as f:
    oldstdout = sys.stdout
    sys.stdout = f
    try:
        help(pow)
    finally:
        sys.stdout = oldstdout

# Do
with open('help.txt', 'w') as f:
    with redirect_stdout(f):
        help(pow)

# ===== CONCISE EXPRESSIVE ONE-LINERS =========================================

# LIST COMPREHENSIONS AND GENERATOR EXPRESSIONS

# Don't
result = []
for i in range(10):
    s = i ** 2
    result.append(s)
print(result)

# Do
result = [i ** 2 for i in range(10)]
print(result)
