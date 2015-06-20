#!/usr/bin/env python

import requests
import json
import sys


class EmelbeeStats:
    """ Pull down MLB stats in JSON from MLB's (mlb.com) free API.

            year, month, day - should be defined for the date you want
            to pull down stats for.

            source - set to local to read cached local file, set to api
            to pull down from MLB API.

            debug - (optional)

        """
    def __init__(self, year, month, day, filename=None, debug=False):

        # Date to Pull down stats for
        self.year = year
        self.month = month
        self.day = day

        # Debug Mode
        self.debug = debug

        # URL for the MLB API
        self.url_base = 'http://gd2.mlb.com/components/game/mlb'

        # JSON file with Sample Stats (if we don't want to reach out to
        # the MLB API directly for debugging and developing).
        self.json_file = filename

        # Get the JSON that this class needs
        self.json_stats = self.return_stats()

        # Team Names as referenced in the MLB API
        self.team_names = ['pirates',
                           'white sox',
                           'orioles',
                           'phillies',
                           'tigers',
                           'reds',
                           'red sox',
                           'braves',
                           'marlins',
                           'yankees',
                           'mets',
                           'blue jays',
                           'rays',
                           'nationals',
                           'cubs',
                           'indians',
                           'rangers',
                           'dodgers',
                           'astros',
                           'rockies',
                           'brewers',
                           'royals',
                           'cardinals',
                           'twins',
                           'angels',
                           'd-backs',
                           'padres',
                           'athletics',
                           'giants',
                           'mariners']

    def print_json(self, json):
        """ Pretty Print the JSON """
        print json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4,
                         separators=(',', ': '))

    def return_stats(self):
        """ Returns Stats in JSON format, get it from a local file if one
            is provided, otherwise hit the MLB API directly """
        if self.json_file:
            json_data = open(self.json_file).read()
            return json.loads(json_data)
        else:
            if self.debug:
                print 'Debug: Hitting URL ' + self.assemble_url()
            api_resp = requests.get(self.assemble_url())
            if api_resp.status_code != requests.codes.ok:
                sys.exit('API not responding the way we want: Response ' +
                         'Code ' + str(api_resp.status_code))
            else:
                return api_resp.json()

    def assemble_url(self):
        """ We need to assemble a URL to pull down stats with. """
        url = self.url_base + '/year_' + self.year + '/month_' + self.month \
            + '/day_' + self.day + '/master_scoreboard.json'
        return url

    def valid_team(self, team):
        """ Make sure it's a a valid team name """
        if team.lower() in self.team_names:
            return True
        else:
            return False

    def team_scores(self, team=None):
        """ Return Scores """

        # Placeholder for Scores String
        scores = ''

        # Convert team name to lower case if defined
        if team:
            team = team.lower()

        if team != None and not self.valid_team(team):
            sys.exit('"%s" is not a valid team name.' % team)

        for stat in self.json_stats['data']['games']['game']:
            home_team = stat['home_team_name'].lower()
            away_team = stat['away_team_name'].lower()

           # If it's not the home or the away team defined, and one
           # is defined, we try the next
            if (home_team != team and away_team != team) and team != None:
                 continue

            # The note summarizes the score 
            note = stat['alerts']['brief_text']
            scores = scores + note + '\n'

            ## Go through the stats file
            #for item in stat.items():
            #    # Get the Line Score
            #    if item[0] == 'linescore':
            #        home_score = stat[item[0]]['r']['home']
            #        away_score = stat[item[0]]['r']['away']

            #scores = scores + '%s (GB:%s) @ %s (GB:%s) :: '\
            #                  '(%s-%s) %s\n' % (away_team.title(),
            #                                    away_team_gb,
            #                                    home_team.title(),
            #                                    home_team_gb,
            #                                    away_score,
            #                                    home_score,
            #                                    game_status)

        return scores.rstrip()
