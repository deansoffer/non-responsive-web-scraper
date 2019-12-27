# -*- encoding: utf-8 -*-
import argparse
import requests
from search_engines import Google
import codecs
import os
import re
from search_engines.core import utilities as utl
from bs4 import BeautifulSoup
try:
    from search_engines.core.engines import engines_dict, Multi, All
    from search_engines import config
    from search_engines.libs import windows_cmd_encoding
except ImportError as e:
    msg = '"{}"\nPlease install `search_engines` to resolve this error.'
    raise ImportError(msg.format(e.__doc__))


def file_get_contents(filename):
  if os.path.exists(filename):
    fp = open(filename, "r", encoding="utf8")
    content = fp.read()
    fp.close()
    return content


def check_regex():
    reg = r"\name\"viewport\""
    html = file_get_contents('./somehtml.txt')
    found_meta = re.match(reg, html, re.MULTILINE | re.IGNORECASE)
    if 'name="viewport"' in html:
        print('found')
    else:
        print(html)


def make_search(query, num_pages, start_from = None):
    reg = r"\"viewport\""
    starLinks=[]
    print('Query: {:s} | Pages: {:d}'.format(query, num_pages))
    engine = Google()
    engine._start_page = start_from
    results = engine.search(query, num_pages)
    links = results.links()

    for link in links:
        found_meta = False
        try:
            print("checking site: ", link)
            result = requests.get(link)
            if result.status_code not in [200, 301]:
                continue

            # found_meta = re.match(reg, result.text, re.MULTILINE | re.IGNORECASE)
            if 'name="viewport"' not in result.text:
                starLinks.append(link)
                found_meta = True
                print(found_meta)
        except Exception as e:
            print(e)

    print("Meta Not Found In: ", starLinks)

    with codecs.open('./reports/{}.txt'.format(query), 'wb', 'utf8') as f:
        for item in starLinks:
            f.write("%s\n" % item)

if __name__ == '__main__':
    # check_regex()
    # print(quit)
    ap = argparse.ArgumentParser()
    ap.add_argument('-q', help='query', required=True)
    ap.add_argument('-e', help='search engine(s) - ' + ', '.join(engines_dict), default='google')
    ap.add_argument('-r', help='report file [html, csv, json]', default=None)
    ap.add_argument('-p', help='number of pages', default=config.search_pages, type=int)
    ap.add_argument('-sp', help='start page', required=False, default=None)
    ap.add_argument('-f', help='filter results [url, title, text, host]', default=None)
    ap.add_argument('-u', help='collect only unique links', action='store_true')
    ap.add_argument('-proxy', help='use proxy (protocol://ip:port)', default=config.proxy)
    ap.add_argument('-tor', help='use tor proxy', action='store_true')
    args = ap.parse_args()
    make_search(args.q, args.p, args.sp)

    # proxy = args.proxy or (config.tor if args.tor else None)
    # timeout = config.timeout + (10 * int(args.tor))
    # engines = [
    #     e.strip() for e in args.e.lower().split(',')
    #     if e.strip() in engines_dict or e.strip() == 'all'
    # ]
    #
    # if not engines:
    #     print('Choose a search engine: \n' + ', '.join(engines_dict))
    # else:
    #     if 'all' in engines:
    #         engine = All(proxy, timeout)
    #     elif len(engines) > 1:
    #         engine = Multi(engines, proxy, timeout)
    #     else:
    #         engine = engines_dict[engines[0]](proxy, timeout)
    #
    #     engine.unique_urls = args.u
    #     if args.f:
    #         engine.set_search_operator(args.f)
    #
    #
    #     #engine.search(args.q, args.p)
    #
    #     #engine.report(args.r)

