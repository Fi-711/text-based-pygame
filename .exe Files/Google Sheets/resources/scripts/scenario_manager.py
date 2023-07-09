import time, random, insert_name
from singleton import Singleton
from story_manager import StoryManager
from helper_functions import InputGetter
from grade_manager import ProfileMaker, GradeCalculator
from student_generator import StudentGenerator
from helper_functions import TextBoxMaker, InputGetter
from spreadsheet import ScenarioDatabase
from player import Player
from pygame_functions import *
from pathlib import Path

resource_path = Path(__file__).parents[1]                   # The resource folder path
image_path = os.path.join(resource_path, 'images')          # The images folder path
music_path = os.path.join(resource_path, 'music')           # The music folder path
sfx_path = os.path.join(resource_path, 'sfx')               # The sfx folder path

# Images
boss_img = os.path.join(image_path, 'boss.png')
office_img = os.path.join(image_path, 'office_room.png')
workshop_img = os.path.join(image_path, 'workshop_room.png')
lecture_img = os.path.join(image_path, 'lecture_room.png')
staff_room_img = os.path.join(image_path, 'staff_room.png')
meet_the_boss_img = os.path.join(image_path, 'meet_the_boss_room.png')
grass_img = os.path.join(image_path, 'grass.png')

# Music
ending_music = os.path.join(music_path, 'ending.mp3')
free_period_music = os.path.join(music_path, 'free_period.mp3')
lecture_music = os.path.join(music_path, 'lecture.mp3')
meet_the_boss_music = os.path.join(music_path, 'meet_the_boss.mp3')
office_music = os.path.join(music_path, 'office.mp3')
staff_room_music = os.path.join(music_path, 'staff_room.mp3')
workshop_music = os.path.join(music_path, 'workshop.mp3')

# Sound Effects
bio_change_sound = makeSound(os.path.join(sfx_path, 'bio_change.wav'))
dial_clicker_sound = makeSound(os.path.join(sfx_path, 'dial_click.wav'))
ending_drum_roll_sound = makeSound(os.path.join(sfx_path, 'ending_drum_roll.wav'))
game_over_sound = makeSound(os.path.join(sfx_path, 'game_over.wav'))
got_the_power_sound= makeSound(os.path.join(sfx_path, 'got_the_power.wav'))
grading_session_sound = makeSound(os.path.join(sfx_path, 'grading_session.wav'))
gulp_sound = makeSound(os.path.join(sfx_path, 'gulp.wav'))
incorrect_safe_guess_sound = makeSound(os.path.join(sfx_path, 'incorrect_safe_guess.wav'))
pass_fail_stamp = makeSound(os.path.join(sfx_path, 'pass_fail_stamp.wav'))
piano_sound = makeSound(os.path.join(sfx_path, 'piano_sound.wav'))
safe_cracked_sound = makeSound(os.path.join(sfx_path, 'safe_cracked.wav'))
superbass_sound = makeSound(os.path.join(sfx_path, 'superbass.wav'))

player_name = "Default"

# Easter egg
developers_names = ["NAFIS AHMED", "OPHELIA CHAN", "SELIM CELIK", "CALLUM GREER", 
                    "BENJAMIN MEADOWS", "ELLIOT KEMPSON", "HARRISON CASEY"]

def get_name():
    global player_name
    return player_name

