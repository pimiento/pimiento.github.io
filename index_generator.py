#!/usr/bin/env python3
import os
import glob
from lxml import etree


def get_pages():
    pages = sorted(glob.iglob("*.html"),
                   key=lambda x: os.stat(x).st_mtime,
                   reverse=True)
    counter = 1

    for page in pages:
        tree = etree.parse(page, etree.HTMLParser())
        title = tree.xpath("/html/head/title")[0].text
        url = "https://pimiento.github.io/{}".format(page)
        yield("{N}. [{title}]({url} \"{title}\")".format(
            N=counter, title=title, url=url
        ))
        counter += 1


if __name__ == "__main__":
    with open("index.md", "w") as md:
        css = """<link rel="stylesheet" type="text/css" href="solarized-dark.css" />"""
        print(css, end="\n\n", file=md)
        print(*get_pages(), file=md, sep='\n')
