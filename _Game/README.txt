======================================================================
Run module checker to check you have the required dependencies first.
======================================================================
Python version 3.7.8 and earlier recommended
======================================================================

Clean and Code

A 2D top down pixel art game where you play as a janitor who has been hired at Cardiff Uni COMSC department. 
Knowing nothing about coding, can you survive the year and avoid being discovered?

Modules used:
pygame
multipledispatch
gspread 
oauth2Client 
PyOpenSSL
pandas

The game pulls data from a remote google drive so need 5-10s start up. Alternatively, go to spreadsheet.py and uncomment 
out "pass" in ScenarioDatabase() init function while commenting out:
    self.get_worksheets()

To build exe file type following command (will need pyinstaller):

pyinstaller --hidden-import multipledispatch --hidden-import gspread --hidden-import oauth2client --hidden-import pyopenssl --hidden-import pandas --hidden-import google-auth-oauthlib --hidden-import google-auth --hidden-import 
oauthlib --hidden-import requests-oauthlib --hidden-import oauth2client.service_account --onefile -w  main.py

To add an icon to your .exe file to do: pyinstaller -i [iconfile] [file_name]  . Making sure that your icon file is in the same directory that your cmd is in.

Then move the .exe file from dist into its own folder with resouces and delete dist and build folder and main.spec.