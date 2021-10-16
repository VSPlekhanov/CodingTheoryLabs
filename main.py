import numpy as np

# 000000000000000000000001

# (23, 15, 7)
# G =
# 100011111010111100000000
# 010001111101011110000000
# 001000111110101111000000
# 000100011111010111100000
# 000010001111101011110000
# 000001000111110101111000
# 000000100011111010111100
# 000000010001111101011110
# 000000001000111110101111


v = ['--------------111111111',
     '111111111--------------',
     '-------111111111-------',
     '11111--------------1111',
     '1111--------11111------',
     '-----11111--------1111-',
     '-1-1-1-1-1-1-1-1-1-----',
     '------1-1-1-1-1-1-1-1-1',
     '--11--11--11--11--1----',
     '----11--11--11--1--11--',
     '------1-111--1-1-111---',
     '------1---111----1-1111',
     '--11---111---1--1----11',
     '11--111----1--1---11---',
     '111-1111-1-1-----------',
     '11111---111-------1----']


def test(v):
    l = len(v[0])
    for i in range(l):
        for j in range(l):
            for k in range(l):
                if i != j and i != k and j != k:
                    at_least_one_passed = False
                    for x in v:
                        if x[i] == x[j] == x[k] == '-':
                            at_least_one_passed = True
                            break
                    if not at_least_one_passed:
                        return i, j, k

    return -1, -1, -1


def to_matrix(m):
    m1 = [[] for i in range(len(m))]
    for i in range(len(m)):
        m1[i] = []
        for x in m[i]:
            m1[i].append(int(x))
    return m1


def to_arr(x):
    m1 = []
    for i in x:
        m1.append(int(i))
    return np.array(m1)


def invert_matrix(a):
    n = len(a)
    am = np.copy(a)
    idn = np.identity(n)
    im = np.copy(idn)

    indices = list(range(n))
    for fd in range(n):
        for i in indices[0:fd] + indices[fd + 1:]:
            curr = am[i][fd]
            for j in range(n):
                am[i][j] = (am[i][j] - curr * am[fd][j]) % 2
                im[i][j] = (im[i][j] - curr * im[fd][j]) % 2
    return im


def get_gs(v, g):
    gs = [[] for _ in range(len(v))]
    positions = [[] for _ in range(len(v))]
    for i in range(len(v)):
        for j, s in enumerate(v[i]):
            if s == '1':
                positions[i].append(j)
        # print(len(positions[i]))
        gs[i] = invert_matrix(g[:, positions[i]]).dot(g) % 2
    return gs, positions


def generate_code_words(g):
    code_words = []
    for i in range(2 ** (len(g))):
        num = i
        curr = np.zeros(len(g[0]), dtype=int)
        for j in range(len(g) - 1, -1, -1):
            if num // 2 ** j == 1:
                curr += g[j]
                num -= 2 ** j
        code_words.append(list(curr % 2))
    return code_words


def cw_to_str(cw):
    arr = []
    for w in cw:
        s = ''
        for i in w:
            s += str(i)
        arr.append(s)
    return arr


def to_str(c):
    s = ''
    for i in c:
        s += str(i)
    return s


def check(g):
    min_d = len(g[0])
    for i in range(len(g)):
        for j in range(i + 1, len(g)):
            d = np.sum((to_arr(g[i]) - to_arr(g[j])) % 2, dtype=int)
            if d < min_d:
                min_d = d
    return min_d


def move_r(arr):
    a = arr
    last = a[len(a) - 1]
    for i in range(len(a) - 1, 0, -1):
        a[i] = a[i - 1]
    a[0] = last
    return a


def generate_matrix(c):
    c = to_arr(c)
    last = len(c) - 1
    g = []
    i = 0
    while c[last] != 1:
        g.append(to_str(c))
        c = move_r(c)
        i += 1
    g.append(to_str(c))
    return g


c = '100011111010111100000000'
g = generate_matrix(c)
# print(g)

# print(test(v))
# if __name__ == '__main__':
# print(check(g))


g_matrix = np.array(to_matrix(g))
gs, positions = get_gs(v, g_matrix)
cw_set = set(cw_to_str(generate_code_words(g_matrix)))
# print(check(generate_code_words(g_matrix)))
# print(check(g))


while (True):
    # code_word = '11010010110000000'
    # error = to_arr('00000000000000001')
    code_word = input('Input code word:\n ')
    if code_word not in cw_set:
        print('This is not a code word!')
        continue
    error = to_arr(input('Input error code:\n '))
    if len(error) != len(code_word):
        print('Invalid error code')
        continue
    code_word = to_arr(code_word)
    received = (code_word + error) % 2
    print('Received code: ', to_str(received))

    res = []
    for i in range(len(gs)):
        res.append(received[positions[i]].dot(gs[i]) % 2)#
    min_d = len(received)
    best_index = -1
    for i in range(len(res)):
        d = np.sum((received - res[i]) % 2, dtype=int)
        if d < min_d:
            min_d = d
            best_index = i

    print('The result is: ', to_str(np.array(res[best_index], dtype=int)))
    print()
