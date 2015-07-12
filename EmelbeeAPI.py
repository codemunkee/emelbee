from EmelbeeStats import EmelbeeStats
import EmelbeeTeams
from datetime import date
import re


stock_resp = 'Respond with team name for latest scores. Enter "all" '\
             'for all scores\'. To specify date, enter it in the format '\
             '@YYYYMMDD. e.g. "Reds @20140720". For standings, respond '\
             'with "standings".'

stand_stock_resp = 'For standings respond with "Standings League '\
                   'Division". League should be AL or NL. Division should '\
                   'be (W)est, (C)entral, or (E)ast. e.g. "Standings NL W"'


def get_response(message=None):
    """ Respond to an incoming query """
    if not message:
        return stock_resp

    # Always make the message lowercase
    message = message.lower()

    # If someone is searching for scores
    if re.search('standings', message):
        return get_standings(message)
    else:
        return get_scores(message)


def get_standings(message):
    """ Return Standings Information """
    legdev_pattern = re.compile('standings[\s][an]l[\s][wce]')
    # league / division match
    legdev_match = legdev_pattern.search(message)
    if legdev_match:
        year, month, day = todays_date()
        stats = EmelbeeStats(year, month, day)
        league = legdev_match.group()[10:12]
        division = legdev_match.group()[13:14]
        return stats.team_standings(league, division)
    else:
        return stand_stock_resp


def get_scores(message):
    """ Return Scores (gets called by get_response) """
    # If there is a date defined
    if date_defined(message):
        year, month, day = date_defined(message)
    else:
        year, month, day = todays_date()

    # If they save give them all, give them all
    if re.search('all', message):
        stats = EmelbeeStats(year, month, day)
        return stats.team_scores()

    # Otherwise get a list of queried teams
    queried_teams = []
    for team in EmelbeeTeams.get_team_names():
        #team_pattern = re.compile('[\s]'+ team + '[\s]|^' + team)
        team_pattern = re.compile('[\s]'+ team + '[\s]|^' + team + '$|[\s]' +\
                       team + '$|^' + team + '[\s]')
        if team_pattern.search( message):
            # sometimes we can get team abbrevs, this returns
            # the proper team name. e.g. (NYY = Yankees)
            proper_name = EmelbeeTeams.get_proper_name(team)
            queried_teams.append(proper_name)

    # If we have queried team names, get their results
    if len(queried_teams) != 0:
        stats = EmelbeeStats(year, month, day)
        scores = str()
        for qteam in queried_teams:
            scores = scores + stats.team_scores(qteam) + '\n'
        return scores.strip('\n')
    # otherwise, they haven't given us any teams to show them
    else:
        return stock_resp


def date_defined(message):
    """ Identify a defined date """
    pattern = re.compile('@20[0-2][0-9][0-1][0-9][0-3][0-9]')
    date_match = pattern.search(message)
    if date_match:
        year = date_match.group()[1:5]
        month = date_match.group()[5:-2]
        day = date_match.group()[-2:]
        return year, month, day
    else:
        return None


def todays_date():
    """ Returns today's year, month, and day of the month """
    # By default we look for today's stats
    today = date.today()
    year = today.strftime('%Y')
    month = today.strftime('%m')
    day = today.strftime('%d')
    return year, month, day
