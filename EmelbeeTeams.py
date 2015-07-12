"""
return valid team names
"""

team_names = {'dodgers': 'dodgers',
              'lad': 'dodgers',
              'bums': 'dodgers',
              'giants': 'giants',
              'sfg': 'giants',
              'gnats': 'giants',
              'padres': 'padres',
              'sd': 'padres',
              'd-backs': 'd-backs',
              'diamondbacks': 'd-backs',
              'ari': 'd-backs',
              'rockies': 'rockies',
              'col': 'rockies',
              'reds': 'reds',
              'cin': 'reds',
              'cardinals': 'cardinals',
              'cards': 'cardinals',
              'stl': 'cardinals',
              'pirates': 'pirates',
              'pit': 'pirates',
              'bucs': 'pirates',
              'orioles': 'orioles',
              'bal': 'orioles',
              'red sox': 'red sox',
              'bos': 'red sox',
              'yankees': 'yankees',
              'yanks': 'yankees',
              'nyy': 'yankees',
              'white sox': 'white sox',
              'cws': 'white sox',
              'cubs': 'cubs',
              'cubbies': 'cubs',
              'chc': 'cubs',
              'marlins': 'marlins',
              'mia': 'marlins',
              'rays': 'rays',
              'tb': 'rays',
              'twins': 'twins',
              'min': 'twins',
              'athletics': 'athletics',
              'oak': 'athletics',
              'mariners': 'mariners',
              'sea': 'mariners',
              'astros': 'astros',
              'hou': 'astros',
              'rangers': 'rangers',
              'tex': 'rangers',
              'nationals': 'nationals',
              'nats': 'nationals',
              'wsh': 'nationals',
              'phillies': 'phillies',
              'phi': 'phillies',
              'braves': 'braves',
              'atl': 'braves',
              'indians': 'indians',
              'cle': 'indians',
              'mets': 'mets',
              'nym': 'mets',
              'tigers': 'tigers',
              'det': 'tigers',
              'blue jays': 'blue jays',
              'tor': 'blue jays',
              'royals': 'royals',
              'kc': 'royals',
              'angels': 'angels',
              'laa': 'angels'}


def get_team_names():
    """ Return a list of team names """
    teams = []
    for team in team_names:
        teams.append(team)
    return teams


def get_proper_name(name):
    """ Return the proper name for a team """
    return team_names[name]


def valid_name(name):
    """ Return the proper name for a team """
    valid_names = get_team_names()
    # Convert Name to lowercase
    name = name.lower()
    if name in valid_names:
        return True
    else:
        return False
