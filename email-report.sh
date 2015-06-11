#!/usr/bin/bash

cd $(dirname $0)
./report.py | mutt cs-conference-tracker@googlegroups.com \
  -s "Conference Status for $(date +%Y-%m-%d)"
