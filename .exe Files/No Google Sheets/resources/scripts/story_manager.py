import os, insert_name, numpy
from singleton import Singleton
from multipledispatch import dispatch
from pygame_functions import *
from helper_functions import TextBoxMaker, InputGetter, StoryPointsUI, PopUp, JobPointsUI
from pathlib import Path
from spreadsheet import ScenarioDatabase

resource_path = Path(__file__).parents[1]               # The resource folder path
image_path = os.path.join(resource_path, 'images')      # The image folder path
sfx_path = os.path.join(resource_path, 'sfx')           # The image folder path

# Images
job_security = os.path.join(image_path, 'job_security.png')

# SFX
marked_bio_correct_sound = makeSound(os.path.join(sfx_path, 'marked_bio_correct.wav'))
marked_bio_wrong_sound = makeSound(os.path.join(sfx_path, 'marked_bio_wrong.wav'))
game_over_sound = makeSound(os.path.join(sfx_path, 'game_over.wav'))

# Class which handles all story related elements
class StoryManager(metaclass=Singleton):
    def __init__(self):
        self.text_box_maker = TextBoxMaker()
        self.input_getter = InputGetter()
        self.story_points_ui = StoryPointsUI()
        self.job_points_ui = JobPointsUI()
        self.pop_up = PopUp()
        self.scenario_database = ScenarioDatabase()
        self.event_transitions_db = self.scenario_database.event_transitions_data
        self.update_job_security(self.__job_security)

    # overload function using multipledispatch - this way only one update_story() needed
    # update total with grade scene
    @dispatch(bool, bool, dict)
    def update_story(self, player_choice, result, story_points):
        self.player_choice = player_choice
        self.result = result
        self.story_points = story_points
        self.__update_score()

    # update total with non-grade scene
    @dispatch(int)
    def update_story(self, story_points):
        self.story_points = story_points
        self.__update_score2()

    @dispatch(numpy.int64)                                  # as using pandas, now need to handle int64
    def update_story(self, story_points):
        self.story_points = story_points.astype(numpy.int64)
        self.__update_score2()

    # points total, job security and story branches
    __story_total = 0
    __job_security = 100
    __story_level = -1
    __story_branches = {
        0 : ["GRADE STUDENTS"],
        1 : ["MEET THE BOSS"],
        2 : ["LECTURE", "STAFF ROOM", "WORKSHOP"],        
        3 : ["GRADE STUDENTS"],
        4 : ["MEET THE BOSS"],
        5 : ["FREE PERIOD"],
        6 : ["LECTURE", "STAFF ROOM", "WORKSHOP"],
        7 : ["MEET THE BOSS"],
        8 : ["GRADE STUDENTS"],
        9 : ["LECTURE", "STAFF ROOM", "WORKSHOP"],
        10 : ["ENDING"]
    }

    # Job security functions
    def current_job_security(self):
        return self.__job_security
    
    # updates JS points with red pixel numbers
    def update_job_security(self, number):
        if number <= 0:
            if self.__job_security + number < 0: self.__job_security = 0
            else: self.__job_security += number

        else:
            if self.__job_security + number > 100: self.__job_security = 100
            else: self.__job_security += number
        
        self.job_points_ui.job_score(self.__job_security)

        # If JS <= 0 --> GameOver
        if self.__job_security <= 0:
            self.text_box_maker.remove_text_box() 
            self.text_box_maker.create_text_box(self.event_transitions_db["scenario_text"][4], linespacing=32, fontsize=50, fontColour=(255,0,0), width=60)            
            pauseMusic()
            playSound(game_over_sound)
            endWait()

    # Points from scoring Grade Scenarios
    def __points_scored(self):
        playSound(marked_bio_correct_sound) if self.player_choice == self.result else playSound(marked_bio_wrong_sound)
        return self.story_points["correct"] if self.player_choice == self.result else self.story_points["wrong"]
    
    def __update_score(self):
        if self.__story_total + self.__points_scored() < 0: self.__story_total = 0 
        else: self.__story_total += self.__points_scored()
        
        self.pop_up.pop_up_red_points(self.__points_scored()) if self.__points_scored() <= 0 else self.pop_up.pop_up_green_points(self.__points_scored())

        # updates story score UI
        self.story_points_ui.story_score(self.__story_total)

    # Points scored from other scenarios
    def __update_score2(self):

        if self.__story_total + self.story_points < 0: self.__story_total = 0 
        else: self.__story_total += self.story_points
        
        self.pop_up.pop_up_red_points(self.story_points) if self.story_points <= 0 else self.pop_up.pop_up_green_points(self.story_points)

        # Updates story score UI
        self.story_points_ui.story_score(self.__story_total)
    
    # allows user to call total from outside class
    def current_score(self):
        return self.__story_total

    # Story Branches
    # returns chosen story branch
    def __current_story_branch(self):
        self.__story_level += 1
        return self.__story_level
    
    # suggests next story branch - game manager will handle what is done with said branch
    def next_story_branch(self):
        return self.__story_branches[self.__current_story_branch()]

    # returns current branch
    def current_story_level(self):
        return self.__story_level
