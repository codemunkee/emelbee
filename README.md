# emelbee

[![Build
Status](https://travis-ci.org/codemunkee/emelbee.svg?branch=master)](https://travis-ci.org/codemunkee/emelbee)

A tiny application that is used to return text messages with MLB game scores via Twilio. Once you start flask via the 'emelbee_api' script, you just need to configure your Twilio number to point at the web server running on port 5000. 

The app looks for strings coming in as GET requests in the body.  It knows
about two things, 'scores' and 'standings'.

If you send along 'scores all' you'll get all scores. If you send 'scores orioles' you'll get the Orioles
latest score information. Additionally, you can provide a date in the format 
@20150701 to get scores for a particular date.

Similarly, you can get standings information by entering something like
'Standings NL West'. Hoping to add more statistics in the future.

