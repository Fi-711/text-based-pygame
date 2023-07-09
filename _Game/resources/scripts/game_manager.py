import os, insert_name
from singleton import Singleton
from player import Player
from story_manager import StoryManager
from scenario_manager import ScenarioManager
from grade_manager import GradeCalculator, ProfileMaker
from helper_functions import InputGetter, TextBoxMaker, StoryPointsUI, PopUp
from spreadsheet import ScenarioDatabase

# Controls game logic
class GameManager(metaclass=Singleton):
    
    # initialize all classes to be managed
    def __init__(self, frame, nextFrame, player_sprite):
        self.player = Player()
        self.scenario_database = ScenarioDatabase()
        self.event_transitions_db = self.scenario_database.event_transitions_data
        self.story_manager = StoryManager()
        self.scenario_manager = ScenarioManager()
        self.grade_calculator = GradeCalculator()
        self.profile_maker = ProfileMaker()
        self.text_box_maker = TextBoxMaker()
        self.input_getter = InputGetter()
        self.pop_up = PopUp()
        self.story_points_ui = StoryPointsUI()
        self.story_points_ui.story_score(0)
        self.frame = frame
        self.nextFrame = nextFrame
        self.player_sprite = player_sprite
        self.load_level()                                       # load_level starts story chain sequence  

    # global variables needed by other classes
    frame = None
    nextFrame = None
    player_sprite = None

    # private variables
    __current_branch = None
    __next_branch = None
    __play_intro = True

    # update story manager branches
    def update_branches(self):
        self.__current_branch = self.__next_branch
        self.__next_branch = self.story_manager.next_story_branch()

    # loads next scene
    def load_level(self):

        # check if intro has been played
        if self.__play_intro:
            self.scenario_manager.tutorial.tutorial_start()        
            self.__play_intro = False
        
        # update branch data
        self.__story_total = self.story_manager.current_score()
        self.update_branches()

        # check for triple branch scenario first i.e. [Lecture, Workshop, Staff Room]
        if len(self.__next_branch) > 1:         
            self.three_choice_branch()
            self.load_level()
        
        # otherwise send to right single length branch
        else:
            # load MEET THE BOSS branch
            if self.__next_branch[0] == "MEET THE BOSS":                
                self.scenario_manager.choose_meet_the_boss_scenario(self.frame, self.nextFrame, self.player_sprite)
                self.load_level()
            
            # load GRADE STUDENTS branch
            elif self.__next_branch[0] == "GRADE STUDENTS":
                self.scenario_manager.choose_grading_scenario({"correct" : 30, "wrong" : -10}, self.frame, self.nextFrame, self.player_sprite, number_of_tests = 5)                
                self.load_level()
            
            # load FREE PERIOD branch
            elif self.__next_branch[0] == "FREE PERIOD":
                self.scenario_manager.choose_free_period_scenario(self.frame, self.nextFrame, self.player_sprite)
                self.load_level()
            
            # load ENDING branch
            elif self.__next_branch[0] == "ENDING":
                self.scenario_manager.endings.chosen_ending()
            
            else:
                print("何何何何何何何何何何何何何何何何何何！！！！！！！！")
    
    
    # three branch choice - factored from triple branch code above
    def three_choice_branch(self):
        
        # if else statements pull info from spreadsheet to add flavour to transition text boxes
        if self.story_manager.current_story_level() == 2:
            self.text_box_maker.create_text_box(self.event_transitions_db["scenario_text"][0])
            res = self.input_getter.create_input_box("Type NEXT to continue.", ans=['next'])
            if res == 'next': self.text_box_maker.remove_text_box()

        elif self.story_manager.current_story_level() == 6:
            self.text_box_maker.create_text_box(self.event_transitions_db["scenario_text"][0])
            res = self.input_getter.create_input_box("Type NEXT to continue.", ans=['next'])
            if res == 'next': self.text_box_maker.remove_text_box()

        elif self.story_manager.current_story_level() == 9:
            self.text_box_maker.create_text_box(self.event_transitions_db["scenario_text"][3])
            res = self.input_getter.create_input_box("Type NEXT to continue.", ans=['next'])
            if res == 'next': self.text_box_maker.remove_text_box()

        # Generic command option test
        self.text_box_maker.create_text_box(['Please choose:','Go to the Lecture Hall',
                            'Go to the Staff Room','Go to the Workshop'], 50)

        res = self.input_getter.create_input_box("Choose: LECTURE, STAFF ROOM or WORKSHOP", 
                                            ans=['lecture', 'lecture hall', 'staff room', 'staff', 'workshop'])
        
        # load player's choice
        if res == 'lecture' or res == 'lecture hall':
            self.text_box_maker.remove_text_box()
            self.scenario_manager.choose_lecture_scenario(self.frame, self.nextFrame, self.player_sprite)
        elif res == 'staff room' or res == 'staff':
            self.text_box_maker.remove_text_box()            
            self.scenario_manager.choose_staff_room_scenario(self.frame, self.nextFrame, self.player_sprite)
        elif res == 'workshop':
            self.text_box_maker.remove_text_box()            
            self.scenario_manager.choose_workshop_scenario(self.frame, self.nextFrame, self.player_sprite)