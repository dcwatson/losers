# losers

A Django app for running an NLF winner/loser pick league.

## Getting started

1.  `pyvenv venv`
2.  `. venv/bin/activate`
3.  `./manage.py migrate`
4.  `./manage.py createsuperuser`
5.  `./manage.py loadscores`
6.  `./manage.py runserver`
7.  Log in to http://127.0.0.1:8000/admin/ and create a League

## Updating scores

Set up a cron task to run every hour or so, calling `manage.py loadscores` to make sure scores stay updated,
new weeks get added, spreads are loaded, etc.
