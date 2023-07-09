import os, textwrap, time, pygame
from pygame_functions import *
from pathlib import Path
from singleton import Singleton
from game_parser import normalise_input

resource_path = Path(__file__).parents[1]               # The resource folder path
image_path = os.path.join(resource_path, 'images')      # The image folder path
sfx_path = os.path.join(resource_path, 'sfx')           # The sfx folder path

# Images
text_box_img = os.path.join(image_path, 'text_box.png')
choice_box_img = os.path.join(image_path, 'choice_box.png')
ending_box_img = os.path.join(image_path, 'ending.jpg')

# SFX
incorrect_input_sound = makeSound(os.path.join(sfx_path, 'incorrect_input.wav'))

# Pixel Numbers - red
red_0 = os.path.join(image_path, 'red_0.png')
red_1 = os.path.join(image_path, 'red_1.png')
red_2 = os.path.join(image_path, 'red_2.png')
red_3 = os.path.join(image_path, 'red_3.png')
red_4 = os.path.join(image_path, 'red_4.png')
red_5 = os.path.join(image_path, 'red_5.png')
red_6 = os.path.join(image_path, 'red_6.png')
red_7 = os.path.join(image_path, 'red_7.png')
red_8 = os.path.join(image_path, 'red_8.png')
red_9 = os.path.join(image_path, 'red_9.png')

# Pixel Numbers - green
green_0 = os.path.join(image_path, 'green_0.png')
green_1 = os.path.join(image_path, 'green_1.png')
green_2 = os.path.join(image_path, 'green_2.png')
green_3 = os.path.join(image_path, 'green_3.png')
green_4 = os.path.join(image_path, 'green_4.png')
green_5 = os.path.join(image_path, 'green_5.png')
green_6 = os.path.join(image_path, 'green_6.png')
green_7 = os.path.join(image_path, 'green_7.png')
green_8 = os.path.join(image_path, 'green_8.png')
green_9 = os.path.join(image_path, 'green_9.png')

# store above pixel numbers as two dictionaries
green_numbers = {
    0 : green_0, 1 : green_1, 2 : green_2, 3 : green_3, 4 : green_4, 5 : green_5, 6 : green_6, 7 : green_7,
    8 : green_8, 9 : green_9
}

red_numbers = {
    0 : red_0, 1 : red_1, 2 : red_2, 3 : red_3, 4 : red_4, 5 : red_5, 6 : red_6, 7 : red_7,
    8 : red_8, 9 : red_9
}

# Shrinks or enlarges an image size - extended code from pygame_functions
class ImageResizer:
    def __init__(self):
        pass

    __scale = 10
    __scaleChange = 10

    def enlarge(self, sprite, maxsize = 350, speed=20):
        if self.__scale <= maxsize:
            while True:
                self.__scale += self.__scaleChange
                transformSprite(sprite, 0, self.__scale/100)
                if self.__scale > maxsize:
                    break
                pause(speed)

    def shrink(self, sprite, minsize = 10, speed=20):
        if self.__scale >= minsize:
            while True:
                self.__scale -= self.__scaleChange
                transformSprite(sprite, 0, self.__scale/100)
                if self.__scale < minsize:
                    break
                pause(speed)

