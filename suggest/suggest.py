import json
import re
from pprint import pprint


class Suggest(object):
    def __init__(self):
        self.clear_name = lambda s: s.lower().replace('-', '')
        """ read matchup information from file that is a list of dictionaries 
            with each dictionary holding information about a hero """
        self.matchups = {}
        with open("../heroes_json/heroes.json", 'r') as f:
            for hero_matchup in json.load(f):
                name = self.clear_name(hero_matchup['name'])
                self.matchups.update({name: hero_matchup['matchups']})

    def _print_matchups(self):
        pprint(self.matchups)

    def find_best_counter(self, hero_name):
        hero_name = self.clear_name(hero_name)
        matchup = self.matchups[hero_name]
        best_counter_name = ''
        best_counter_advantage = 1000.0

        for hero_name, matchup in matchup.iteritems():
            advantage = float(re.match("\-?\d+.\d+", matchup[0]).group())
            if advantage < best_counter_advantage:
                best_counter_advantage = advantage
                best_counter_name = hero_name

        print best_counter_name, best_counter_advantage


