import os, random, insert_name, scenario_manager
from helper_functions import ImageResizer, TextWrapper
from pygame_functions import makeSprite, moveSprite, showSprite, hideSprite,  makeLabel, showLabel, hideLabel
from singleton import Singleton
from pathlib import Path
from spreadsheet import ScenarioDatabase

resource_path = Path(__file__).parents[1]                           # The resource folder path
image_path = os.path.join(resource_path, 'images')                  # The image folder path

# Easter egg - 100% pass rate
developers_names = ["NAFIS AHMED", "OPHELIA CHAN", "SELIM CELIK", "CALLUM GREER", 
                    "BENJAMIN MEADOWS", "ELLIOT KEMPSON", "HARRISON CASEY"]

# Create one instance in GameManager and then feed it bios, it will output pass/fail
class GradeCalculator(metaclass=Singleton):    
    def __init__(self):
        scenario_database = ScenarioDatabase()
        self.__student_bios_db = scenario_database.student_bios_data

    # holds bio data
    bio = None

    # main function, takes a bio and then outputs pass/fail
    def add_bio(self, biography):
        self.bio = biography

        # easter egg 1 -> devs 100% pass!!!
        if self.bio["name"] in developers_names: return True
        else: return self.__passed_test()

    # This fuction takes a dictionary student_bio and returns the result as a dictionary
    def __trait_score_calculator(self):
        
        # nested dictionary to store scoring values for certain traits. Scored out of 10 for clarity (rather than decimals) - in pass probability all numbers will be divided by 10
        trait_values = {
            "hair colour": {"black" : 10, "brown" : 5, "ginger" : 1, "silver" : 9, "yellow" : 2, "bald" : 2},
            "glasses" : {'yes' : 10, 'no' : 6},
            "style" : {'goth' : 3, 'emo' : 3, 'rugby' : 2, 'nerd' : 10},
            "personality": {"angry" : 2, "lazy" : 1, "astute" : 8, "clever" : 10, "clown" : 1},
            "location" : {"wales" : 10, "scotland" : 2, "northern ireland" : 9, "england" : 1}
        }

        # use .get for error catching - if can't find value (because of typo), that attribute is defaulted to 0
        # place holders - 0.6 weighting to hair color, 0.4 weighting to glasses. 0.6 personality, 0.4 to style
        physical_traits = trait_values.get("hair colour",0).get(self.bio["hair colour"],0) * 0.6 + trait_values.get("glasses",0).get(self.bio["glasses"],0) * 0.4
        personality = trait_values.get("personality",0).get(self.bio["personality"],0) * 0.8 + trait_values.get("style", 0).get(self.bio["style"], 0) * 0.2
        location = trait_values.get("location",0).get(self.bio["location"], 0)

        bio_text = self.bio["bio"]
        bio_text = bio_text.replace(self.bio["name"], "[name]")

        try: bio_index = self.__student_bios_db["bio_text"].loc[lambda x: x==bio_text].index[0]
        except: bio_index = None

        try: bio_fail = self.__student_bios_db["fail_possibility"][bio_index].index[0]
        except: 
            try: bio_fail = self.__student_bios_db["fail_possibility"][bio_index]
            except: bio_fail = 10

        return {"physical" : physical_traits, "personality" : personality, "location" : location, "fail_poss" : bio_fail}

    # takes the dictionary produced by trait_score_calculator and calculates a pass probability
    def __pass_probability(self):
        student_values = self.__trait_score_calculator()
        pass_probability = lambda physical, personality, location, fail_poss : ((0.2 * physical + 0.2 * location + 0.6 * personality) / 30) + ((10-fail_poss)/15)
        #print(f"Pass probability = {pass_probability(student_values['physical'], student_values['personality'], student_values['location'], student_values['fail_poss'])}")
        return pass_probability(student_values['physical'], student_values['personality'], student_values['location'], student_values['fail_poss'])

    # passed_test returns true if pass_probability >= random number generated
    def __passed_test(self):
        return True if self.__pass_probability() >= random.random() else False

test = GradeCalculator()


