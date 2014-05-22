import json
import re


class Suggest(object):
    def __init__(self):
        """ list of dictionaries with each dictionary holding information about a hero """
        matchups_raw = []
        with open("../heroes_json/heroes.json", 'r') as f:
            matchups_raw = json.load(f)

        self.matchups = {}
        for hero_matchup in matchups_raw:
            self.matchups.update({hero_matchup['name'].lower(): hero_matchup['matchups']})

    def find_best_counter(self, hero_name):
        matchup = self.matchups[hero_name]
        best_counter_name = ''
        best_counter_advantage = 1000.0

        for hero_name, matchup in matchup.iteritems():
            advantage = float(re.match("\-?\d+.\d+", matchup[0]).group())
            if advantage < best_counter_advantage:
                best_counter_advantage = advantage
                best_counter_name = hero_name

        print best_counter_name, best_counter_advantage


