from pprint import pprint
from utils.utils import Matchup, Counter
import json
import re


class Suggest(object):
    def __init__(self):
        self.clear_name = lambda s: s.lower().replace('-', '').replace(' ', '')
        self.extract_float = lambda s: float(re.match("\-?\d+.\d+", s).group())
        self.matchups = {}

        """ read matchup information from file that is a list of dictionaries 
            with each dictionary holding information about a hero matchups
            [{'name': 'zeus', 'matchups': {'Abaddon': ['-1.14%', '47.29%', '116,531'], ...}}, {...}] """
        with open("../heroes_json/heroes.json", 'r') as f:
            for hero_matchup in json.load(f):
                name = self.clear_name(hero_matchup['name'])
                matchups = {n: Matchup(*m) for n, m in hero_matchup['matchups'].iteritems()}
                self.matchups.update({name: matchups})

    def _print_matchups(self):
        pprint(self.matchups)

    def _print_counter(self, pick, counter_pick):
        message = "\t {cn} counters {p} with advantage of {a} and win_rate of {wr} of {nom} games"
        cn = counter_pick.name
        cm = counter_pick.matchup
        print(message.format(p=pick, cn=cn, a=self.extract_float(cm.advantage)*(-1), wr=cm.win_rate, 
                             nom=cm.number_of_matches))

    def _print_top_counters(self, pick, counter_picks, limit=1):
        print("Counters to {p} are:".format(p=pick))
        for cp in counter_picks[:limit]:
            cp = Counter(*cp)
            self._print_counter(pick, cp)

    def find_top_counters(self, hero_name, limit=1):
        """ Searches through the matchup information and selects heroes that
            the selected hero has the highest disadvantage against """

        hn = self.clear_name(hero_name)
        matchup = self.matchups.get(hn)

        if not matchup:
            print("Error: {hn} not found!".format(hn=hero_name))
            return 

        min_advantage = lambda x: self.extract_float(x[1].advantage)
        cps = sorted(matchup.iteritems(), key=min_advantage)

        self._print_top_counters(hero_name, cps, limit)
