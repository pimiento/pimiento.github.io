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


def link_template(title, url):
    return "[{title}]({url} \"{title}\")".format(title=title, url=url)


def tag_template(tags):
    title = ('|'.join("{}" for tag in tags)).format(*tags)
    header_line = '|'.join([" --- "] * len(tags))
    return title + "\n" + header_line


def tag_link_template(links):
    return ('|'.join("{}" for link in links)).format(*links)


def get_index_page():
    keywords = defaultdict(list)
    lines = []

    for title, url, tags in get_pages():
        link_entry = link_template(title, url)
        lines.append("* {}".format(link_entry))
        for tag in tags:
            keywords[tag].append(link_entry)

    # add blank field
    lines.append("""<div id="data-blank-field" style="height:600px"></div>""")

    keys_iterator = iter(sorted(keywords.keys()))
    for tags in zip_longest(*[keys_iterator]*3, fillvalue=''):
        lines.append("\n"*2)
        lines.append(tag_template(tags))
        for links in zip_longest(*[keywords[t] for t in tags], fillvalue=''):
            lines.append(tag_link_template(links))

    return lines


if __name__ == "__main__":
    with open("index.md", "w") as md:
        css = """<link rel="stylesheet" type="text/css" href="solarized-dark.css" />"""
        print(css, end="\n\n", file=md)
        print(*get_index_page(), file=md, sep='\n')
