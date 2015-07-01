#!/usr/bin/env python

import requests
import json
import sys
import re
import os


class EmelbeeStats:
    """ Pull down MLB stats in JSON from MLB's (mlb.com) free API.

            year, month, day - should be defined for the date you want
            to pull down stats for.

            score_file - set to location of cached local file for score
            information, it needs needs to be in teh format ber the MLB
            game day API, http://gd2.mlb.com/components/game/mlb

            standing_file - set to location of cached local file
            for standings, it needs to be in the format of
            https://erikberg.com/mlb/standings.json.

            debug - (optional)

        """
    def __init__(self, year, month, day, score_file=None, standing_file=None,
                 debug=False):

        # Current Working Directory
        cwd = os.path.dirname(__file__)

        # Date to Pull down stats for
        self.year = year
        self.month = month
        self.day = day

        # Debug Mode
        self.debug = debug

        # URL for the MLB API
        self.score_url_base = 'http://gd2.mlb.com/components/game/mlb'

        # JSON File with Standings information
        self.standing_file = cwd + '/data/standings.json'

        # JSON file with Sample Stats (if we don't want to reach out to
        # the MLB API directly for debugging and developing).
        self.score_file = cwd + '/data/scores.json'

        # Get the JSON that this class needs
        self.game_stats = self.return_stats()
        self.standing_stats = self.return_stats(self.standing_file)

        # List of Team Names
        self.team_names = self.get_team_names(cwd + '/conf/team_names.txt')

    def get_team_names(self, team_names_file):
        """ Read through team_names.txt to get valid team names """
        team_names = []
        text_file = open(team_names_file, 'r')
        for line in text_file:
            team_names.append(line.rstrip())
        return team_names

    def return_stats(self, filename=None):
        """ Returns Stats in JSON format, get it from a local file if one
            is provided, otherwise hit the MLB API directly """

        if filename:
            json_data = open(filename).read()
            return json.loads(json_data)

        else:
            # Go to the MLB API

            if self.debug:
                print 'Debug: Hitting URL ' + self.assemble_mlb_url()

            api_resp = requests.get(self.assemble_mlb_url())

            if self.debug:
                print 'Debug: %s API Response Code' % (api_resp.status_code)
            if api_resp.status_code != requests.codes.ok:
                return None
            else:
                return api_resp.json()

    def no_game_info_found(self, team=None):
        if team:
            return str('No game information found for %s on %s/%s/%s'
                       % (team.title(), self.month, self.day, self.year))
        else:
            return str('No game information found for ' +
                       '%s/%s/%s.' % (self.month,
                                      self.day,
                                      self.year))

    def assemble_mlb_url(self):
        """ We need to assemble an MLB URL to pull down stats with. """
        url = self.score_url_base + '/year_' + self.year + '/month_' +\
            self.month + '/day_' + self.day + '/master_scoreboard.json'
        return url

    def valid_team(self, team):
        """ Make sure it's a a valid team name """
        if team.lower() in self.team_names:
            return True
        else:
            return False

    def team_standings(self, league, division):
        """ Return Standings as String """
        standings = str()
        # specified team and league
        spec_league = league.lower()
        spec_division = division.lower()
        for team in self.standing_stats['standing']:
            if team['division'].lower() == spec_division and \
               team['conference'].lower() == spec_league:
                team_name = team['last_name']
                conference = team['conference']
                division = team['division']
                rank = team['ordinal_rank']
                gb = team['games_back']
                standings = standings + '%s %s - %s GB\n' % (rank,
                                                             team_name,
                                                             gb)
        return standings.rstrip()

    def team_scores(self, team=None):
        """ Return Scores as String """

        # Placeholder for Scores String
        scores = str()

        # Convert team name to lower case if defined
        if team:
            team = team.lower()

        # If a team is defined but it's not valid. We shouldn't
        # get here, but if the attribute gets overridden..
        if team is not None and not self.valid_team(team):
            sys.exit('"%s" is not a valid team name.' % team)

        # If we couldn't get any data
        if not self.game_stats and not team:
            return self.no_game_info_found()
        elif not self.game_stats and team:
            return self.no_game_info_found(team)

        # Sometimes there is JSON data defined but no actual games, bail out
        # if we run into that...
        if 'game' not in self.game_stats['data']['games']:
            return self.no_game_info_found()
        for stat in self.game_stats['data']['games']['game']:
            home_team = stat['home_team_name'].lower()
            away_team = stat['away_team_name'].lower()
            home_team_abbrev = stat['home_name_abbrev']
            away_team_abbrev = stat['away_name_abbrev']

            # If it's not the home or the away team defined, and one
            # is defined, we try the next
            if (home_team != team and away_team != team) and team is not None:
                continue

            # Game Status
            game_status = stat['status']['status']
            if self.debug:
                print 'Debug: %s' % game_status

            try:
                # The note summarizes the score
                note = stat['alerts']['brief_text']
                scores = scores + note + '\n'

            except KeyError:

                if 'linescore' in stat.keys():
                    home_score = stat['linescore']['r']['home']
                    away_score = stat['linescore']['r']['away']
                else:
                    home_score = 0
                    away_score = 0

                # If the game hasn't start, get the start time
                if re.search('Preview', game_status):
                    home_time = stat['home_time']
                    home_tz = stat['home_time_zone']
                    game_status = '%s %s' % (home_time, home_tz)

                scores = scores + '%s @ %s (%s-%s) - %s\n' % (away_team_abbrev,
                                                              home_team_abbrev,
                                                              away_score,
                                                              home_score,
                                                              game_status)
        if not scores and team:
            return self.no_game_info_found(team)
        elif not scores:
            return self.no_game_info_found()

        return scores.rstrip()
