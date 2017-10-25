#!/usr/bin/env python3
import os
import glob
from lxml import etree
from itertools import zip_longest
from collections import defaultdict


def get_pages():
    pages = sorted(glob.iglob("*.html"),
                   key=lambda x: os.stat(x).st_mtime,
                   reverse=True)

    for page in pages:
        keywords = []
        tree = etree.parse(page, etree.HTMLParser())
        title = tree.xpath("/html/head/title")[0].text
        meta = tree.xpath("/html/head/meta[@name='keywords']")
        if len(meta) > 0:
            keywords = meta[0].get('content').split(' ')
        url = "https://pimiento.github.io/{}".format(page)
        yield(title, url, keywords)


def get_index_page():
    keywords = defaultdict(list)
    lines = []
    link_template = lambda t, u: "[{t}]({u} \"{t}\")".format(t=t, u=u)
    tag_template = lambda n1, n2: "{n1}|{n2}\n--- |---".format(n1=n1, n2=n2)
    tag_link_template = lambda l1, l2: "{l1}|{l2}".format(l1=l1, l2=l2)

    for title, url, tags in get_pages():
        link_entry = link_template(title, url)
        lines.append("* {}".format(link_entry))
        for tag in tags:
            keywords[tag].append(link_entry)

    lines.extend([""]*8)          # 8 blank lines

    keys_iterator = iter(sorted(keywords.keys()))
    for tags in zip_longest(keys_iterator, keys_iterator, fillvalue=''):
        lines.append(tag_template(*tags))
        (t1, t2) = tags
        for links in zip_longest(keywords[t1], keywords[t2], fillvalue=''):
            lines.append(tag_link_template(*links))

    return lines


if __name__ == "__main__":
    with open("index.md", "w") as md:
        css = """<link rel="stylesheet" type="text/css" href="solarized-dark.css" />"""
        print(css, end="\n\n", file=md)
        print(*get_index_page(), file=md, sep='\n')
