#!/usr/bin/env python
# -*- coding: utf-8; -*-

import requests

# Declaring available languages
languages = {
    'as' : 2,
    'bash' : 13,
    'c#' : 20,
    'c' : 7,
    'c++' : 7,
    'css' : 8,
    'diff' : 5,
    'html' : 11,
    'xml' : 11,
    'java' : 9,
    'js' : 10,
    'perl' : 18,
    'php' : 15,
    'plain' : 6,
    'py' : 16,
    'rb': 3,
    'sql' : 14,
    'yaml' : 19,
}

def pastie(content, lang='plain', private=0):

    # If lang is in languages, choose it else choose plain
    parser_id = languages[lang] if lang in languages else languages['plain']

    # Create a new session
    s = requests.session()

    # Creating post dict
    post_dict = {}
    post_dict['utf8'] = '&#x2713;'
    post_dict['paste[authorization]'] = 'burger'
    post_dict['paste[access_key]'] = ''
    post_dict['paste[parser_id]'] = parser_id
    post_dict['paste[body]'] = content
    post_dict['paste[restricted]'] = private

    rep = s.post('http://pastie.org/pastes', post_dict)

    if 'paste-id' in rep.headers:
        return rep.headers['paste-id']
    else:
        return False


if __name__ == '__main__':

    import sys, argparse

    # =================================================================================
    # Setting argparse
    # =================================================================================

    parser = argparse.ArgumentParser()

    # Private param
    parser.add_argument("-p", "--private", help="Make the paste private", action="store_true")

    # Language lexer
    parser.add_argument("-l", "--lang", help="Set language lexer for content (default: plain)")

    # Input file
    parser.add_argument("file", nargs='?', help="Input file, if not specified, reading from stdin")

    # Show lang list
    parser.add_argument("--langlist", help="List available language lexers", action="store_true")

    # =================================================================================
    # Reading params
    # =================================================================================

    args = parser.parse_args()

    # Lang list
    if args.langlist:
        print '================================================================'
        print 'Available language lexers'
        print '================================================================'
        print '\n'.join(languages)
        sys.exit(0)

    # Input content
    if args.file:
        try:
            f = open(args.file, 'r')
            content = f.read()
        except IOError:
            print 'Error while reading input file'
            sys.exit(1)
        except Exception, e:
            print str(e)
            sys.exit(1)
    else:
        try:
            content = sys.stdin.read().decode('utf8')
        except KeyboardInterrupt:
            sys.exit(1)

    # Private param
    private = 1 if args.private else 0

    # Language lexser
    lang = args.lang if args.lang else 'plain'

    print 'http://pastie.org/' + pastie(content, lang, private)
