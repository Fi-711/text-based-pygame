# Install pygame module through pip - must use python version below 3.8
import os, sys, pygame
sys.path.append(os.path.join(os.path.dirname(__file__), 'resources/scripts'))   # can now import from resources/scripts
from pygame_functions import * 
from game_manager import GameManager
# import pygame_functions, insert_name, scenario_manager

# Initialize pygame
pygame.init()

# Create screen display - 4:3 aspect ratio
display_width = 1280
display_height = 960
screenSize(display_width, display_height)

# Auto update display
setAutoUpdate = False

# Set default paths for directories
current_path = os.path.dirname(__file__)                        # Where this file is located
resource_path = os.path.join(current_path, 'resources')         # The resource folder path
image_path = os.path.join(resource_path, 'images')              # The image folder path
music_path = os.path.join(resource_path, 'music')               # The music folder path
fonts_path = os.path.join(resource_path, 'fonts')               # The fonts folder path

# Title and Icon
pygame.display.set_caption("Clean and Code")
icon = pygame.image.load(os.path.join(image_path, 'book.png'))
pygame.display.set_icon(icon)

# Images
office_img = os.path.join(image_path, 'office_room.png')
workshop_img = os.path.join(image_path, 'workshop_room.png')
lecture_img = os.path.join(image_path, 'lecture_room.png')
staff_room_img = os.path.join(image_path, 'staff_room.png')
meet_the_boss_img = os.path.join(image_path, 'boss_room.png')
player_img = os.path.join(image_path, 'player_sprite.png')
grass_img = os.path.join(image_path, 'grass.png')
boss_img = os.path.join(image_path, 'boss.png')

# Music
intro_music = makeMusic(os.path.join(music_path, 'intro.ogg'))
playMusic()

# Player sprite
player_sprite = makeSprite(player_img, 24)
moveSprite(player_sprite,display_width/2, display_height/2, True)
showSprite(player_sprite)


# Main Game Loop ----------------------------------------------------- #
def main():

    # Game Setup - background images in [6x2]
    setBackgroundImage([[office_img, grass_img, meet_the_boss_img, staff_room_img, lecture_img, workshop_img],         
                        [grass_img, grass_img, grass_img, grass_img, grass_img, grass_img]])

    nextFrame = clock()
    frame = 0

    # Initialize Game Manager - controls all game logic
    game_manager = GameManager(frame, nextFrame, player_sprite)

    # closes game
    endWait()


if __name__ == "__main__":
    main()
