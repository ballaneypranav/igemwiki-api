from bs4 import BeautifulSoup
from helpers import is_relative, iGEM_URL, resolve_relative_URL
from pathlib import Path
import os
import re
from jsmin import jsmin

# process HTML files

def HTMLparser(config, path, contents, upload_map):

    # https://stackoverflow.com/questions/2725156/complete-list-of-html-tag-attributes-which-have-a-url-value

    soup = BeautifulSoup(contents, 'html5lib')

    queries = [('link', 'href'), ('script', 'src'), ('a', 'href'),
               ('applet', 'codebase'), ('area', 'href'), ('base', 'href'),
               ('blockquote', 'cite'), ('body', 'background'), ('del', 'cite'),
               ('form', 'action'), ('frame', 'longdesc'), ('frame', 'src'),
               ('head', 'profile'), ('iframe', 'longdesc'), ('iframe', 'src'),
               ('img', 'longdesc'), ('img', 'src'), ('img', 'usemap'),
               ('input', 'src'), ('input', 'usemap'), ('ins', 'cite'),
               ('object', 'classid'), ('object', 'codebase'), ('object', 'data'),
               ('object', 'usemap'), ('q', 'cite'), ('audio', 'src'),
               ('button', 'formaction'), ('command', 'icon'), ('embed', 'src'),
               ('html', 'manifest'), ('input', 'formaction'), ('source', 'src'),
               ('track', 'src'), ('video', 'poster'), ('video', 'src')]

    # TODO: Replace URLs for AJAX loads as well

    for (tag_name, attr) in queries:
        query = soup.findAll(tag_name, attrs={attr: True})
        for tag in query:
            # TODO: Add data-nosub
            tag[attr] = iGEM_URL(config, path, upload_map, tag[attr])
            # TODO: Add error handling

    contents = str(soup)
    return contents


def CSSparser(config, path, contents, upload_map):

    css = contents

    # 1) Find all css links
    exp = r'url\(\'?([(..)/].*?)\'?\)'
    links = re.findall(exp, css)

    for i in range(len(links)):
        links[i] = links[i].split('?')[0]
        links[i] = links[i].split('#')[0]

    # 2) Clear all duplicates
    links = list(dict.fromkeys(links))

    # TODO: Think of a way to do replicate data-nosub for CSS

    # print(links)
    # 3) Replace all links with the absolute path
    for link in links:
        css = css.replace(link, iGEM_URL(config, path, upload_map, link))

    return css


def JSparser(contents):

    contents = jsmin(contents)
    # TODO: URL replacement in JS
    # look at Virginia's tasks/unit/html.js for this
    return contents
