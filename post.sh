#!/bin/sh

# variables
title="New Post"
linkpost=
permalink=
postdate=`date +%Y-%m-%d`
posttime=`date +%H:%M:%S`
publishdate="$postdate $posttime"
categories=
openfile=false

# parameter handling
while getopts "n:l:d:p:o" arg
do
    #echo "ARG is $arg"
    case "$arg" in
        n) title="$OPTARG";;
        l) link_post="$OPTARG";;
        d) publishdate="$OPTARG"
            postdate=`date -jf "%F %T" "$publishdate" +%Y-%m-%d`
            posttime=`date -jf "%F %T" "$publishdate" +%H:%M:%S`;;
        p) permalink="$OPTARG";;
        o) openfile=true;;
        -) break;;
        \?) ;;
        *) echo "unhandled option $arg";;
        ?) echo $usage_string
            exit 1;;
    esac
done

# create the file name
lowercase=`echo $title | awk '{print tolower($0)}'`
stripped=`echo ${lowercase// /-}`
filename=$postdate-$stripped.md
file=_drafts/$filename

# create the file and add content
echo "---" >> $file
echo "title: \"$title\"" >> $file

if [ -z "$permalink" ]; then
    echo "permalink: /$stripped/" >> $file
else
    echo "permalink: /$permalink/" >> $file
fi

if [ -z "$linkpost" ]; then
    echo "layout: post" >> $file
else
    echo "layout: post-link" >> $file
    echo "post_link: $linkpost" >> $file
fi

echo "published: false" >> $file


echo "date: $publishdate" >> $file
echo "---\n" >> $file >> $file
echo "Post content!" >> $file

# open file if wanted
if $openfile; then
    open $file
fi

# done
exit 0
