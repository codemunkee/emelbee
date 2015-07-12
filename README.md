# emelbee

[![Build
Status](https://travis-ci.org/codemunkee/emelbee.svg?branch=master)](https://travis-ci.org/codemunkee/emelbee)

A tiny application that is used to return text messages with MLB game scores via Twilio. Once you start flask via the 'emelbee_api' script, you just need to configure your Twilio number to point at the web server running on port 5000. 

The app looks for strings coming in as GET requests in the body.  It knows about two things, 'scores' and 'standings'.

If you send along a team name you'll get that team's scores. If you repond with 'all' you'll get all team scores. 
Additionally, you can provide a date in the format @YYYYMMDD to get scores for a particular date.

Similarly, you can get standings information by entering something like 'Standings NL West'. Hoping to add more statistics in the future.
