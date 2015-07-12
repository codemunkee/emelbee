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

import EmelbeeTeams

# make sure if we give a bogus team name the method returns false
def test_invalid_team():
    assert EmelbeeTeams.valid_name('Gnnats') == False


# make sure if we give a valid team name the method returns false
def test_valid_team():
    assert EmelbeeTeams.valid_name('Dodgers') == True


# make sure if we give a valid team name the method returns false
def test_case_insensitive_team():
    assert EmelbeeTeams.valid_name('doDGers') == True
