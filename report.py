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
        print("Error: {} not in {}.".format(yaml, field))
        sys.exit(-1)
    return yaml[field]


class Event:
    def __init__(self, yaml):
        self.date = getExpectedField(yaml, 'date')
        if 'note' in yaml:
            self.note = yaml['note']
        else:
            self.note = None


class Conference:
    def __init__(self, yaml, group):
        self.group = group
        self.title = getExpectedField(yaml, 'title')
        self.events = [Event(eYaml)
                       for eYaml in getExpectedField(yaml, 'events')]
        self.url = yaml['url']
        upcomingEvents = [e for e in self.events if e.date > today]
        if len(upcomingEvents) > 0:
            self.upcoming = min(upcomingEvents, key=attrgetter('date'))
        else:
            self.upcoming = None

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

    print("\n# Upcoming conferences.")
    for conf in sorted(upcoming, key=attrgetter('upcoming.date')):
        print("+ {}".format(conf.title))
        note = conf.upcoming.note
        date = conf.upcoming.date
        if note:
            print("    + {} - {}".format(note, date))
        else:
            print("    + {}".format(date))
        print("    + {}".format(conf.url))

    print("\n\n# Outdated information.")
    for conf in outdated:
        print("+ {}".format(conf.title))
