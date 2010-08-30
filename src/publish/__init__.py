#!/usr/bin/env python

import argparse, sys
from pprint import pprint
from publish.utils import parse_meta_and_article


def main():
    """
    ``publish`` executable.
    """
    parser = argparse.ArgumentParser(description='Article Publisher')
    parser.add_argument('path', type=argparse.FileType('r'),
                        help='Relative or absolute path to article')
    parser.add_argument('--draft -d', action='store_true', default=False,
                        help='Publish as a draft only', dest='draft')
    parser.add_argument('--noactive', action='store_false', default=True,
                        help='Make the article "inactive"', dest='is_active')
    parser.add_argument('--login', action='store_false', default=True,
                        help='Require a login to view the article',
                        dest='login_required')
    parser.add_argument('--publish -p', type=str, metavar='YYYY-MM-DD HH:MM',
                        help='When to publish the article (overrides in-file '
                        'value, if any)', default=None, dest='publish')
    args = parser.parse_args()
    f = open(args.path, 'r')
    meta, content = parse_meta_and_article(f.read())