# Creates the grading profiles
class ProfileMaker(metaclass=Singleton):
    def __init__(self):
        self.text_wrapper = TextWrapper()
        self.image_resizer = ImageResizer()

    __can_add_bio = True
    __current_profile = None

    __book_parts = {                            # dictionary which holds the book sprites
        'book' : None,
        'text' : None
    }

    __body_parts = {                            # dictionary which hobody sprites
        'body' : None,
        'hair' : None,
        'top'  : None,
        'bottom' : None,
        'shoes' : None,
        'accessories' : None,
        'glasses' : None    
    }

    __text_parts = {                            # dictionary which holds the text sprites
        "name" : None,
        "gender":None,
        "location" : None,
        "personality" : None,
        "style" : None,
        "phone" : None,
        "dob":None,
        "bio" : None,
        "comments" : None,
        "glasses" : None,
        "hair colour" : None
    }

    __text_locations = {                        # dictionary which holds location for text to be blitzed as a list
        "name" : [340,206],
        "gender": [360,398],
        "location" : [375,238],
        "personality" : [411,272],
        "style" : [341,304],
        "phone" : [350,337],
        "dob":[326,370],
        "bio" : [692,210],
        "comments" : [80,532],
        "glasses" : [366,456],
        "hair colour" : [390,428]      
    }

    # make bio pic and text
    def create_bio(self, profile, x=100, y=300):
        
        # add bio if one not on screen
        if self.__can_add_bio:
            self.__can_add_bio = False
            self.__current_profile = profile

            #make book borders
            self.__make_book_pic()

            # makes pixel bio pic
            self.__make_bio_pic(profile)

            for item in profile:
                if self.__text_locations[item] != None:
                    # bio and comments need to be text wrapped before blitz so handled sperately
                    if item == 'bio':
                        self.text_wrapper.add_multi_line_text(profile['bio'], fontsize=20, x=self.__text_locations[item][0],
                                        y=self.__text_locations[item][1], width = 44, fontColour=(61, 55, 55), font='04B_03__')
                    elif item == 'comments':
                        try: self.text_wrapper.add_multi_line_text_2(insert_name.insert_name(profile['comments'], scenario_manager.get_name()), fontsize=20, x=self.__text_locations[item][0],   #### Add name from scenario manager
                                        y=self.__text_locations[item][1], width = 44, fontColour=(61, 55, 55), font='04B_03__')                        
                        except: pass
                    else:
                        self.__text_parts[item] = makeLabel(profile[item], 20, self.__text_locations[item][0], self.__text_locations[item][1], font='04B_03__')
                        showLabel(self.__text_parts[item])

    # Generate the pixel art book and text box
    def __make_book_pic(self, x=40, y=130):
        book_part_img_location = {
            'book' : os.path.join(image_path, 'frames/'+str(random.randint(0, 5))+'.png'),
            'text' : os.path.join(image_path, 'text/bio.png'),
        }

        for part in self.__book_parts:
            self.__book_parts[part] = makeSprite(book_part_img_location[part])
            
            moveSprite(self.__book_parts[part], x, y)
            showSprite(self.__book_parts[part])
            
            # initialize book with 0 size -> 100 to give appearance of enlarging out
            if part == 'book' : 
                self.image_resizer.shrink(self.__book_parts['book'])
                self.image_resizer.enlarge(self.__book_parts['book'], 90, speed=25)

    # Generate the pixel art picture        
    def __make_bio_pic(self, profile, x=75, y=145):
        
        # finds image location
        body_part_img_location = {
            'body' : os.path.join(image_path, 'character/'+ profile['gender'] +'/body.png'),
            'hair' : os.path.join(image_path, 'character/'+ profile['gender'] +'/hair/'+ profile['style'] + '_' + profile['hair colour']+ '_' + str(random.randint(0, 1))+ '.png'),
            'top' : os.path.join(image_path, 'character/'+ profile['gender'] +'/top/'+ profile['style'] + '_' + str(random.randint(0, 1))+ '.png'),
            'bottom' : os.path.join(image_path, 'character/unisex/bottom/'+ profile['style'] + '_' + str(random.randint(0, 1))+ '.png'),
            'shoes' : os.path.join(image_path, 'character/'+ profile['gender'] +'/shoes/'+ str(random.randint(0, 3))+ '.png'),
            'accessories' : os.path.join(image_path, 'character/'+ profile['gender'] +'/accessories/'+ str(random.randint(0, 2))+ '.png'),
            'glasses' : os.path.join(image_path, 'character/'+ profile['gender'] +'/glasses/'+ profile['glasses']+ '.png')        
        }

        # for loop then displays it
        for part in self.__body_parts:
            self.__body_parts[part] = makeSprite(body_part_img_location[part])

            moveSprite(self.__body_parts[part], x, y)
            showSprite(self.__body_parts[part])

    # changes bio pic
    def change_bio_pic(self):
        for part in self.__body_parts:            
            hideSprite(self.__body_parts[part])
        
        # update only the pixel image
        self.__make_bio_pic(self.__current_profile)
    
    # removes all info
    def remove_bio(self):
        
        # remove pixel pic
        for part in self.__body_parts:
            if self.__body_parts[part] != None: hideSprite(self.__body_parts[part])
        
        # removes text from profile
        for item in self.__text_parts:
            if self.__text_parts[item] != None and (item != 'bio' or item != 'comments') : hideLabel(self.__text_parts[item])
            self.text_wrapper.remove_multi_line_text()
            self.text_wrapper.remove_multi_line_text_2()

        # hides book sprite
        hideSprite(self.__book_parts['text'])
        
        self.__can_add_bio = True
        
        # shrinks and hides book
        self.image_resizer.shrink(self.__book_parts['book'], speed=25)
        
        hideSprite(self.__book_parts['book'])
        self.__current_profile = None
