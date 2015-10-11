#!/usr/bin/python

"""

"""

from glob import glob
import sys
import os
import datetime


def strip_post_name(file_name):
    prefix = '_posts/yyyy-mm-dd-'
    suffix = '.md'
    return file_name[len(prefix):-len(suffix)]


def strip_lhs_name(file_name):
    prefix = '_lhs/'
    suffix = '.lhs'
    return file_name[len(prefix):-len(suffix)]

posts = map(strip_post_name, glob('_posts/*.md'))
lhs = map(strip_lhs_name, glob('_lhs/*.lhs'))

args = sys.argv[1:]

DRY = False

i = 0
while i < len(args):
    if args[i] == '--dry':
        DRY = True
        args.pop(i)
    else:
        i += 1

if len(args) > 0:
    lhs = [l for l in lhs if any(a in l for a in args)]
else:
    lhs = [l for l in lhs if l not in posts]

for l in lhs:
    now = datetime.date.today()
    today = '%04i-%02i-%02i' % (now.year, now.month, now.day)
    cmd = 'runhaskell scripts/lhs-to-jekyll-markdown.lhs < _lhs/{0}.lhs > _posts/{1}-{0}.md'.format(l, today)
    print('running', cmd)
    if not DRY:
        os.system(cmd)
