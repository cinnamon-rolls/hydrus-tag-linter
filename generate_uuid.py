#!/usr/bin/python3

"""
Use this script to generate random strings

USAGE:
    -q sets the amount of IDs to generate, default 1
    -l sets the length of each ID, default 8


FOR LINUX USERS:
    I personally run this command: ./generate_uuid.py | xclip -selection c -rmlastnl
    This will automatically copy the output to my clipboard
    Note that just selecting the output and copying and pasting manually is sufficient
"""

import argparse
from secrets import randbelow

# These should be case insensitive and generally just
# not a pain to encode or move around
CHARS = [i for i in "abcdefghijklmnopqrstuvwxyz0123456789"]
CHARS_LEN = len(CHARS)

argp = argparse.ArgumentParser()

argp.add_argument(
    "--quantity", "-q",
    type=int, default=1,
    help="Number of strings to generate")

argp.add_argument(
    "--length", "-l",
    type=int, default=8,
    help="length of the string to generate"
)

args = argp.parse_args()

quantity = args.quantity
length = args.length


def random_string():
    ret = ""
    for i in range(0, length):
        ret += CHARS[randbelow(CHARS_LEN)]
    return ret


for i in range(0, quantity):
    print(random_string())
