#!/usr/bin/env python3

import re


def check1(f1, f2, start):
    """
    this checks two files, `f1` would normally be a `raw` file and `f2` the
    `text-prep` file with custom encoding.

    `start` is the initial offset to skip any header lines in `f1`.
    """

    # get the first file starting at `start` and the second file as-is
    x1 = open(f1).read()[start:]
    x2 = open(f2).read()

    # these regex substitution convert the custom encoded `text-prep` files to
    # what should be in the raw file
    x2 = re.sub(r"\\u200B", "\u200B", x2)  # `\u200B` should be an actual U+200B
    x2 = re.sub(r"\\n", "\n", x2)  # `\n` should be an actual \n
    x2 = re.sub(r"\n\^", "", x2)  # a `^` after newline deletes the preceding newline

    x2 = re.sub(r"{([^>]*)>([^}]*)}", r"\1", x2)  # `{foo>bar}` is replaced with just foo

    # x2 now represents what x1 _should_ be
    # we compare char by char, though so we can identifier the location of mismatches
    # note that zip ends as soon as one runs out so we don't have to strip trailers
    offset = 0
    for ch1, ch2 in zip(x1, x2):
        if ch1 != ch2:
            print(x1[offset-100:offset])
            print(f"--- fail {f2}")
            print(x1[offset:offset+100])
            print("---")
            print(x2[offset:offset+100])
            quit()
        offset += 1


def check2(f1, f2):
    """
    this checks two `text-prep` custom-encoded files to see if they are
    identical once the encoding is considered.
    """

    x1 = open(f1).readlines()
    x2 = open(f2).readlines()

    line_num = 0
    for l1, l2 in zip(x1, x2):
        line_num += 1

        o1 = l1
        o2 = l2

        # drop the stuff in the raw text we don't consider part of the
        # transformed text and do the {>} substitutions

        l1 = re.sub(r"\\u200B", "", l1)
        l2 = re.sub(r"\\u200B", "", l2)

        l1 = re.sub(r"\\n", "", l1)
        l2 = re.sub(r"\\n", "", l2)

        l1 = re.sub(r"\^", "", l1)
        l2 = re.sub(r"\^", "", l2)

        l1 = re.sub(r"{([^>]*)>([^}]*)}", r"\2", l1)
        l2 = re.sub(r"{([^>]*)>([^}]*)}", r"\2", l2)

        # ignore case for now

        l1 = l1.lower()  # for now
        l2 = l2.lower()  # for now

        # ignore quote details for now

        l1 = re.sub("’", "'", l1)
        l2 = re.sub("’", "'", l2)
        l1 = re.sub("‘", "'", l1)
        l2 = re.sub("‘", "'", l2)
        l1 = re.sub("“", '"', l1)
        l2 = re.sub("“", '"', l2)
        l1 = re.sub("”", '"', l1)
        l2 = re.sub("”", '"', l2)
        l1 = re.sub("--", '—', l1)
        l2 = re.sub("--", '—', l2)
        l1 = re.sub("`", "'", l1)
        l2 = re.sub("`", "'", l2)

        # ignore italics for now

        l1 = re.sub("_", "", l1)  # for now
        l2 = re.sub("_", "", l2)  # for now

        # if the line doesn't match exactly, complain and quit

        if l1 != l2:
            print(line_num, f1, f2)
            print("---")
            print(o1)
            print("---")
            print(o2)
            print("---")
            offset = 0
            for ch1, ch2 in zip(l1, l2):
                if ch1 != ch2:
                    print(l1[offset-20:offset])
                    print("---")
                    print(l1[offset:offset+20])
                    print("---")
                    print(l2[offset:offset+20])
                    quit()
                offset += 1


check1("raw/gutenberg_A.txt", "text-prep/gutenberg_A.txt", 2544)
print("A matches")

check1("raw/gutenberg_B.txt", "text-prep/gutenberg_B.txt", 1963)
print("B matches")

check1("raw/gutenberg_C.txt", "text-prep/gutenberg_C.txt", 11849)
print("C matches")

check1("raw/gutenberg_D.txt", "text-prep/gutenberg_D.txt", 2876)
print("D matches")

check1("raw/wikisource_E.txt", "text-prep/wikisource_E.txt", 31256)
print("E matches")

print("---")

check2("text-prep/gutenberg_A.txt", "text-prep/gutenberg_B.txt")
print("AB matches")

check2("text-prep/gutenberg_A.txt", "text-prep/gutenberg_C.txt")
print("AC matches")

check2("text-prep/gutenberg_B.txt", "text-prep/gutenberg_C.txt")
print("BC matches")

check2("text-prep/gutenberg_A.txt", "text-prep/gutenberg_D.txt")
print("AD matches")

check2("text-prep/gutenberg_B.txt", "text-prep/gutenberg_D.txt")
print("BD matches")

check2("text-prep/gutenberg_C.txt", "text-prep/gutenberg_D.txt")
print("CD matches")

print("---")
check2("gutenberg_0.txt", "text-prep/gutenberg_A.txt")
print("0A matches")

check2("gutenberg_0.txt", "text-prep/gutenberg_B.txt")
print("0B matches")

check2("gutenberg_0.txt", "text-prep/gutenberg_C.txt")
print("0C matches")

check2("gutenberg_0.txt", "text-prep/gutenberg_D.txt")
print("0D matches")
