s = 'hello'
ss = set()
for i in range(len(s)):
    if s[i] == 'e':
        continue
        print('continue')
    ss.add((i, s[i]))
print(ss)
