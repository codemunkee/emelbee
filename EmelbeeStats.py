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
    def __init__(self, year, month, day, source, debug=False):

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
        self.json_file = 'master_scoreboard.json'

        # Get the JSON that this class needs
        self.json_stats = self.return_stats(source)

        # Team Names as referenced in the MLB API
        self.team_names = ['Pirates',
                           'White Sox',
                           'Orioles',
                           'Phillies',
                           'Tigers',
                           'Reds',
                           'Red Sox',
                           'Braves',
                           'Marlins',
                           'Yankees',
                           'Mets',
                           'Blue Jays',
                           'Rays',
                           'Nationals',
                           'Cubs',
                           'Indians',
                           'Rangers',
                           'Dodgers',
                           'Astros',
                           'Rockies',
                           'Brewers',
                           'Royals',
                           'Cardinals',
                           'Twins',
                           'Angels',
                           'D-backs',
                           'Padres',
                           'Athletics',
                           'Giants',
                           'Mariners']


    def print_json(self, json):
        """ Pretty Print the JSON """
        print json.dumps({'4': 5, '6': 7}, sort_keys=True, indent=4,
                         separators=(',', ': '))

    def return_stats(self, source):
        """ Returns Stats in JSON format, source can be 'local' (eg a file)
            or 'api', the MLB API """
        if source == 'local':
            json_data = open(self.json_file).read()
            return json.loads(json_data)
        elif source == 'api':
            if self.debug:
                print 'Debug: Hitting URL ' + self.assemble_url()
            api_resp = requests.get(self.assemble_url())
            if api_resp != requests.codes.ok:
                sys.exit('API not responding the way we want: Response ' +\
                         'Code ' + str(api_resp.status_code))
            else:
                return api_resp.json()
        else:
            sys.exit('Unable to open source: %s' % source)

    def assemble_url(self):
        """ We need to assemble a URL to pull down stats with. """
        url = self.url_base + '/year_' + self.year + '/month_' + self.month \
            + '/day_' + self.day + '/master_scoreboard.json'
        return url

    def print_scores(self):
        """ Print out all of the Scores """

        for stat in self.json_stats['data']['games']['game']:

            home_team = stat['home_team_name']
            # games behind
            home_team_gb = stat['home_games_back']
            away_team = stat['away_team_name']
            # games behind
            away_team_gb = stat['away_games_back']
            game_status = stat['status']['status']

            # Go through the stats file
            for item in stat.items():
                # Get the Line Score
                if item[0] == 'linescore':
                    home_score = stat[item[0]]['r']['home']
                    away_score = stat[item[0]]['r']['away']

            print '%s (GB:%s) @ %s (GB:%s) :: (%s-%s) %s' % (away_team,
                                                             away_team_gb,
                                                             home_team,
                                                             home_team_gb,
                                                             away_score,
                                                             home_score,
                                                             game_status)

