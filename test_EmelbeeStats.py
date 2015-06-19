import pytest
import EmelbeeStats
import re

stats = EmelbeeStats.EmelbeeStats('2015','06','15',
                                  'master_scoreboard.json.sample')

# print string returned from team_scores function
def test_all_score_output():
    #patterns = re.compile(r'\bDodgers\b' | r'\bGiants\b')   
    patterns=re.compile(r'\bPadres\b|\Giants\b|\bAstros\b|\bDodgers\b')   
    assert patterns.search(stats.team_scores())

# connect to the API and get JSON dict results
def test_connect_to_api():
    json = stats.return_stats()
    assert isinstance(json, dict)
