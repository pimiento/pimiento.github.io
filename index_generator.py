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


def get_todo():
    with open("todo.md", "r") as todo:
        return ("* {}".format(line) for line in todo.readlines()
                if line[0] == "*")


def maybe_h(h, n=6):
    return '{} 'if h == "" else '#'*n + " {} " + '#'*n


def blank_field(height):
    return '<div class="blank-field" style="height:{}px"></div>'.format(height)


def link_template(title, url):
    return "[{title}]({url} \"{title}\")".format(title=title, url=url)


def tag_template(tags):
    title = ('|'.join('{}' for tag in tags)).format(*tags)
    if len(tags) > 2:
        first = "| --- |"
        last = "|---:|"
        middle = '|'.join([":---:"] * len(tags[1:-1]))
        header_line = first + middle + last
    else:
        header_line = '|'.join(["---"] * len(tags))
    return title + "\n" + header_line


def tag_link_template(links):
    return ('|'.join('{}' for link in links)).format(*links)


def get_index_page():
    keywords = defaultdict(list)
    lines = []

    for title, url, tags in get_pages():
        link_entry = link_template(title, url)
        lines.append("* {}".format(link_entry))
        for tag in tags:
            keywords[tag].append(link_entry)

    lines.append(blank_field(100))
    lines.append("\n---\n")
    lines.append(maybe_h("-", 3).format("TODO LIST"))
    lines.append("\n---\n")
    lines.extend(get_todo())
    lines.append("\n---\n")


    # add blank field
    lines.append(blank_field(400))
    lines.append("\n---\n")
    lines.append(maybe_h("-", 5).format("ugly implimentation of tags cloud"))
    lines.append("\n---\n")

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
