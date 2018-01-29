#!/usr/bin/env python
# -*- coding: utf-8 -*-


# -*- coding: utf-8 -*-
import re


def clean_str(string):
    string = string.replace('\n', '').replace('\r', '')
    string = string.lower()
    string = re.sub(r"[\s+\!\/_,$%^*(+\'\"\"]+|[+——！，。？、~@#￥%……&·*<>（）:：；《）《》“”()»〔〕【】{}\[\]↑●★『』「」-]+", ' ', string)
    string = re.sub(' ', '', string)
    return string


# s="你好\n这是http://www.baidu.comfads妈 妈"
# print(clean_str(s))


def to_str(bytes_or_str):
    if isinstance(bytes_or_str, bytes):
        value = bytes_or_str.decode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of str


def to_bytes(bytes_or_str):
    if isinstance(bytes_or_str, str):
        value = bytes_or_str.encode('utf-8')
    else:
        value = bytes_or_str
    return value  # Instance of bytes




def read_all_data(fn):
    all = b''
    with open(fn, 'rb') as rf:
        while True:
            cc = rf.read(16 * 10240)
            if not cc:
                break
            else:
                all += cc

    return to_str(all)


def is_chinese(s):
    return u'\u4e00' <= s <= u'\u9fff'


def is_digit(s):
    for c in s:
        if c not in '.0123456789*':
            return False
    return True


def is_validchar(ch=""):
    if '0'<=ch<='9' or 'a'<=ch<='z' or 'A'<=ch<='Z':
        return True
    if is_chinese(ch):
        return True
    if ch in [' ','-',":",'//','\\']:
        return True
    if ch in '''+\!\/_,$%^*(+\'\"\"]+|[+——！，。？、~@#￥%……&·*<>（）:：；《）《》“”()» {}\[\]-]+''':
        return True
    if ch in '''.,'":;?!@#$%^&*()_-+=!~<>{}[]|''':
        return True
    return False


def conv_validstr(s=""):
    a=""
    for c in s:
        if is_validchar(c):
            a+=c
    return a