# Manages all scenario paths
class ScenarioManager(metaclass=Singleton):
    def __init__(self):
        self.tutorial = Tutorial()
        self.grading_scenario = GradingScenarios()
        self.lecture_scenario = LectureScenarios()
        self.staff_room_scenario = StaffRoomScenarios()
        self.workshop_scenario = WorkshopScenarios()
        self.meet_the_boss_scenario = MeetTheBossScenarios()
        self.free_period_scenario = FreePeriodScenarios()
        self.endings = Endings()
        self.student_generator = StudentGenerator()
        self.player = Player()

    __lecture_branches_played = []
    __lecture_branches_available = [0,1,2,3]
    __staff_room_branches_played = []
    __staff_room_branches_available = [0,1,2,3]
    __workshop_branches_played = []
    __workshop_branches_available = [0,1,2,3]
    __meet_the_boss_branches_played = []
    __meet_the_boss_branches_available = [0,1,2]

    __safe_cracking_played = False
    __reset_background = False
    __workshop_free_movement_played = False

    __chosen_branch = None

    # choose tutorial
    def choose_tutorial(self):
        self.tutorial.tutorial_start()

    # choose grade scenario branch
    def choose_grading_scenario(self, outcomes, frame, nextFrame, player_sprite, profile=None, number_of_tests = 5, istutorial = False):
        # move player to right room
        self.player.move([340, 805], frame, nextFrame, player_sprite)
        
        # generates a profile if none given
        if profile == None: profile = self.student_generator.generate_profile()
        
        # play room music
        makeMusic(office_music)
        playMusic()
        
        # start a grading scenario by feeding it the above generated profile
        self.grading_scenario.generate_marking_session(outcomes=outcomes, profile=profile, 
                        number_of_tests = number_of_tests, istutorial=istutorial)

    # choose lecture scenario branch
    def choose_lecture_scenario(self, frame, nextFrame, player_sprite):
        
        # move to lecture room
        self.player.move([3200, 480], frame, nextFrame, player_sprite)
        self.player.current_room = "lecture"
        
        # play music
        makeMusic(lecture_music)
        playMusic()

        # randomly choose a lecture branch
        self.__chosen_branch = random.randint(0,3)

        # check if branch already chosen, if so try again
        while self.__chosen_branch not in self.__lecture_branches_available:
            self.__chosen_branch = random.randint(0,3)

        # update branches played and not played in private variables at top of this function
        self.__lecture_branches_played.append(self.__chosen_branch)
        self.__lecture_branches_available.remove(self.__chosen_branch)

        # load the selected branch
        self.lecture_scenario.text_only_scenario(self.__chosen_branch)

    # choose staff_room branch
    def choose_staff_room_scenario(self, frame, nextFrame, player_sprite):

        # move player to staff room
        self.player.move([4480, 480], frame, nextFrame, player_sprite)
        self.player.current_room = "staff_room"
        
        # play music
        makeMusic(staff_room_music)
        playMusic()

        # randomly choose a staff room branch
        self.__chosen_branch = random.randint(0,3)

        # check if branch already chosen, if so try again
        while self.__chosen_branch not in self.__staff_room_branches_available:
            self.__chosen_branch = random.randint(0,3)
        
        # update branches played and not played in private variables at top of this function
        self.__staff_room_branches_played.append(self.__chosen_branch)
        self.__staff_room_branches_available.remove(self.__chosen_branch)

        # load the selected branch
        self.staff_room_scenario.text_only_scenario(self.__chosen_branch)

    # choose work_shop branch
    def choose_workshop_scenario(self, frame, nextFrame, player_sprite):

        # move to workshop
        self.player.move([1920, 480], frame, nextFrame, player_sprite)
        self.player.current_room = "workshop"
        
        # play music
        makeMusic(workshop_music)
        playMusic()

        # randomly choose a staff room branch
        self.__chosen_branch = random.randint(0,3)

        # check if branch already chosen, if so try again
        while self.__chosen_branch not in self.__workshop_branches_available:
            self.__chosen_branch = random.randint(0,3)

        # update branches played and not played in private variables at top of this function
        self.__workshop_branches_played.append(self.__chosen_branch)
        self.__workshop_branches_available.remove(self.__chosen_branch)

        # before loading selected room - check if bespoke scenario has been played
        if not self.__workshop_free_movement_played:
            self.workshop_scenario.workshop_scenario(frame, nextFrame, player_sprite)
            self.__workshop_free_movement_played = True
        else:
            self.workshop_scenario.text_only_scenario(self.__chosen_branch)


    # choose meet_the_boss branch
    def choose_meet_the_boss_scenario(self, frame, nextFrame, player_sprite):
        # lot of code here - resetting background images so new images now has a boss
        # character - backgrounds have to be reset than simply placing a sprite of the boss as backgrounds are
        # scrolled, if a sprite was just placed, they would move with the player! 
        
        # first check if safe cracking game has been played
        if self.__safe_cracking_played:
            # check if background has been changed for scenarios after safe cracking one
            if not self.__reset_background:
                self.player.move([640, 480], frame, nextFrame, player_sprite)
                setBackgroundImage([[office_img, grass_img, meet_the_boss_img, staff_room_img, lecture_img, workshop_img],                            # background images in [5x2]
                            [grass_img, grass_img, grass_img, grass_img, grass_img, grass_img]])
                self.__reset_background = True
            
            # move layer in front of boss if safe cracking scenario done
            self.player.move([6090, 745], frame, nextFrame, player_sprite)
        
        # otherwise move player to middle of room for safe cracking scenario
        else:
            self.player.move([5760, 480], frame, nextFrame, player_sprite)
        
        self.player.current_room = "bosses_office"
        
        # room play music
        makeMusic(meet_the_boss_music)
        playMusic()

        # randomly choose a staff room branch
        self.__chosen_branch = random.randint(0,3)

        # check if branch already chosen, if so try again
        while self.__chosen_branch not in self.__meet_the_boss_branches_available:
            self.__chosen_branch = random.randint(0,3)

        # update branches played and not played in private variables at top of this function
        self.__meet_the_boss_branches_played.append(self.__chosen_branch)
        self.__meet_the_boss_branches_available.remove(self.__chosen_branch)

        # load safe cracking scenario if available, otherwise load text based scenario
        if not self.__safe_cracking_played:
            self.meet_the_boss_scenario.safe_cracking_scenario(frame, nextFrame, player_sprite)
            self.__safe_cracking_played = True
        else:
            self.meet_the_boss_scenario.text_only_scenario(self.__chosen_branch)

    # Free period
    def choose_free_period_scenario(self, frame, nextFrame, player_sprite):
        
        # Move back to office
        self.player.current_room = "office"
        self.player.move([640, 480], frame, nextFrame, player_sprite)
        
        # play music
        makeMusic(free_period_music)
        playMusic()

        # load the free period scenario
        self.free_period_scenario.office_scenario(frame, nextFrame, player_sprite)

    # choose ending
    def choose_ending(self, frame, nextFrame, player_sprite):
        # move back to office and play ending
        self.player.move([640, 480], frame, nextFrame, player_sprite)
        self.endings.chosen_ending()


# Generates tutorial scenario
class Tutorial(metaclass=Singleton):
    def __init__(self):
        self.scenario_database = ScenarioDatabase()
        self.__intro_db = self.scenario_database.intro_data
        self.grading_scenario = GradingScenarios()
        self.text_box_maker = TextBoxMaker()
        self.input_getter = InputGetter()        

    __intro_db =  None

    # Prints out intro and asks the player if they want a tutorial or not
    def tutorial_start(self):
        
        jonathan_profile = {
            "name" : "Jonathan",
            "gender" : "male",
            "location" : "england",
            "hair colour" : "brown",
            "glasses" : "no",
            "personality" : "clown",
            "style" : "rugby",
            "dob" : "31/01/2015",
            "phone" : "029 999 - hehe, 1000 iq",
            "bio" : self.__intro_db["desc"][0],
            "comments" : self.__intro_db["extra"][0]
        }

        self.text_box_maker.scrollable_text_box([self.__intro_db["intro_text"][0], self.__intro_db["intro_text_2"][0]]) 
        self.input_getter.create_input_box("Type 'NEXT' to continue.", ans=['next'])
        
        global player_name
        c = False
        
        # gets player's name
        while not c:
            player_name = self.input_getter.create_input_box("Please enter your name: ", set_ans=False)
            confirm = self.input_getter.create_input_box(f"Is {player_name} ok? yes/no", ans=['yes', 'no', 'y', 'n'])
            if confirm == "yes" or confirm == "y":
                c = True

        # tutorial text
        self.text_box_maker.scroll_right()
        self.input_getter.create_input_box("Ready to start? yes/no", ans=['yes', 'y'])
        self.text_box_maker.remove_text_box()
        self.text_box_maker.create_text_box(["Would you like to start with a tutorial?", "Answer with yes/no"], 50)
        
        res = self.input_getter.create_input_box("Answer with yes/no", ans=['yes', 'no', 'y', 'n'])

        if (res == "yes" or res == 'y'):
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box(["The following is the bio of an... interesting character.",
                                                "Pass? Fail? to quote the 90s band SNAP...", "I'VE GOT THE POWER!", 
                                                "Don't worry, you won't be scored for your answer but keep an ear out for the", 
                                                "sound as it will tell you if you were right or wrong."], 50)
            # play got the power sfx
            playSoundAndWait(got_the_power_sound, 1000)
            
            self.input_getter.create_input_box("Type 'NEXT' to continue.", ans=['next'])
            self.text_box_maker.remove_text_box()

            self.grading_scenario.generate_marking_session({"correct" : 0, "wrong" : 0}, 
                        jonathan_profile, number_of_tests = 1, istutorial=True)
        
        elif (res == "no" or res == 'n'):
            self.text_box_maker.remove_text_box()
            return

