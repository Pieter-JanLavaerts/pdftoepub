#!/usr/bin/sh
pandoc -f epub -t html -o "$1.html" "$1"  --standalone --embed-resources

