# emelbee

A tiny application that is used to return text messages with MLB game scores via Twilio. Once you start flask via the 'emelbee_api' script, you just need to configure your Twilio number to point at the web server running on port 5000. 

The app looks for strings coming in as GET requests in the body. If it sees 'scores' it will return all of the day's scores. If it sees a team name it will return that team's score for the day, if it exits. If a user wants to get a score from a previous day they just include a string in the format of '@YYYYMMDD'. 

Similarly, you can get standings information by entering something like
'Standings NL West'. Hoping to add more statistics in the future.