# Generates lecture scenarios
class LectureScenarios(metaclass=Singleton):
    def __init__(self):
        self.scenario_database = ScenarioDatabase()
        self.__lecture_db = self.scenario_database.lecture_data
        self.story_manager = StoryManager()
        self.text_box_maker = TextBoxMaker()
        self.input_getter = InputGetter()  

    __lecture_db =  None                                    #scenario_database.lecture_data

    # code for generating text based only scenarios
    def text_only_scenario(self, number_in_db):
        # insert player's name into bios where [player] appears
        global player_name
        self.text_box_maker.create_text_box(insert_name.insert_name(self.__lecture_db["scenario_text"][number_in_db], player_name), 33)
        
        response = self.input_getter.create_input_box("Type 'NEXT' to continue.", ans=['next'])

        if response == 'next': self.text_box_maker.remove_text_box()

        # standard 3 choice text box using data pulled from spreadsheet
        self.text_box_maker.create_text_box([ f"Choice 1: {self.__lecture_db['choice_1'][number_in_db]}", 
                                                f"Choice 2: {self.__lecture_db['choice_2'][number_in_db]}", 
                                                f"Choice 3: {self.__lecture_db['choice_3'][number_in_db]}"], 50)
        
        res = self.input_getter.create_input_box("Choose: CHOICE 1, CHOICE 2, CHOICE 3", 
                        ans=['choice 1', 'choice one', '1', 'one', 'choice 2', 'choice two', '2', 'two',
                        'choice 3', 'choice three', '3', 'three'])

        # update story manager with their choices
        if (res == "choice 1" or res == "choice one" or res == "one" or res == "1"):
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box(self.__lecture_db['outcome_choice_1'][number_in_db])
            self.story_manager.update_story(self.__lecture_db['points_choice_1'][number_in_db])
            self.story_manager.update_job_security(self.__lecture_db['js_points_choice_1'][number_in_db])            
        
        elif (res == "choice 2" or res == "choice two" or res == "two" or res == "2"):
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box(self.__lecture_db['outcome_choice_2'][number_in_db])
            self.story_manager.update_story(self.__lecture_db['points_choice_2'][number_in_db])
            self.story_manager.update_job_security(self.__lecture_db['js_points_choice_2'][number_in_db]) 
        
        elif (res == "choice 3" or res == "choice three" or res == "three" or res == "3"):
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box(self.__lecture_db['outcome_choice_3'][number_in_db])
            self.story_manager.update_story(self.__lecture_db['points_choice_3'][number_in_db])
            self.story_manager.update_job_security(self.__lecture_db['js_points_choice_3'][number_in_db])

        # remove text box and add input to continue
        self.input_getter.create_input_box("Type 'NEXT' to continue.", ans=['next'])
        self.text_box_maker.remove_text_box()

# Generates staff room scenarios
class StaffRoomScenarios(metaclass=Singleton):
    def __init__(self):
        self.scenario_database = ScenarioDatabase()
        self.__staff_room_db = self.scenario_database.staff_room_data
        self.story_manager = StoryManager()
        self.text_box_maker = TextBoxMaker()
        self.input_getter = InputGetter()  

    __staff_room_db =  None                         #scenario_database.staff_room_data

    # generate text based scenarios from spreadsheet data
    def text_only_scenario(self, number_in_db):

        # replace [player] with player name where needed
        global player_name
        self.text_box_maker.create_text_box(insert_name.insert_name(self.__staff_room_db["scenario_text"][number_in_db], player_name), 33)
        
        response = self.input_getter.create_input_box("Type 'NEXT' to continue.", ans=['next'])

        if response == 'next': self.text_box_maker.remove_text_box()

        self.text_box_maker.create_text_box([ f"Choice 1: {self.__staff_room_db['choice_1'][number_in_db]}", 
                                                f"Choice 2: {self.__staff_room_db['choice_2'][number_in_db]}", 
                                                f"Choice 3: {self.__staff_room_db['choice_3'][number_in_db]}"], 50)
        
        res = self.input_getter.create_input_box("Choose: CHOICE 1, CHOICE 2, CHOICE 3", 
                        ans=['choice 1', 'choice one', '1', 'one', 'choice 2', 'choice two', '2', 'two',
                        'choice 3', 'choice three', '3', 'three'])
        
        if (res == "choice 1" or res == "choice one" or res == "one" or res == "1"):
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box(insert_name.insert_name(self.__staff_room_db['outcome_choice_1'][number_in_db], player_name))
            self.story_manager.update_story(self.__staff_room_db['points_choice_1'][number_in_db])
            self.story_manager.update_job_security(self.__staff_room_db['js_points_choice_1'][number_in_db])            
        
        elif (res == "choice 2" or res == "choice two" or res == "two" or res == "2"):
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box(insert_name.insert_name(self.__staff_room_db['outcome_choice_2'][number_in_db], player_name))
            self.story_manager.update_story(self.__staff_room_db['points_choice_2'][number_in_db])
            self.story_manager.update_job_security(self.__staff_room_db['js_points_choice_2'][number_in_db]) 
        
        elif (res == "choice 3" or res == "choice three" or res == "three" or res == "3"):
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box(insert_name.insert_name(self.__staff_room_db['outcome_choice_3'][number_in_db], player_name))
            self.story_manager.update_story(self.__staff_room_db['points_choice_3'][number_in_db])
            self.story_manager.update_job_security(self.__staff_room_db['js_points_choice_3'][number_in_db])

        self.input_getter.create_input_box("Type 'NEXT' to continue.", ans=['next'])
        self.text_box_maker.remove_text_box()

