'''
-8/4/2021
-Coral Generator, a program made by Sebastian Jimenez
-This script is responsible for running the custom GUI for Coral Generator
'''

# Imports
from gooey import Gooey, GooeyParser
import os


# GUI configuration of tabs, size , name, ect..
@Gooey(program_name='Coral Generator', default_size=(3000, 2200),
               program_description='A program that creates coral visualizations of the 3N+1 phenomenon',
               menu=[{
                   'name': 'File',
                   'items': [{
                       'type': 'AboutDialog',
                       'menuTitle': 'About',
                       'name': 'Coral Generator',
                       'description': '2021',
                       'website': 'https://potassium3919.itch.io/',
                       'developer': 'Sebastian Jimenez',

                   }]
               }])
# contains attributes that are refined versions of the GUI inputs
class CoralGUI:

    def __init__(self):
        self.output_directory = None
        self.color_selected = None
        self.range_selected = None
        self.primes_only = None
        self.odd_angle = None
        self.even_angle = None
        self.width = None
        self.length = None

    # custom gui
    def start_get_and_clean(self):

        # get inputs section
        parser = GooeyParser()

        parser.add_argument('output_directory',
                            metavar='Output Location', widget='DirChooser',
                            default=rf'{os.path.join(os.getcwd(), "Coral Graphics")}',
                            help='Enter output directory')

        modified_input = 'str(user_input).replace(" ", "").split(",")'
        parser.add_argument('range_selected',
                            metavar='Select Range',
                            default='9, 1000',
                            help='Enter two different positive integers separated by a comma to determine the inclusive'
                                 ' range',
                            gooey_options={
                                'validator': {
                                    'test': f'len({modified_input}) == 2 and {modified_input}[0].isdigit() '
                                            f'and {modified_input}[1].isdigit() and '
                                            f'{modified_input}[0] != {modified_input}[1]'
                                            f'and "0" not in {modified_input}',
                                    'message': 'Only two different positive integers will be accepted'}})

        parser.add_argument('-color_selected',
                            metavar='Color Selection', widget='ColourChooser',
                            default='#e9967a',  # darksalmon
                            help='Select the color to draw the coral with')

        parser.add_argument('-primes_only',
                            metavar='Primes Only', widget='CheckBox',
                            help='Toggle whether to only include prime numbers', action='store_true', default=False)

        parser.add_argument('-coral_length',
                            metavar='Coral Length', widget='Slider', default=30,
                            gooey_options={'min': 1, 'max': 60}, help='Enter the length of pixels between each node')

        parser.add_argument('-coral_width',
                            metavar='Coral Width', widget='Slider', default=6,
                            gooey_options={'min': 1, 'max': 20}, help='Enter the width of each segment')

        parser.add_argument('-odd_angle',
                            metavar='Odd Rotation', widget='IntegerField', default=20,
                            gooey_options={'min': -45, 'max': 45},
                            help='Enter number of degrease of rotation at each odd node')

        parser.add_argument('-even_angle',
                            metavar='Even Rotation', widget='IntegerField', default=-8,
                            gooey_options={'min': -45, 'max': 45},
                            help='Enter number of degrease of rotation at each even node')

        inputs = parser.parse_args()

        # set attributes to inputs and perform necessary refining

        # sets default if output directory is not an actual directory
        output_directory = str(inputs.output_directory)

        if not os.path.isdir(output_directory):
            output_directory = os.path.join(os.getcwd(), 'Coral Graphics')

        self.output_directory = output_directory

        self.primes_only = bool(inputs.primes_only)
        self.color_selected = str(inputs.color_selected)

        # turns string input into refined integer list and sorts
        range_selected = str(inputs.range_selected).replace(" ", "").split(",")

        range_selected[0] = int(range_selected[0])
        range_selected[1] = int(range_selected[1])

        range_selected.sort()

        range_selected = range(range_selected[0], range_selected[1]+1)

        self.range_selected = range_selected

        self.width = int(inputs.coral_width)
        self.length = int(inputs.coral_length)
        self.even_angle = int(inputs.even_angle)
        self.odd_angle = int(inputs.odd_angle)





