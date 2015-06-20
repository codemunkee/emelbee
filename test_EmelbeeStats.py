import pytest
import EmelbeeStats
import re

stats = EmelbeeStats.EmelbeeStats('2015','06','15',
                                  'master_scoreboard.json.sample')

# print string returned from team_scores function
def test_all_score_output():
    patterns=re.compile(r'\bPadres\b|\Giants\b|\bAstros\b|\bDodgers\b')   
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
    assert re.match('Dodgers', stats.team_scores('Dodgers'))
