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

    def __repr__(self):
        return self.title


class ConferenceGroup:
    def __init__(self, yaml):
        self.title = getExpectedField(yaml, 'title')
        self.conferences = [Conference(c, self.title)
                            for c in getExpectedField(yaml, 'conferences')]
        self.upcoming = [c for c in self.conferences if c.date > today]
        self.week = [c for c in self.conferences
                     if 0 <= (today - c.date).days <= 6]
        self.outdated = [c for c in self.conferences
                         if (today - c.date).days > 6]

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
                        metavar="DIR",
                        default="{}/data".format(myDir))
    args = parser.parse_args()

    confGroups = list(iterGroups(args.dataDir))
    upcoming = list(chain.from_iterable(cg.upcoming for cg in confGroups))
    outdated = list(chain.from_iterable(cg.outdated for cg in confGroups))
    week = list(chain.from_iterable(cg.week for cg in confGroups))

    print("# Conferences this past week.")
    for conf in week:
        print("+ [{}] {}".format(conf.group, conf.title))
        print("    + {}".format(conf.url))
        print("    + {}".format(conf.date))

    print("\n\n# Upcoming conferences.")
    for conf in sorted(upcoming, key=attrgetter('date')):
        print("+ [{}] {}".format(conf.group, conf.title))
        print("    + {}".format(conf.url))
        print("    + {}".format(conf.date))

    print("\n\n# Past conferences. Update data.")
    for conf in sorted(outdated, key=attrgetter('date'), reverse=True):
        print("+ [{}] {}".format(conf.group, conf.title))
        print("    + {}".format(conf.url))
        print("    + {}".format(conf.date))

    print("\n\n")
    print("Powered by https://github.com/bamos/conference-tracker")
    print("Crafted by Brandon Amos: http://bamos.github.io")
