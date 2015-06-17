#!/usr/bin/env python

import requests

class Emelbee:
    """ Pull down MLB stats from MLB's (mlb.com) free API. """

    def __self__(self):
        self.url_base = 'http://gd2.mlb.com/components/game/mlb/'

    def assemble_url(self, base_url, month, day, year):
        """ We need to assemble a URL to pull down stats with. """
        url = base_url + 'components/game/mlb/year_%s/month_%s
      
