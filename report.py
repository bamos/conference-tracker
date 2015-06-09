#!/usr/bin/env python3

import argparse
import os
import yaml

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    myDir = os.path.dirname(os.path.realpath(__file__))
    parser.add_argument('--dataDir', type=str,
                        help="Directory of YAML conference data. "
                        "Defaults to '<conference tracker>/data'",
                        default="{}/data".format(myDir))
    args = parser.parse_args()
