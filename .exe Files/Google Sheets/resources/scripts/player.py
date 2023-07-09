import os
from singleton import Singleton
from pygame_functions import *
from pathlib import Path
from helper_functions import TextBoxMaker, InputGetter, ImageResizer
from story_manager import StoryManager

resource_path = Path(__file__).parents[1]                       # The resource folder path
image_path = os.path.join(resource_path, 'images')              # The image folder path
player_img = os.path.join(image_path, 'player_sprite.png')

# collectible items for inventory - unable to fully implement
toy_1_img = os.path.join(image_path, 'toy_1.png')
toy_2_img = os.path.join(image_path, 'toy_2.png')
toy_3_img = os.path.join(image_path, 'toy_3.png')

#Store player data including inventory and related info
class Player(metaclass=Singleton):
    def __init__(self):
        self.text_box_maker = TextBoxMaker()
        self.input_getter = InputGetter()
        self.image_resize = ImageResizer()
        self.story_manager = StoryManager()

    # some unused variables here as ran out of time whilst implementing other features
    player_inventory = []
    toys_collected = 0
    collectable_items = ['']
    current_room = "office"
    current_location = [640, 480]                             # top left = [1280, 960], bottom right = [0, 0]
    
    __return_location = [640, 480]

    # Movement code - destination = coordinates in a list
    def move(self, destination, frame, nextFrame, player_sprite):
        
        # If not in middle of room, move to middle then to destination
        if destination[1] != 480 and destination != self.current_location:
            self.__move_player([destination[0], 480], frame, nextFrame, player_sprite)
        
        # then move player to target location
        self.__move_player(destination, frame, nextFrame, player_sprite)
        
        # store target location so can move from there
        self.current_location = destination
    
    # movement code - background is scrolled
    def __move_player(self, destination, frame, nextFrame, player_sprite):
        
        if self.current_location[1] <= destination[1]:
            
            while self.current_location[1] != destination[1]:
                if clock() > nextFrame:
                    frame = (frame+1)%6
                    nextFrame += 60
                pause(5)
                changeSpriteImage(player_sprite, 1*6+frame)
                scrollBackground(0, 5)
                self.current_location[1] += 5
        
        elif self.current_location[1] >= destination[1]:
            
            while self.current_location[1] != destination[1]:
                if clock() > nextFrame:
                    frame = (frame+1)%6
                    nextFrame += 60
                pause(5)
                changeSpriteImage(player_sprite, 3*6+frame)
                scrollBackground(0, -5)
                self.current_location[1] -= 5
        
        if self.current_location[0] <= destination[0]:
            
            while self.current_location[0] != destination[0]:
                if clock() > nextFrame:
                    frame = (frame+1)%6
                    nextFrame += 60
                pause(5)
                changeSpriteImage(player_sprite, 2*6+frame)
                scrollBackground(5, 0)
                self.current_location[0] += 5
        
        elif self.current_location[0] >= destination[0]:
            
            while self.current_location[0] != destination[0]:
                
                if clock() > nextFrame:
                    frame = (frame+1)%6
                    nextFrame += 60
                
                pause(5)
                
                changeSpriteImage(player_sprite, 0*6+frame)
                scrollBackground(-5, 0)
                self.current_location[0] -= 5

    # use for movement testing and finding coordinates of an item on the screen - not needed for gameplay
    # def get_current_location(self, player_sprite, frame):
    #     if keyPressed("right"):
    #         changeSpriteImage(player_sprite, 0*6+frame)    
    #         scrollBackground(-5,0)
    #         self.__return_location[0] -= 5

    #     elif keyPressed("down"):
    #         changeSpriteImage(player_sprite, 3*6+frame)    
    #         scrollBackground(0, -5)
    #         self.__return_location[1] -= 5

    #     elif keyPressed("left"):
    #         changeSpriteImage(player_sprite, 2*6+frame)    
    #         scrollBackground(5,0)
    #         self.__return_location[0] += 5

    #     elif keyPressed("up"):
    #         changeSpriteImage(player_sprite,1*6+frame)
    #         scrollBackground(0,5)
    #         self.__return_location[1] += 5