#!/usr/bin/bash

cd $(dirname $0)
git pull --rebase
./report.py | mutt cs-conference-tracker@googlegroups.com bamos@cs.cmu.edu \
  -s "Conference Status for $(date +%Y-%m-%d)"
