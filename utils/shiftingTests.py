import time
t = ['a', 'b', 'c', 'd', 'e']
for item in t:
    print item
time.sleep(1)
print ' '
t = t[1:]
t.append('f')
for item in t:
    print item
print ' '
f = [1, 2, 3]
time.sleep(1)
s = t + f
for item in s:
    print item
