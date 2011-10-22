#coding:utf-8
"""
    helpers.py
    ~~~~~~~~~~~~~~~~~~~~

"""

import unicodedata
import re

def normalize(string):
    string = unicodedata.normalize("NFKD", unicode(string)).encode(
        "ascii", "ignore")
    string = re.sub(r"[^\w]+", " ", string)
    string = "-".join(string.lower().strip().split())
    return string

def normalize_tags(string):
    tags = string.split(',')
    result = []
    for tag in tags:
        normalized = normalize(tag)
        if normalized and not normalized in result:
            result.append(normalized)

    return result
