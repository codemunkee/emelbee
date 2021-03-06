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
                                       'data/scores.json', debug=True)

todays_stats = EmelbeeStats.EmelbeeStats(year, month, day, debug=True)

no_stats = EmelbeeStats.EmelbeeStats('1913', '01', '01', debug=True)


# print string returned from team_scores function (old stats)
def test_bogus_date_output():
    patterns = re.compile(r'No game information found')
    assert patterns.search(no_stats.team_scores())

# print string returned from team_scores function (old stats)
def test_pastday_all_score_output():
    patterns = re.compile(r'\bLAD\b|\SF\b|\CWS\b|\bBAL\b')
    assert patterns.search(past_stats.team_scores())

# print string returned from team_scores function (today stats)
def test_todays_all_score_output():
    patterns = re.compile(r'\bLAD\b|\SF\b|\CWS\b|\bBAL\b')
    assert patterns.search(past_stats.team_scores())

# print string returned from team_scores function (today stats)
def test_todays_all_score_output():
    patterns = re.compile(r'\bLAD\b|\SF\b|\CWS\b|\bBAL\b')
    assert patterns.search(past_stats.team_scores())

# get dictionary from scores API
def test_todays_json_scores_from_api():
    scores = todays_stats.return_scores()
    assert isinstance(scores, dict)

# get dictionary from standings API
def test_todays_json_standings_from_api():
    standings = todays_stats.return_standings()
    assert isinstance(standings, dict)

# print string returned from team_scores function (today stats)
def test_todays_all_standings_output():
    patterns = re.compile(r'\bDiamondbacks\b|\Giants\b')
    assert patterns.search(past_stats.team_standings('nl', 'w'))

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

