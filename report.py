#!/usr/bin/env python3

import argparse
import os
import yaml


def iterData(dataDir):
    for root, dirs, files in os.walk(args.dataDir):
        for group in files:
            with open(os.path.join(root, group), 'r') as f:
                yield yaml.load(f)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    myDir = os.path.dirname(os.path.realpath(__file__))
    parser.add_argument('--dataDir', type=str,
                        help="Directory of YAML conference data. "
                        "Defaults to '<conference tracker>/data'",
                        default="{}/data".format(myDir))
    args = parser.parse_args()

    for confData in iterData(args.dataDir):
        print(confData)
