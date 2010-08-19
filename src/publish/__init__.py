#!/usr/bin/env python

import argparse, sys
from pprint import pprint
from publish.utils import parse_meta_and_article


def main():
    """
    ``publish`` executable.
    """
    parser = argparse.ArgumentParser(description='Article Publisher')
    parser.add_argument('path', type=str,
                        help='Relative or absolute path to article')
    args = parser.parse_args()
    f = open(args.path, 'r')
    meta, content = parse_meta_and_article(f.read())

