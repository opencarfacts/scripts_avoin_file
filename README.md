Avoin file
==========

This repository contains scripts to check and improve this file:
 `http://www.trafi.fi/en/services/open_data`

Run `make_it_english.sh` script first (the first argument needs to be the
path to the csv file

Script check_constructors
=========================

You need python to run this script.
You can run it with `./check_constructors.py path_to_file`
It will produce stats about this file, and produce a file of unfound constructors
at /tmp/constructors.unfound
The game is to add aliases in map_wmi_constructor to have a empty unfound file!
Goodluck
