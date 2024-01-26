import re
import unicodedata
import sys


def to_pascal_case(phrase: str):
    words = phrase.lower().split()
    pascal_case_words = [word.capitalize() for word in words]
    return "".join(pascal_case_words)


def strip_accents(s):
    """https://stackoverflow.com/a/518232"""
    return "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")


def keep_only_letters(s):
    """https://stackoverflow.com/a/72478014/4072641"""
    return re.sub("[\W\d_]", "", s)


input_file = input("input file (empty to scan lines): ")

output_file = input("output file (empty to print to stdout): ")
if output_file:
    output_file = open(output_file, "w", encoding="utf8")
    sys.stdout = output_file

if input_file:
    with open(input_file, encoding="utf8") as file:
        for line in file:
            normalized = strip_accents(keep_only_letters(to_pascal_case(line)))
            print(normalized, line)
else:
    line = input("input lines (empty line to stop):\n")
    while line:
        normalized = strip_accents(keep_only_letters(to_pascal_case(line)))
        print(normalized, line)
        line = input()

if output_file:
    output_file.close()
