#!/usr/bin/bash

cd $(dirname $0)
./report.py | mutt bdamos@vt.edu -s "Conference Status for $(date +%Y-%m-%d)"
