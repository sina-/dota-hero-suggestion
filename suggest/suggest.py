from pprint import pprint
from utils.utils import Matchup, Counter
from itertools import imap
import json
import re
import operator


class Suggest(object):
    def __init__(self):
        self.clear_name = lambda s: s.lower().replace('-', '').replace(' ', '')
        self.extract_float = lambda s: float(re.match("\-?\d+.\d+", s).group())
        self.matchups = {}
        self.name_map = {}

        """ read matchup information from file that is a list of dictionaries
            with each dictionary holding information about a hero matchups
            [{'name': 'zeus', 'matchups': {'Abaddon': ['-1.14%', '47.29%',
             '116.531'],...}}, {...}] """
        with open("../heroes_json/heroes.json", 'r') as f:
            for hero_matchup in json.load(f):
                name = self.clear_name(hero_matchup['name'])
                self.name_map[name] = hero_matchup['name']
                matchups = {self.clear_name(n): Matchup(*m) for n, m in
                            hero_matchup['matchups'].iteritems()}
                self.matchups.update({name: matchups})

        """ verify content by comparing the number of matchups in
            consecutive hero matchups"""
        prev_count = None
        for n, m in self.matchups.iteritems():
            prev_count = len(m) if not prev_count else prev_count
            if prev_count != len(m):
                print("Error: missing matchup information for {n}".format(n=n))

    def _print_matchups(self):
        pprint(self.matchups)

    def _print_counter(self, counter_pick):
        message = "\t {cn}, advantage: {a}, and win_rate: {wr} of {nom} games"
        cn = counter_pick.name
        cm = counter_pick.matchup
        print(message.format(cn=cn, a=cm.advantage, wr=cm.win_rate,
                             nom=cm.number_of_matches))

    def _print_suggested_counter(self, picks, counter_picks,
                                 order, limit=5):
        print("{ps} is {st} against:".format(ps=picks, st=order))

        for cp in counter_picks[:limit]:
            print("\t {cp}, advantage: {a}".format(cp=self.name_map[cp[0]],
                                                   a=cp[1]))

    def suggest_counter(self, picks, order, limit=5):
        """ Searche through the matchup information and select hero
            that the selected hero, or heroes, has the highest, or lowest,
            advantage against """

        ps = imap(self.clear_name, picks)

        """ Dictionary with {'hero_name': aggregated_advantage}
            where aggregated_advantage is the sum of advantages from matchup
            of given list of heroes """
        total_ad = {}
        for p in ps:
            m = self.matchups.get(p)
            """ delete the picks from result to aviod for example suggesting
                slark as best counter for slark+tiny """
            for pp in picks:
                m.pop(self.clear_name(pp), None)
            for k, v in m.iteritems():
                ad = self.extract_float(v.advantage)+total_ad.get(k, 0.0)
                total_ad.update({k: ad})

        sort_reversed = True
        if order == 'worst':
            sort_reversed = False

        cps = sorted(total_ad.iteritems(), key=operator.itemgetter(1),
                     reverse=sort_reversed)

        self._print_suggested_counter('+'.join(picks), cps, order, limit)
