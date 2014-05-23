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
        message = "Best counter to {p} is {cn} with advantage of {a} and win_rate of {wr} of {nom} games"
        cn = counter_pick.name
        cm = counter_pick.matchup
        print(message.format(p=pick, cn=cn, a=self.extract_float(cm.advantage)*(-1), wr=cm.win_rate, nom=cm.number_of_matches))

    def find_best_counter(self, hero_name):
        """ Searches through all the matchup information of every hero and selects the one that
            the current hero has the highest disadvantage against """

        hero_name = self.clear_name(hero_name)
        """ Dictionary of {'hero_name': Matchup} """
        matchup = self.matchups[hero_name]

        min_advantage = lambda x: self.extract_float(x[1].advantage)
        counter_pick = Counter(*min(matchup.iteritems(), key=min_advantage))

        self._print_counter(hero_name, counter_pick)