# Takes in text, wraps it ready for use with pygame_functions
class TextWrapper:
    def __init__(self):
        pass

    # private variables - 2 sets to allow for 2 wrapped texts on screen e.g. student bios -> bio + comment sections
    wrap_the_text = None
    __label_holder = []
    wrap_the_text_2 = None
    __label_holder_2 = []
    
    # After adding a multiline, make sure to call remove multiline before adding another
    def add_multi_line_text(self, text, fontsize=40, x=460, y=300, width=40, fontColour="black", font="pxlxxl", background="clear", linespacing = 29):
        if type(text) == list:
            self.wrap_the_text = text
        else:
            self.wrap_the_text = textwrap.wrap(text, width)    

        for i in range(0, len(self.wrap_the_text)):
            xheight = x
            yheight = y+i*linespacing
            self.__label_holder.append(makeLabel(self.wrap_the_text[i], fontsize, xheight, yheight, fontColour, font, background))
            showLabel(self.__label_holder[i])
    
    # removes stored multiline text so new text can be added
    def remove_multi_line_text(self):
        for label in self.__label_holder:  
            hideLabel(label)
        self.wrap_the_text = None
        self.__label_holder = []

    # Second wrapping box to be used when double multiline needed e.g. comments on bios - this code needs to be refactored
    def add_multi_line_text_2(self, text, fontsize=40, x=460, y=300, width=40, fontColour="black", font="pxlxxl", background="clear", linespacing = 29):
        if type(text) == list:
            self.wrap_the_text_2 = text
        else:
            self.wrap_the_text_2 = textwrap.wrap(text, width)    

        for i in range(0, len(self.wrap_the_text_2)):
            xheight = x
            yheight = y+i*linespacing
            self.__label_holder_2.append(makeLabel(self.wrap_the_text_2[i], fontsize, xheight, yheight, fontColour, font, background))
            showLabel(self.__label_holder_2[i])
    
    def remove_multi_line_text_2(self):
        for label in self.__label_holder_2:  
            hideLabel(label)
        self.wrap_the_text_2 = None
        self.__label_holder_2 = []

# Makes a box for player to put input
class InputGetter(metaclass=Singleton):
    def __init__(self):
        pass

    __wordBox = None
    __intBox = None

    # creates an input box
    def create_input_box(self, prompt="Enter text here", ans=['yes', 'no'], set_ans=True):
        self.__wordBox = makeTextBox(30, 880, 1220, 0, prompt, 60, 30, font="visitor1", fontColour=(255, 255, 255), background=(0,0,153))
        
        showTextBox(self.__wordBox)
        
        if set_ans:
            res = normalise_input(textBoxInput(self.__wordBox))
            while res not in ans:
                playSound(incorrect_input_sound)
                res = normalise_input(textBoxInput(self.__wordBox))

        else:
            res = textBoxInput(self.__wordBox)

        hideTextBox(self.__wordBox)

        return res

    # for number inputs e.g. number guessing game - ans = acceptable number input
    # in ans enter list of length 2 with desired number range [inclusive, exclusive]
    # e.g. create_number_only_input_box(self, prompt="Enter a number", ans=[1,100]) -< answer range 1-99 
    def create_number_only_input_box(self, prompt="Enter a number", ans=None):
        
        # store list of int to be converted to list of string
        list_int = None
        list_string = None
        
        # use default 1-1000 if argument set
        if ans == None:
            list_int = list(range(1, 1001))
            list_string = map(str, list_int)
        
        # else try the argument
        else:
            try:
                type(ans) == list

                # raise exception if not a list or len(ans) not 2
                if type(ans) != list or len(ans) != 2: raise ValueError
                
                # if valid input, grab the range
                list_int = list(range(ans[0], ans[1]))
                list_string = map(str, list_int)
            
            # create default 1-1000 list if errors not handled
            except ValueError:
                list_int = list(range(1, 1001))
                list_string = map(str, list_int)
        
        # set accepted ans to the list of numbers taken from above if/else statement
        ans = list(list_string)

        # create, show and save result in res
        self.__intBox = makeTextBox(30, 880, 1220, 0, prompt, 60, 30, font="visitor1", fontColour=(255, 255, 255), background=(0,0,153))
        showTextBox(self.__intBox)
        res = textBoxInput(self.__intBox)

        # loop box creation until valid result entered
        while res not in ans:
            playSound(incorrect_input_sound)
            res = textBoxInput(self.__intBox)
            
        # hide input box
        hideTextBox(self.__intBox)

        # return the res
        return res