# Generates workshop scenarios
class WorkshopScenarios(metaclass=Singleton):
    def __init__(self):
        self.scenario_database = ScenarioDatabase()
        self.__workshop_db = self.scenario_database.workshop_data
        self.story_manager = StoryManager()
        self.text_box_maker = TextBoxMaker()
        self.input_getter = InputGetter()
        self.player = Player()

    __workshop_db =  None  #scenario_database.workshop_data

    __reception = True
    __study_room = True
    __computer_lab = True
    __lockers = True

    # generates standard text based scenarios
    def text_only_scenario(self, number_in_db):
        self.text_box_maker.create_text_box(self.__workshop_db["scenario_text"][number_in_db], 33)
        
        response = self.input_getter.create_input_box("Type 'NEXT' to continue.", ans=['next'])

        if response == 'next': self.text_box_maker.remove_text_box()

        self.text_box_maker.create_text_box([ f"Choice 1: {self.__workshop_db['choice_1'][number_in_db]}", 
                                                f"Choice 2: {self.__workshop_db['choice_2'][number_in_db]}", 
                                                f"Choice 3: {self.__workshop_db['choice_3'][number_in_db]}"], 50)
        
        res = self.input_getter.create_input_box("Choose: CHOICE 1, CHOICE 2, CHOICE 3", 
                        ans=['choice 1', 'choice one', '1', 'one', 'choice 2', 'choice two', '2', 'two',
                        'choice 3', 'choice three', '3', 'three'])

        if (res == "choice 1" or res == "choice one" or res == "one" or res == "1"):
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box(self.__workshop_db['outcome_choice_1'][number_in_db])
            self.story_manager.update_story(self.__workshop_db['points_choice_1'][number_in_db])
            self.story_manager.update_job_security(self.__workshop_db['js_points_choice_1'][number_in_db])            
        
        elif (res == "choice 2" or res == "choice two" or res == "two" or res == "2"):
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box(self.__workshop_db['outcome_choice_2'][number_in_db])
            self.story_manager.update_story(self.__workshop_db[number_in_db]['points_choice_2'])
            self.story_manager.update_job_security(self.__workshop_db['js_points_choice_2'][number_in_db]) 
        
        elif (res == "choice 3" or res == "choice three" or res == "three" or res == "3"):
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box(self.__workshop_db['outcome_choice_3'][number_in_db])
            self.story_manager.update_story(self.__workshop_db['points_choice_3'][number_in_db])
            self.story_manager.update_job_security(self.__workshop_db['js_points_choice_3'][number_in_db])

        self.input_getter.create_input_box("Type 'NEXT' to continue.", ans=['next'])
        self.text_box_maker.remove_text_box()

    # geneartes a bespoke movement based workshop scenario
    def workshop_scenario(self, frame, nextFrame, player_sprite):
        self.text_box_maker.remove_text_box()
        
        if self.player.current_room == "workshop":
            
            self.text_box_maker.create_choice_box(["You can move to:", "RECEPTION", "STUDY AREA",
                                                "COMPUTER LAB", "LOCKERS", "EXIT"], linespacing=21, fontsize=26)

            res = self.input_getter.create_input_box("Enter a command: ", ans=['reception', 'study area', 'computer lab',
                                    'lockers', 'exit'])

            # Hardcoded locations - when using dictionary bugs with skipping locations after one full cycle
            # ??? to do with frame changing causing dictionary misreads???
            if res == "reception":
                self.player.move([1605, 555], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("You make your way to reception and notice the good looking receptionist. They give you a coquettish wink. They might be interested in you. Do you ask them for their number?", 40)

                res = self.input_getter.create_input_box("Ask them for their number?: Yes/ No", ans=['yes', 'no'])
                
                if res == 'yes':
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("Doh, that wasn't a wink, they had dust in their eyes! You quickly take your leave.", 40)                
                    self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                
                    if self.__reception:
                        self.story_manager.update_story(-10)
                        self.story_manager.update_job_security(-10)
                        self.__reception = False
                
                self.workshop_scenario(frame, nextFrame, player_sprite)
            
            elif res == "study area":
                self.player.move([2495,900], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("It's so quiet here, I guess all the students are stuck at home havng to do self directed learning or as we teachers call it, nothing at all.", 40)
                
                res = self.input_getter.create_input_box("Type next to continue", ans=['next'])
                
                if res == 'next':
                    self.text_box_maker.remove_text_box()
                    
                    if self.__study_room:
                        self.text_box_maker.create_text_box("Oh, I just notice the teddy bear. It's kinda cute. Should I take it? I might look a little wierd carrying it out.", 40)
                        self.input_getter.create_input_box("TAKE the teddy bear? Yes, or No", ans=['yes', 'no'])
                        
                        if res == "yes":
                            self.story_manager.update_story(10)
                            self.story_manager.update_job_security(-10)
                            self.__study_room = False
                            self.player.toys_collected += 1
                
                self.workshop_scenario(frame, nextFrame, player_sprite)

            elif res == "computer lab":
                self.player.move([2510,210], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("Hey these laptops look pretty nice. I wonder if I have time to have a quick game?", 40)
                
                res = self.input_getter.create_input_box("Play a quick game?: Yes/ No", ans=['yes', 'no'])
                
                if res == 'yes':
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("What a crappy game. It doesn't even work. Looks like it was designed by a first year as the code has more bugs than a bee hive. I'd better leave before the code crashes me.", 40)
                    self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if self.__computer_lab:
                        self.story_manager.update_story(20)
                        self.__computer_lab = False
                
                self.workshop_scenario(frame, nextFrame, player_sprite)

            elif res == "lockers":
                self.player.move([1845,160], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("These lockers don't look very secure. They're probably from the 70s. And what are they doing here in the middle of the workshop? Did a 5 year old make this room because it looks like it was made in paint. Whatever, I'll just give the door a little nudge.", 40)
                
                res = self.input_getter.create_input_box("The door opened. Take what's inside?  yes/ no", ans=['yes', 'no'])
                
                if res == 'yes':
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("Ahhh.. crap, I think someone's coming!", 40)
                    res = self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if res == 'next':
                        self.text_box_maker.remove_text_box()
                        self.text_box_maker.create_text_box("False alarm. But I all I got is this moldy old sandwich. Gross!", 40)
                        self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                        
                        if self.__lockers:
                            self.story_manager.update_story(-10)
                            self.story_manager.update_job_security(-10)
                            self.__lockers = False
                
                self.workshop_scenario(frame, nextFrame, player_sprite)

            elif res == "exit":
                self.player.move([1245, 480], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("There wasn't much to do in the workshop but are you sure you are ready to leave?", 40)
                
                res = self.input_getter.create_input_box("Do you want to exit?: Yes/ No", ans=['yes', 'no'])
                
                if res == 'yes':
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("Ok. Time for next part of your journey...", 40)
                    
                    res = self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if res == "next" : self.text_box_maker.remove_text_box()
                
                if res == 'no': self.workshop_scenario(frame, nextFrame, player_sprite)

# Generates grading scenarios
class GradingScenarios(metaclass=Singleton):
    def __init__(self):
        #self.scenario_database = ScenarioDatabase()
        self.profile_maker = ProfileMaker()
        self.grade_calculator = GradeCalculator()
        self.story_manager = StoryManager()
        self.student_generator = StudentGenerator()
        self.text_box_maker = TextBoxMaker()
        self.input_getter = InputGetter()
        self.scenario_database = ScenarioDatabase()
        self.event_transitions_db = self.scenario_database.event_transitions_data        

    def generate_marking_session(self, outcomes, profile=None, number_of_tests = 5, istutorial = False):
        tests_remaining = number_of_tests

        if profile == None: profile = self.student_generator.generate_profile()

        if not istutorial:
            if self.story_manager.current_story_level() == 3:
                self.text_box_maker.create_text_box(self.event_transitions_db["scenario_text"][2])
                
                res = self.input_getter.create_input_box("Type NEXT to continue.", ans=['next'])
                
                if res == 'next': self.text_box_maker.remove_text_box()
            
            else:
                self.text_box_maker.create_text_box(["Time for your daily grading session.", 
                            "Read the student's covering letter as the code...", "           ...is just jiberish to you!", 
                            "Then decide on an appropriate grade.", "Correctly marking bios means more story points!", 
                            "WTF are story points? Do you know what gold is? It's not that.", "Get marking!"], 40)
                self.input_getter.create_input_box("Type 'NEXT' to continue.", ans=['next'])

        # who wants to be millionaire sound clip
        playSound(grading_session_sound)

        # create profile
        self.text_box_maker.remove_text_box()
        
        # page change sound fx
        playSound(bio_change_sound)
        
        self.profile_maker.create_bio(profile)

        while tests_remaining > 0:
            res = self.input_getter.create_input_box("Answer with pass/fail", 
                                ans=['pass', 'fail'])              
            
            # play stamp sound of choice
            playSound(pass_fail_stamp)

            if res == "pass":
                self.story_manager.update_story(True, self.grade_calculator.add_bio(profile),
                                outcomes)
                tests_remaining -= 1
                self.profile_maker.remove_bio()
                
                if tests_remaining > 0:
                    playSound(bio_change_sound)
                    profile = self.student_generator.generate_profile()
                    self.profile_maker.create_bio(profile)
            
            elif res == "fail":
                #Easter egg 2: If fail one of the devs -> job security -50
                if profile["name"] in developers_names: self.story_manager.update_job_security(-50)

                self.story_manager.update_story(False, self.grade_calculator.add_bio(profile),
                                outcomes)
                tests_remaining -= 1
                self.profile_maker.remove_bio()
                
                if tests_remaining > 0:
                    playSound(bio_change_sound)
                    profile = self.student_generator.generate_profile()
                    self.profile_maker.create_bio(profile)             

# Generate meet the boss scenarios
class MeetTheBossScenarios(metaclass=Singleton):
    def __init__(self):
        self.scenario_database = ScenarioDatabase()
        self.__meet_the_boss_db = self.scenario_database.meet_the_boss_data
        self.event_transitions_db = self.scenario_database.event_transitions_data   
        self.story_manager = StoryManager()
        self.text_box_maker = TextBoxMaker()
        self.input_getter = InputGetter()
        self.player = Player()  

    __reception = True
    __laptop = True
    __piano = True

    __meet_the_boss_db =  None  #scenario_database.meet_the_boss_data
    __played_safe_game = False

    def intro_text(self):
        global player_name
        
        if self.story_manager.current_story_level() == 4:
            self.text_box_maker.create_text_box(insert_name.insert_name(self.event_transitions_db["scenario_text"][1],player_name))
            
            res = self.input_getter.create_input_box("Type NEXT to continue.", ans=['next'])
            
            if res == 'next': self.text_box_maker.remove_text_box()
        
        else: pass

    def safe_cracking_scenario(self, frame, nextFrame, player_sprite):
        self.text_box_maker.remove_text_box()
        
        if self.player.current_room == "bosses_office":
            
            self.text_box_maker.create_choice_box(["You can move to:", "RECEPTION", "SAFE",
                                                "LAPTOP", "PIANO", "EXIT"], linespacing=21, fontsize=26)

            res = self.input_getter.create_input_box("Enter a command: ", ans=['reception', 'safe', 'laptop',
                                    'piano', 'exit'])

            # Hardcoded locations - when using dictionary bugs with skipping locations after one full cycle
            # ??? to do with frame changing causing dictionary misreads???
            if res == "reception":
                self.player.move([5660, 515], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("You make your way to reception and ask where the boss is today. Apparently he's out playing golf. She then gives you a dirty look as if asking: 'Why are YOU here?'", 40)

                res = self.input_getter.create_input_box("Send her a dirty look back?: Yes/ No", ans=['yes', 'no'])
                
                if res == 'yes':
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("She gives you a stern expression. She's definitely not one to mess with.", 40)                
                    self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if self.__reception:
                        self.story_manager.update_story(-10)
                        self.story_manager.update_job_security(-10)
                        self.__reception = False
                
                self.safe_cracking_scenario(frame, nextFrame, player_sprite)
            
            elif res == "safe":
                self.player.move([6000,845], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                
                if not self.__played_safe_game:
                    self.text_box_maker.create_text_box("Ooh, the boss's safe and he's not here. There must be good things inside but I have to be quick and quiet or miss bossy pants outside will roast me.", 40)
                    
                    res = self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if res == 'next':
                        self.safe_cracking()
                else:
                    self.text_box_maker.create_text_box("You've already done everything here that's possible. Better leave or you might be caught.", 40)
                    res = self.input_getter.create_input_box("Type next to continue", ans=['next'])
                        
                self.safe_cracking_scenario(frame, nextFrame, player_sprite)

            elif res == "laptop":
                self.player.move([5465,730], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("Hey this laptop looks pretty nice. I wonder if I have time to have a quick game?", 40)
                
                res = self.input_getter.create_input_box("Play a quick game?: Yes/ No", ans=['yes', 'no'])
                
                if res == 'yes':
                    self.text_box_maker.remove_text_box()

                    self.text_box_maker.create_text_box("Wow this game is a amazing. It's called clean and code and was definitely made by pros!", 40)
                    self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if res == 'next':
                        
                        if self.__laptop:
                            self.story_manager.update_story(50)
                            self.__laptop = False
                
                self.safe_cracking_scenario(frame, nextFrame, player_sprite)

            elif res == "piano":
                self.player.move([6255,135], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("This piano looks nice. As expected of the boss. I wonder if I should have a quick play?", 40)
                
                res = self.input_getter.create_input_box("Play the piano?  yes/ no", ans=['yes', 'no'])
                
                if res == 'yes':
                    playSound(piano_sound)
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("Hehe I'm pretty good but the receptionist is still wondering who the hell I am?", 40)
                    
                    res = self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if res == 'next':
                        if self.__piano:
                            #play superbass
                            playSoundAndWait(superbass_sound, 1000)
                            self.story_manager.update_story(30)
                            self.story_manager.update_job_security(-10)
                            self.__piano = False
                
                self.safe_cracking_scenario(frame, nextFrame, player_sprite)

            elif res == "exit":
                self.player.move([5120, 480], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("Well that was a productive little session. I have a bad feeling that I'll be back here in the future...", 40)
                
                res = self.input_getter.create_input_box("Do you want to exit?: Yes/ No", ans=['yes', 'no'])
                
                if res == 'yes':
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("Ok. Time for next part of your journey...", 40)
                    
                    res = self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if res == "next" : self.text_box_maker.remove_text_box()
                
                if res == 'no':
                    self.safe_cracking_scenario(frame, nextFrame, player_sprite)
        
    def text_only_scenario(self, number_in_db):
        global player_name

        # separate function to play text grabbed from spreadsheet
        self.intro_text()

        self.text_box_maker.create_text_box(insert_name.insert_name(self.__meet_the_boss_db["scenario_text"][number_in_db], player_name), 33)
        
        response = self.input_getter.create_input_box("Type 'NEXT' to continue.", ans=['next'])

        if response == 'next': self.text_box_maker.remove_text_box()

        self.text_box_maker.create_text_box([ f"Choice 1: {self.__meet_the_boss_db['choice_1'][number_in_db]}", 
                                                f"Choice 2: {self.__meet_the_boss_db['choice_2'][number_in_db]}", 
                                                f"Choice 3: {self.__meet_the_boss_db['choice_3'][number_in_db]}"], 50)
        
        res = self.input_getter.create_input_box("Choose: CHOICE 1, CHOICE 2, CHOICE 3", 
                        ans=['choice 1', 'choice one', '1', 'one', 'choice 2', 'choice two', '2', 'two',
                        'choice 3', 'choice three', '3', 'three'])

        if (res == "choice 1" or res == "choice one" or res == "one" or res == "1"):
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box(insert_name.insert_name(self.__meet_the_boss_db['outcome_choice_1'][number_in_db], player_name))
            self.story_manager.update_story(self.__meet_the_boss_db['points_choice_1'][number_in_db])
            self.story_manager.update_job_security(self.__meet_the_boss_db['js_points_choice_1'][number_in_db])            
        
        elif (res == "choice 2" or res == "choice two" or res == "two" or res == "2"):
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box(insert_name.insert_name(self.__meet_the_boss_db['outcome_choice_2'][number_in_db], player_name))
            self.story_manager.update_story(self.__meet_the_boss_db['points_choice_2'][number_in_db])
            self.story_manager.update_job_security(self.__meet_the_boss_db['js_points_choice_2'][number_in_db]) 
        
        elif (res == "choice 3" or res == "choice three" or res == "three" or res == "3"):
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box(insert_name.insert_name(self.__meet_the_boss_db['outcome_choice_3'][number_in_db], player_name))
            self.story_manager.update_story(self.__meet_the_boss_db['points_choice_3'][number_in_db])
            self.story_manager.update_job_security(self.__meet_the_boss_db['js_points_choice_3'][number_in_db])

        self.input_getter.create_input_box("Type 'NEXT' to continue.", ans=['next'])
        self.text_box_maker.remove_text_box()
    
    def safe_cracking(self):
        self.text_box_maker.remove_text_box()
        self.text_box_maker.create_text_box("The safe has a combination lock. With a bit of tweaking I recogn you could crack it. The solution is a number between 1 and 1000. Can you guess it? Maybe trying one those search algorithms from one of the COMSC classes might help... it was called binary something.")
        
        res = self.input_getter.create_input_box("Try to crack the safe? Yes or No", ans=['yes', 'no'])

        if res == 'yes':
            self.__played_safe_game = True
            self.text_box_maker.remove_text_box()
            
            thoughtnum = random.randrange(1,1000)

            if thoughtnum < 500:
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_choice_box("You fiddle with the knob and realise the first number is less than 500")

            if thoughtnum > 500:
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_choice_box("You fiddle with the knob and realise the first number is more than 500")

            #Sets the number to think of
            correct = False
            attempts = 10
            last_guess = None

            while attempts >= 1 and correct == False:
 
                guessnum = self.input_getter.create_number_only_input_box("Try entering a number between 1 and 1000.")
                
                # will only playb after correct guess
                playSound(dial_clicker_sound)

                self.text_box_maker.remove_choice_box()
                #asks the user for input
                
                try:
                #if guessnum was a number, plays the game
                    checknum = int(guessnum)
                    if checknum < thoughtnum:

                        attempts = (attempts) -1
                        last_guess = checknum

                        self.text_box_maker.create_choice_box(["After a bit of tweaking", "you realise you need", "to go:", "HIGHER", "You have:", f"{str(attempts)} attempts remaining.", f"Last Guess: {last_guess}"])
                    
                    if checknum > thoughtnum:
                        attempts = (attempts) -1
                        last_guess = checknum

                        self.text_box_maker.create_choice_box(["After a bit of tweaking", "you realise you need", "to go", "LOWER", "You have:", f"{str(attempts)} attempts remaining.", f"Last Guess: {last_guess}"])
                    
                    if checknum == thoughtnum:
                        playSound(safe_cracked_sound)
                        self.text_box_maker.create_choice_box(["Clink...", "You hear the sweet", "sound of a lock", "being picked."])
                        correct = True
                    
                    if attempts == 0:
                        playSound(game_over_sound)
                        
                        self.text_box_maker.create_choice_box(["Your time has run up.", "Looks like you can't", "give up your day job", "to become a master burglar."])
                        self.story_manager.update_job_security(-10)
                        self.story_manager.update_story(-10)
                        self.text_box_maker.remove_choice_box()
                        self.text_box_maker.remove_text_box()
                        
                        return
                    
                    # incorrect guess
                    playSound(incorrect_safe_guess_sound)

                except:
                #if guessnum was not a number
                    self.text_box_maker.create_choice_box("At least try real numbers.", "Nows not the time to catch stupid!")

            res = self.input_getter.create_input_box("Type NEXT to continue", ans=["next"])
            
            if res == "next":
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box(["You find what your boss holds most dear in his safe.", "It's a picture of his wife. Oh how sweet.", "But... sweet doesn't pay the bills.", "Dammit, foiled again by life!", "Take the picture out of spite?"])

            res = self.input_getter.create_input_box("Do you want to take the picture? Yes/No", ['yes', 'no'])

            if res == 'yes': 
                self.story_manager.update_job_security(-20)
                self.story_manager.update_story(-20)
                self.text_box_maker.remove_text_box()
            
            elif res == 'no':
                self.story_manager.update_job_security(20)
                self.story_manager.update_story(30)
                self.text_box_maker.remove_text_box()

        else:
            self.text_box_maker.remove_text_box()
            self.text_box_maker.create_text_box("Wuss.")
            
            res = self.input_getter.create_input_box("Type NO if you've decided to man (or woman) up. Otherwise type NEXT ", ans=['next', 'no'])

            if res == "next": 
                self.text_box_maker.remove_text_box()
                
            elif res == "no":
                self.text_box_maker.remove_text_box()
                self.safe_cracking()

# Generates free period scenarios
class FreePeriodScenarios(metaclass=Singleton):
    def __init__(self):
        self.story_manager = StoryManager()
        self.text_box_maker = TextBoxMaker()
        self.input_getter = InputGetter()  
        self.player = Player()

    __papers = True
    __water_dispenser = True
    __photocopier = True
    __vending_machine = True
    __waiting_room = True

    def office_scenario(self, frame, nextFrame, player_sprite):
        self.text_box_maker.remove_text_box()
        
        if self.player.current_room == "office":
            
            self.text_box_maker.create_choice_box(["You can move to:", "PAPERS", "WATER DISPENSER",
                                                "TELEPHONE", "WAITING ROOM", "PHOTOCOPIER", "VENDING MACHINE", "EXIT"], linespacing=21, fontsize=26)

            res = self.input_getter.create_input_box("Enter a command: ", ans=['papers', 'telephone', 'waiting room',
                                    'photocopier', 'vending machine', 'water dispenser', 'exit'])

            # Hardcoded locations - when using dictionary bugs with skipping locations after one full cycle
            # ??? to do with frame changing causing dictionary misreads???
            if res == "papers":
                self.player.move([340, 805], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("Still so much work to do. Hmmm, maybe I should burn some of these papers to lighten my load... LIGHTen, get it. Hehe.", 40)

                res = self.input_getter.create_input_box("Burn some papers?: Yes/ No", ans=['yes', 'no'])
                if res == 'yes':
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("Ahhh..... crap, the room smells of smoke now. Hope people don't think I'm a smoker.", 40)                
                    self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if self.__papers:
                        self.story_manager.update_story(30)
                        self.story_manager.update_job_security(-20)
                        self.__papers = False
                
                self.office_scenario(frame, nextFrame, player_sprite)
            
            elif res == "telephone":
                self.player.move([60,410], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("What's this telephone doing here. Seems kinda random. Besides, I thought everybody used mobile phones. It must belong to one of those dinosaurs... I mean professors.", 40)
                
                res = self.input_getter.create_input_box("Type next to continue", ans=['next'])
                
                if res == 'next':
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("I better stop procrastinating and do some work.", 40)
                    self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                
                self.office_scenario(frame, nextFrame, player_sprite)

            elif res == "waiting room":
                self.player.move([1100,790], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("Those magazines look really old. Haven't people heard of kindle's and the internet? Well, I guess they got to spend the 9k tuition fees on something. Huh, what's this... you think you spot an issue of playboy... ", 40)
                
                res = self.input_getter.create_input_box("Do you read it?: Yes/ No", ans=['yes', 'no'])
                
                if res == 'yes':
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("What, no nude pics. Oh, this isn't playboy... ahem, I mean this isn't Nature. Cough, cough.", 40)
                    self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if self.__waiting_room:
                        self.story_manager.update_story(20)
                        self.__waiting_room = False
                
                self.office_scenario(frame, nextFrame, player_sprite)

            elif res == "photocopier":
                self.player.move([920,520], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("This photocopier looks ancient. I wonder if it still works... it does! Hmmm, I wonder what I could do...? Maybe I could...", 40)
                
                res = self.input_getter.create_input_box("Photocopy your butt? yes/ no", ans=['yes', 'no'])
                
                if res == 'yes':
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("Ahhh.. crap, I think someone's coming!", 40)
                    
                    res = self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if res == 'next':
                        self.text_box_maker.remove_text_box()
                        self.text_box_maker.create_text_box("False alarm. But I got a friction burn. Dammit!", 40)
                        self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                        
                        if self.__photocopier:
                            self.story_manager.update_story(-10)
                            self.story_manager.update_job_security(-10)
                            self.__photocopier = False
                
                self.office_scenario(frame, nextFrame, player_sprite)

            elif res == "vending machine":
                self.player.move([720,530], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("Huh, a vending machine. Wispa, dairy milk, crunchie, skittle. All the essentials a growing teacher needs. Ahh but it's kinda pricey and the bars are so small. I remember when jumbo size was just regular size. Ahh.. those were the days.", 40)
                
                res = self.input_getter.create_input_box("Try and jiffy the machine for free chocolate?: Yes/ No", ans=['yes', 'no'])
                
                if res == 'yes':
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("Ahhh..... damn, my fingers got jammed", 40)
                    self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if self.__vending_machine:
                        self.story_manager.update_story(-10)
                        self.story_manager.update_job_security(-10)
                        self.__vending_machine = False
                
                self.office_scenario(frame, nextFrame, player_sprite)

            elif res == "water dispenser":
                self.player.move([40,485], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("It's very warm today and you've been working hard. You should stay hydrated. Do you want to drink a glass of cool water?", 40)
                
                res = self.input_getter.create_input_box("Drink the water?: Yes/ No", ans=['yes', 'no'])
                
                if res == 'yes':
                    playSound(gulp_sound)
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("Ahhh..... that was refreshing. Remember boys (and girls), stay hydrated. This segment was sponsored by [insert water company].", 40)
                    self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if self.__water_dispenser:
                        self.story_manager.update_story(10)
                        self.__water_dispenser = False
                
                self.office_scenario(frame, nextFrame, player_sprite)

            elif res == "exit":
                self.player.move([1290, 480], frame, nextFrame, player_sprite)
                self.text_box_maker.remove_choice_box()
                self.text_box_maker.create_text_box("So you've finished working hard in your office, after all doing nothing is hard work. But are you sure you are ready to leave?", 40)
                
                res = self.input_getter.create_input_box("Do you want to exit?: Yes/ No", ans=['yes', 'no'])
                
                if res == 'yes':
                    self.text_box_maker.remove_text_box()
                    self.text_box_maker.create_text_box("Ok. Time for next part of your journey...", 40)
                    
                    res = self.input_getter.create_input_box("Type NEXT to continue", ans=['next'])
                    
                    if res == "next" : self.text_box_maker.remove_text_box()
                
                if res == 'no': self.office_scenario(frame, nextFrame, player_sprite)

# Generates ending based on story points
class Endings:
    def __init__(self):
        self.scenario_database = ScenarioDatabase()
        self.__endings_db = self.scenario_database.endings_data
        self.player = Player()
        self.story_manager = StoryManager()
        self.text_box_maker = TextBoxMaker()
        self.input_getter = InputGetter()

    __endings_db = None

    def __chosen_ending_index(self):
        final_score = self.story_manager.current_score()

        if final_score >= 200: return 0
        elif final_score >= 150: return 1
        elif final_score >= 100: return 2
        elif final_score >= 50: return 3
        else: return 4

    def chosen_ending(self):
        
        # check if all 3 toys in inventory - not all toys in game :(
        if self.player.toys_collected >= 3: story_manager.update_story(100)
        elif self.player.toys_collected >= 2: story_manager.update_story(30)
        elif self.player.toys_collected >= 1: story_manager.update_story(10)

        # find chosen ending
        ending_index = self.__chosen_ending_index()

        self.text_box_maker.remove_text_box()
        
        # sort out audio: stop music -> drum roll -> restart music
        pauseMusic()
        playSoundAndWait(ending_drum_roll_sound, 100)
        makeMusic(ending_music)
        playMusic()
        
        global player_name
        
        self.text_box_maker.create_ending_text_box(insert_name.insert_name(self.__endings_db["ending_text"][ending_index], player_name))
        
        res = self.input_getter.create_input_box("Type: EXIT to close the game", ans=['exit'])
        
        # exit game
        if res == 'exit':
            pygame.quit()
            exit()

