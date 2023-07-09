import os#, gspread
#from oauth2client.service_account import ServiceAccountCredentials
from singleton import Singleton
from pathlib import Path
import pandas as pd

# Set root path and json file location
root_path = Path(__file__).parents[2]                                           # The root folder path
json_file = os.path.join(root_path, 'client_secret.json')                       # The location of json file
data_path = os.path.join(root_path, 'resources/data')                           # data folder path

class ScenarioDatabase(metaclass=Singleton):
    def __init__(self):
        pass
        #self.get_worksheets()
    
    intro_data = pd.read_csv(os.path.join(data_path,'intro.csv'))
    student_bios_data = pd.read_csv(os.path.join(data_path,'student_bios.csv'))
    meet_the_boss_data = pd.read_csv(os.path.join(data_path,'meet_the_boss.csv'))
    lecture_data = pd.read_csv(os.path.join(data_path,'lecture.csv'))
    staff_room_data = pd.read_csv(os.path.join(data_path,'staff_room.csv'))
    workshop_data = pd.read_csv(os.path.join(data_path,'workshop.csv'))
    endings_data = pd.read_csv(os.path.join(data_path,'endings.csv'))
    event_transitions_data = pd.read_csv(os.path.join(data_path,'event_transitions.csv'))

    #print(student_bios_data)

    # def get_worksheets(self):

    #     # use creds to create a client to interact with the Google Drive API
    #     scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
    #     creds = ServiceAccountCredentials.from_json_keyfile_name(json_file, scope)
    #     client = gspread.authorize(creds)

    #     # try to get data from google spreadsheet first
    #     try:
    #         # Find a worksheet by name - pull from google sheet
    #         __intro_sheet = client.open("Story Scenarios").worksheet('Intro')
    #         __student_bios_sheet = client.open("Story Scenarios").worksheet('Student Bios')
    #         __meet_the_boss_sheet = client.open("Story Scenarios").worksheet('Meet the Boss')
    #         __lecture_sheet = client.open("Story Scenarios").worksheet('Lecture')
    #         __staff_room_sheet = client.open("Story Scenarios").worksheet('Staff Room')
    #         __workshop_sheet = client.open("Story Scenarios").worksheet('Workshop')
    #         __endings_sheet = client.open("Story Scenarios").worksheet('Endings')
    #         __event_transitions_sheet = client.open("Story Scenarios").worksheet('Event Transitions')

    #         # Extract all data from google sheets
    #         self.intro_data = pd.DataFrame(__intro_sheet.get_all_records())
    #         self.student_bios_data = pd.DataFrame(__student_bios_sheet.get_all_records())
    #         self.meet_the_boss_data = pd.DataFrame(__meet_the_boss_sheet.get_all_records())
    #         self.lecture_data = pd.DataFrame(__lecture_sheet.get_all_records())
    #         self.staff_room_data = pd.DataFrame(__staff_room_sheet.get_all_records())
    #         self.workshop_data = pd.DataFrame(__workshop_sheet.get_all_records())
    #         self.endings_data = pd.DataFrame(__endings_sheet.get_all_records())
    #         self.event_transitions_data = pd.DataFrame(__event_transitions_sheet.get_all_records())

    #     # if fail, use local csv files
    #     except:
    #         # Print error message
    #         print("Couldn't find google server. Using local files.")