# Makes a text box for player to read instructions
class TextBoxMaker(metaclass=Singleton):
    def __init__(self):
        self.__text_box_sprite = makeSprite(text_box_img)
        self.__choice_box_sprite = makeSprite(choice_box_img)
        self.__ending_box_sprite = makeSprite(ending_box_img)
        self.__text_wrapper = TextWrapper()
        self.image_resizer = ImageResizer()
    
    # private variables
    __text_wrapper = None
    __text_box_sprite = None
    __choice_box_sprite = None
    __ending_box_sprite = None
    __can_add_text = True
    __can_add_choice_box_text = True
    __index = 0
    __scrollable_text = False
    __can_scroll = True
    __text_list = []

    # text box for main text pieces
    def create_text_box(self, text, linespacing=29, fontsize=40, fontColour=(255, 255, 255), width=78):
        
        if self.__can_add_text:
            self.__can_add_text = False
            
            moveSprite(self.__text_box_sprite, 640, 630, True)
            showSprite(self.__text_box_sprite)
            
            self.__text_wrapper.add_multi_line_text(text, fontsize=fontsize, x=240, y=480, width=width, 
                    fontColour=fontColour, font="pxlxxl", background="clear", linespacing = linespacing)

    def remove_text_box(self):
        
        if not self.__can_add_text:
            self.__text_wrapper.remove_multi_line_text()
            
            hideSprite(self.__text_box_sprite)
            
            self.__can_add_text = True
            self.__scrollable_text = False
            self.__index = 0

    # For long text pieces - text = list of texts
    def scrollable_text_box(self, text):
        
        if self.__can_add_text:
            self.__scrollable_text = True
            self.__can_add_text = False
            self.__text_list = text
            
            moveSprite(self.__text_box_sprite, 640, 630, True)
            showSprite(self.__text_box_sprite)
            
            self.__text_wrapper.remove_multi_line_text()
            self.__text_wrapper.add_multi_line_text(text[self.__index], fontsize=40, x=240, y=480, width=78, 
                fontColour=(255, 255, 255), font="pxlxxl", background="clear")

    # scroll left and right used to navigate scroll box
    def scroll_right(self):
        
        if self.__scrollable_text:
            self.__index += 1
            
            if self.__index >= len(self.__text_list):
                self.remove_text_box()
            else:
                self.__text_wrapper.remove_multi_line_text()
                self.__text_wrapper.add_multi_line_text(self.__text_list[self.__index], fontsize=40, x=240, y=480, width=78, 
                    fontColour=(255, 255, 255), font="pxlxxl", background="clear")

    def scroll_left(self):
        
        if self.__scrollable_text and self.__index > 0:    
            self.__index -= 1
            self.__text_wrapper.remove_multi_line_text()
            self.__text_wrapper.add_multi_line_text(self.__text_list[self.__index], fontsize=40, x=240, y=480, width=78, 
                fontColour=(255, 255, 255), font="pxlxxl", background="clear")

    def current_index(self):
        return self.__index

    # Small boxes - use for command lists
    def create_choice_box(self, text, linespacing=22, x=125, y=670, fontsize=28, fontColour=(255, 255, 255)):
        
        if self.__can_add_choice_box_text:
            self.__can_add_choice_box_text = False
            
            moveSprite(self.__choice_box_sprite, 200, 750, True)
            showSprite(self.__choice_box_sprite)
            
            self.__text_wrapper.add_multi_line_text(text, fontsize=fontsize, x=x, y=y, width=20, 
                    fontColour=fontColour, font="pxlxxl", background="clear", linespacing = linespacing)

    def remove_choice_box(self):
        
        if not self.__can_add_choice_box_text:
            
            self.__text_wrapper.remove_multi_line_text()
            hideSprite(self.__choice_box_sprite)
            
            self.__can_add_choice_box_text = True


    # ending text box
    def create_ending_text_box(self, text, linespacing=27, fontsize=24, fontColour=(0, 0, 0)):
        
        if self.__can_add_text:
            self.__can_add_text = False
            
            moveSprite(self.__ending_box_sprite, 640, 480, True)
            showSprite(self.__ending_box_sprite)
            
            self.image_resizer.enlarge(self.__ending_box_sprite,90)
            self.__text_wrapper.add_multi_line_text(text, fontsize=fontsize, x=390, y=200, width=40, 
                    fontColour=fontColour, font="visitor1", background="clear", linespacing = linespacing)

    def remove_ending_text_box(self):
        
        if not self.__can_add_text:
            
            self.__text_wrapper.remove_multi_line_text()
            hideSprite(self.__text_box_sprite)
            
            self.__can_add_text = True
            self.__scrollable_text = False
            self.__index = 0

