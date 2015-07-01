import pytest
import re
import sys
import os
import inspect


# This lets us load the module from the parent directory
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import EmelbeeStats

stats = EmelbeeStats.EmelbeeStats('2015', '07', '01',
                                  'data/scores.json')


# print string returned from team_scores function
def test_all_score_output():
    patterns = re.compile(r'\bLAD\b|\SF\b|\CWS\b|\bBAL\b')
    assert patterns.search(stats.team_scores())


# connect to the API and get JSON dict results
def test_connect_to_api():
    json = stats.return_stats()
    assert isinstance(json, dict)


# make sure if we give a bogus team name the method returns false
def test_invalid_team():
    assert stats.valid_team('Gnats') == False


# make sure if we give a valid team name the method returns false
def test_valid_team():
    assert stats.valid_team('Dodgers') == True


# make sure if we give a valid team name the method returns false
def test_case_insensitive_team():
    assert stats.valid_team('doDGers') == True


# get an individual team score
def test_team_score():
    assert re.match('LAD|Dodgers', stats.team_scores('Dodgers'))
