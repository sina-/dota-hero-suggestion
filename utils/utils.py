from collections import namedtuple


Matchup = namedtuple('Matchup', 'advantage, win_rate, number_of_matches')
Counter = namedtuple('Counter', 'name, matchup')
