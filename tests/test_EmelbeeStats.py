import pytest
import re
import sys
import os
import inspect
from datetime import date


# This lets us load the module from the parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

today = date.today()
year = today.strftime('%Y')
month = today.strftime('%m')
day = today.strftime('%d')

import EmelbeeStats

past_stats = EmelbeeStats.EmelbeeStats('2015', '07', '01',
                                       'data/scores.json')

todays_stats = EmelbeeStats.EmelbeeStats(year, month, day)



# print string returned from team_scores function (old stats)
def test_pastday_all_score_output():
    patterns = re.compile(r'\bLAD\b|\SF\b|\CWS\b|\bBAL\b')
    assert patterns.search(past_stats.team_scores())

# print string returned from team_scores function (today stats)
def test_todays_all_score_output():
    patterns = re.compile(r'\bLAD\b|\SF\b|\CWS\b|\bBAL\b')
    assert patterns.search(past_stats.team_scores())

# get dictionary from standings API
def test_todays_standings_info_from_api():
    standings = todays_stats.standings_from_api()
    assert isinstance(standings, dict)

# print string returned from team_scores function (today stats)
def test_todays_all_standings_output():
    patterns = re.compile(r'\bDiamondbacks\b|\Giants\b')
    assert patterns.search(past_stats.team_standings('nl', 'w'))

# make sure if we give a bogus team name the method returns false
def test_invalid_team():
    assert past_stats.valid_team('Gnats') == False


# make sure if we give a valid team name the method returns false
def test_valid_team():
    assert past_stats.valid_team('Dodgers') == True


# make sure if we give a valid team name the method returns false
def test_case_insensitive_team():
    assert past_stats.valid_team('doDGers') == True


# get an individual team score
def test_team_score():
    assert re.match('LAD|Dodgers', past_stats.team_scores('Dodgers'))

# get scores from cache
def test_scores_from_cache_file():
    scores = past_stats.read_cache('tests/emelbee_scores_cache.json')
    assert isinstance(scores, dict)

# get standings from cache
def test_standings_from_cache_file():
    standings = past_stats.read_cache('tests/emelbee_standings_cache.json')
    assert isinstance(standings, dict)