# outputs pop ups e.g. point notifications
class PopUp(metaclass=Singleton):
    
    def __init__(self):
        self.image_resizer = ImageResizer()

    __spacing = 0

    # green pixel number pop up
    def pop_up_green_points(self, number, x=1160, y=120):
        
        number_holder = [int(d) for d in str(abs(number))]
        sprite_holder = []

        can_add_num = True

        if can_add_num:
            can_add_num = False
            
            for num in number_holder:
                sprite = makeSprite(green_numbers[num])
                sprite_holder.append(sprite)
                moveSprite(sprite, x + self.__spacing, y, True)
                transformSprite(sprite, 0, 0.5)
                showSprite(sprite)
                self.__spacing += 36
            
            can_add_num = True
            self.__spacing = 0
        
        for sprite in sprite_holder:
            self.image_resizer.enlarge(sprite, 60)
            self.image_resizer.shrink(sprite, 50)
        
        time.sleep(1)
        for sprite in sprite_holder:
            hideSprite(sprite)

    # red pixel number pop ups
    def pop_up_red_points(self, number, x=1160, y=120):
        
        number_holder = [int(d) for d in str(abs(number))]
        sprite_holder = []

        can_add_num = True

        if can_add_num:
            can_add_num = False
            
            for num in number_holder:
                sprite = makeSprite(red_numbers[num])
                sprite_holder.append(sprite)
                moveSprite(sprite, x + self.__spacing, y, True)
                transformSprite(sprite, 0, 0.5)
                showSprite(sprite)
                self.__spacing += 36
            
            can_add_num = True
            self.__spacing = 0
        
        for sprite in sprite_holder:
            self.image_resizer.enlarge(sprite, 60)
            self.image_resizer.shrink(sprite, 50)
        
        time.sleep(1)
        for sprite in sprite_holder:
            hideSprite(sprite)

# updates story points text on UI
class StoryPointsUI(metaclass=Singleton):
    def __init__(self):
        self.image_resizer = ImageResizer()

    __spacing = 0
    __sprite_holder = []

    def story_score(self, score, x=1220, y=50):
        
        self.remove_old_score()
        
        if score < 0:
            sprite = makeSprite(green_numbers[0])
            self.__sprite_holder.append(sprite)
            
            moveSprite(sprite, x + self.__spacing, y, True)
            transformSprite(sprite, 0, 0.7)
            showSprite(sprite)
            
            return

        number_holder = [int(d) for d in str(score)]

        can_add_num = True

        if can_add_num:
            can_add_num = False
            for i in range(len(number_holder)-1,-1,-1):
                sprite = makeSprite(green_numbers[number_holder[i]])
                self.__sprite_holder.append(sprite)
                
                moveSprite(sprite, x + self.__spacing, y, True)
                transformSprite(sprite, 0, 0.7)
                showSprite(sprite)
                
                self.__spacing -= 60
            
            can_add_num = True
            self.__spacing = 0

    def remove_old_score(self):
        for sprite in self.__sprite_holder: hideSprite(sprite)

# updates job points text on UI
class JobPointsUI(metaclass=Singleton):
    def __init__(self):
        self.image_resizer = ImageResizer()

    __spacing = 0
    __sprite_holder = []

    def job_score(self, score, x=50, y=50):
        
        self.remove_old_score()
        
        if score < 0:
            sprite = makeSprite(red_numbers[0])
            self.__sprite_holder.append(sprite)
            
            moveSprite(sprite, x + self.__spacing, y, True)
            transformSprite(sprite, 0, 0.7)
            showSprite(sprite)
            
            return

        number_holder = [int(d) for d in str(score)]

        can_add_num = True

        if can_add_num:
            can_add_num = False
            
            for i in range(len(number_holder)):
                sprite = makeSprite(red_numbers[number_holder[i]])
                self.__sprite_holder.append(sprite)
                
                moveSprite(sprite, x + self.__spacing, y, True)
                transformSprite(sprite, 0, 0.7)
                showSprite(sprite)
                
                self.__spacing += 60
            
            can_add_num = True
            self.__spacing = 0

    def remove_old_score(self):
        for sprite in self.__sprite_holder: hideSprite(sprite)
