#!/usr/bin/env python3

import argparse
import datetime as dt
import os
import sys
import yaml

from itertools import chain
from operator import attrgetter

today = dt.datetime.today().date()


def getExpectedField(yaml, field):
    if field not in yaml:
        print("Error: field '{}' not in {}.".format(field, yaml))
        sys.exit(-1)
    return yaml[field]


class Conference:
    def __init__(self, yaml, group):
        self.group = group
        self.title = getExpectedField(yaml, 'title')
        self.date = getExpectedField(yaml, 'date')
        self.url = getExpectedField(yaml, 'url')
        self.upcoming = self.date > today

    def __repr__(self):
        return self.title


class ConferenceGroup:
    def __init__(self, yaml):
        self.title = getExpectedField(yaml, 'title')
        self.conferences = [Conference(c, self.title)
                            for c in getExpectedField(yaml, 'conferences')]
        self.upcoming = [c for c in self.conferences if c.upcoming]
        self.outdated = [c for c in self.conferences if not c.upcoming]

    def __repr__(self):
        return "{}: {}".format(self.title, self.conferences)


def iterGroups(dataDir):
    for group in os.listdir(args.dataDir):
        with open(os.path.join(dataDir, group), 'r') as f:
            yield ConferenceGroup(yaml.load(f))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    myDir = os.path.dirname(os.path.realpath(__file__))
    parser.add_argument('--dataDir', type=str,
                        help="Directory of YAML conference data. "
                        "Defaults to '<conference tracker>/data'",
                        default="{}/data".format(myDir))
    args = parser.parse_args()

    confGroups = list(iterGroups(args.dataDir))
    upcoming = list(chain.from_iterable(cg.upcoming for cg in confGroups))
    outdated = list(chain.from_iterable(cg.outdated for cg in confGroups))

    print("# Upcoming conferences.")
    for conf in sorted(upcoming, key=attrgetter('date')):
        print("+ [{}] {}".format(conf.group, conf.title))
        print("    + {}".format(conf.date))
        print("    + {}".format(conf.url))

    print("\n\n# Outdated information.")
    for conf in outdated:
        print("+ [{}] {}".format(conf.group, conf.title))
