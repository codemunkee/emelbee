from datetime import date
import EmelbeeTeams
import requests
import time
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
        self.debug = debug
        cwd = os.getcwd()

        # Date to Pull down stats for
        self.year = str(year)
        self.month = str(month)
        self.day = str(day)

        if self.debug:
            print 'Debug: Requested @%s/%s/%s' % (self.year, self.month,
                                                  self.day)

        self.current_time = time.time()
        self.current_year = str(date.today().year)
        self.current_month = str('{:02d}'.format(date.today().month))
        self.current_day = str('{:02d}'.format(date.today().day))
        if self.debug:
            print 'Debug: Today is @%s/%s/%s' % (self.current_year,
                                                 self.current_month,
                                                 self.current_day)

        # Max Cache Age - Max seconds before we refresh cache
        self.scores_max_cache_age = 60  # 1 minute
        self.standing_max_cache_age = 300  # 5 minutes

        self.score_url_base = 'http://gd2.mlb.com/components/game/mlb'
        self.standings_url = 'https://erikberg.com/mlb/standings.json'

        cache_dir = 'data'
        self.create_cache_dir(cache_dir)

        # JSON File with Standings information

        # Get the names of the cache file we should be using. For scores,
        # where we can get historical information, we create cache files
        # with the date baked into the filename. Standings are only available
        # for the most recent date
        self.standings_cache = cache_dir + '/' + 'standings_cache.json'
        if (self.year == self.current_year) \
           and (self.month == self.current_month) \
           and (self.day == self.current_day):
            self.scores_cache = cache_dir + '/' + 'scores_cache.json'
            self.today = True
        else:
            # Otherwise do append the date to the end of the cache filename
            self.scores_cache = cache_dir + '/' + 'scores_cache.json.' \
                                + self.year + self.month + self.day
            self.today = False

        self.team_names = EmelbeeTeams.get_team_names()

        # We need these headers so the APIs can identify us as a legit user
        self.headers = {
             'User-Agent': 'https://github.com/codemunkee/emelbee',
             'From': 'codemunkee@gmail.com'}

    def file_exists(self, filename):
        """ Check to see if a file exists """
        if os.path.isfile(filename):
            return True
        else:
            return False

    def create_cache_dir(self, dirname):
        """ Create a cache directory if it doesn't already exist """
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    def cache_file_age(self, cache_file):
        """ Get score cache age """
        mtime = os.path.getmtime(cache_file)
        return self.current_time - mtime

    def scores_from_api(self):
        if self.debug:
            print 'Debug: Hitting URL ' + self.assemble_mlb_url()
        api_resp = requests.get(self.assemble_mlb_url(), headers=self.headers)
        if self.debug:
            print 'Debug: %s API Response Code' % (api_resp.status_code)
        if api_resp.status_code != requests.codes.ok:
            return None
        else:
            return api_resp.json()

    def standings_from_api(self):
        if self.debug:
            print 'Debug: Hitting URL ' + self.standings_url
        api_resp = requests.get(self.standings_url, headers=self.headers)
        if self.debug:
            print 'Debug: %s API Response Code' % (api_resp.status_code)
        if api_resp.status_code != requests.codes.ok:
            return None
        else:
            return api_resp.json()

    def return_standings(self, filename=None):
        """ Returns Standings in JSON format from
            https://erikberg.com/mlb/standings.json """
        if filename:
            return self.read_cache(filename)
        else:
            # Does our standings cache exist?
            if self.file_exists(self.standings_cache):
                if self.debug:
                    print 'Debug: Standings Cache file (%s) exists.' \
                          % (self.standings_cache)
                # Is our local cache up to date?
                age_secs = self.cache_file_age(self.standings_cache)
                if self.debug:
                    print 'Debug: Standings Cache file age: ' + str(age_secs)
                if age_secs > self.standing_max_cache_age:
                    standings = self.standings_from_api()
                    self.write_cache(standings, self.standings_cache)
                    return standings
                else:
                    return self.read_cache(self.standings_cache)

            else:
                if self.debug:
                    print 'Debug: Standings cache file does NOT exist,' \
                          + 'going to the Erik Berg API.'
                standings = self.standings_from_api()
                self.write_cache(standings, self.standings_cache)
                return standings

    def write_cache(self, json_blob, cache_file_name):
        """ Write the JSON blob to cache file """
        if self.debug:
            print 'Debug: Writing cache to %s' % cache_file_name
        with open(cache_file_name, 'w') as cache_file:
                json.dump(json_blob, cache_file)

    def read_cache(self, cache_file):
        """ Read the JSON in a cache file """
        try:
            json_data = open(cache_file).read()
            return json.loads(json_data)
        except IOError:
            print 'Error: Unable to open "%s"' % cache_file
            raise

    def return_scores(self, filename=None):
        """ Returns scores in JSON format, get it from a local file if one
            is provided, otherwise check our local cache, if that doesn't
            work hit the API directly"""
        if filename:
            try:
                json_data = open(filename).read()
                return json.loads(json_data)
            except IOError:
                print 'Error: Unable to open "%s"' % filename
                raise
        else:
            # Does our scores cache exist?
            if self.file_exists(self.scores_cache):
                if self.debug:
                    print 'Debug: Scores Cache file (%s) exists.' \
                          % self.scores_cache
                # Only get a new copy of the cache if it's today, otherwise
                # the stale information is fine (the past doesn't change)
                if self.today:
                    # Is our local cache up to date?
                    age_secs = self.cache_file_age(self.scores_cache)
                    if self.debug:
                        print 'Debug: Scores Cache file age: ' + str(age_secs)

                    if age_secs > self.scores_max_cache_age:
                        scores = self.scores_from_api()
                        self.write_cache(scores, self.scores_cache)
                        return scores
                    else:
                        return self.read_cache(self.scores_cache)
                else:
                    return self.read_cache(self.scores_cache)
            else:
                if self.debug:
                    print 'Debug: Score Cache file does NOT exist, going to' \
                          + ' the MLB API.'
                scores = self.scores_from_api()
                self.write_cache(scores, self.scores_cache)
                return scores

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

    def team_standings(self, league, division):
        """ Return Standings as String """
        json_standings = self.return_standings()
        team_standings = str()
        # specified team and league
        spec_league = league.lower()
        spec_division = division.lower()
        for team in json_standings['standing']:
            if team['division'].lower() == spec_division and \
               team['conference'].lower() == spec_league:
                team_name = team['last_name']
                conference = team['conference']
                division = team['division']
                rank = team['ordinal_rank']
                gb = team['games_back']
                team_standings = team_standings + '%s %s - %s GB\n' %\
                                                  (rank, team_name, gb)
        return team_standings.rstrip()

    def team_scores(self, team=None):
        """ Return Scores as String """
        # Placeholder for Scores String
        json_scores = self.return_scores()
        team_scores = str()

        if team:
            team = team.lower()

        if team:
            if not EmelbeeTeams.valid_name(team):
                sys.exit('"%s" is not a valid team name.' % team)

        # If we couldn't get any data
        if not json_scores and not team:
            return self.no_game_info_found()
        elif not json_scores and team:
            return self.no_game_info_found(team)

        # Sometimes there is JSON data defined but no actual games, bail out
        # if we run into that...
        if 'game' not in json_scores['data']['games']:
            return self.no_game_info_found()

        # Go through the scores JSON
        for stat in json_scores['data']['games']['game']:
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

            try:
                # The note summarizes the score
                note = stat['alerts']['brief_text']
                team_scores = team_scores + note + '\n'

            except KeyError:

                if 'linescore' in stat.keys():
                    home_score = stat['linescore']['r']['home']
                    away_score = stat['linescore']['r']['away']
                else:
                    home_score = 0
                    away_score = 0

                # If the game hasn't started, get the start time
                if re.search('Preview', game_status):
                    home_time = stat['home_time']
                    home_tz = stat['home_time_zone']
                    game_status = '%s %s' % (home_time, home_tz)

                team_scores = team_scores + '%s @ %s (%s-%s)'\
                                            ' - %s\n' % (away_team_abbrev,
                                                         home_team_abbrev,
                                                         away_score,
                                                         home_score,
                                                         game_status)
        if not team_scores and team:
            return self.no_game_info_found(team)
        elif not team_scores:
            return self.no_game_info_found()

        return team_scores.rstrip()
