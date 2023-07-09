import random as rand
import os
from pathlib import Path
from spreadsheet import ScenarioDatabase

# Set root path and json file location
resource_path = Path(__file__).parents[1]                                   # The root folder path
names_text_file = os.path.join(resource_path, 'data/student_names.txt')     # The location of student_names.txt

# Generates random student profiles
class StudentGenerator():
    def __init__(self):
        scenario_database = ScenarioDatabase()
        self.__student_bios_db = scenario_database.student_bios_data

    __student_bios_db = None

    #picks a name from a text file with all cs student names
    def generate_name(self):
        offset = rand.randrange(2, 3181)
        student_names = open(names_text_file)
        student_names.seek(offset)
        student_names.readline()
        name = student_names.readline()

        return name.strip()

    #list of attributes for a student
    class attributes:
        gender = ['male','male','male','male','male','male','male','male', 'female', 'female']
        glasses = ['yes', 'no']
        haircolours = ['brown', 'yellow', 'ginger', 'black', 'silver', 'bald']
        stylechoice = ['goth', 'emo', 'rugby', 'nerd']
        traits = ['angry', 'lazy', 'astute', 'clever', 'clown']
        location = ['wales', 'scotland', 'northern ireland', 'england']
        phone = '07' + str(rand.randrange(123456789, 999999999))
        dob = str(rand.randrange(1,28)) + '/' + str(rand.randrange(1,12)) + '/' + str(rand.randrange(1970,2003))

    #func to randomize student profiles
    def generate_profile(self):
        bio_index = rand.randint(0,13)
        name = self.generate_name()
        bio_text = self.__student_bios_db["bio_text"][bio_index].replace("[name]", name)

        studentprofile = {
            'name': name,
            'gender': rand.choice(self.attributes.gender),
            'phone': self.attributes.phone,
            'dob': self.attributes.dob,
            'glasses': rand.choice(self.attributes.glasses),
            'hair colour': rand.choice(self.attributes.haircolours),
            'style': rand.choice(self.attributes.stylechoice),
            'personality': rand.choice(self.attributes.traits),
            'location': rand.choice(self.attributes.location),
            'bio': bio_text,
            'comments': self.__student_bios_db["excuse"][bio_index]
        }
        return studentprofile 