#!/usr/bin/env python3

from itertools import zip_longest
import unicodedata

a = 0
b = 0
c = 0

def norm(token):
    if token:
        return "".join(ch for ch in token if unicodedata.category(ch)[0] == "L")


for g_line, w_line in zip(open("gutenberg_0.txt"), open("wikisource_0.txt")):
    for g_token, w_token in zip_longest(g_line.split(), w_line.split()):
        if g_token == w_token:
            print(g_token, w_token, "", sep="\t")
            a += 1
        elif norm(g_token) == norm(w_token):
            print(g_token, w_token, ".", sep="\t")
            b += 1
        else:
            print(g_token, w_token, "@", sep="\t")
            c += 1

print(a, b, c)