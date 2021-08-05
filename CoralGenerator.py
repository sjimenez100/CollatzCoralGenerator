'''
-8/4/2021
-Coral Generator, a program made by Sebastian Jimenez
-This script is responsible for running the main functionalities of Coral Generator
'''
# imports
import os
from PIL import Image, ImageDraw
import math
import CG_GUI
import sys

# global variables
graphic = Image.new('RGB', (630, 500))
coral_gui = CG_GUI.CoralGUI()


# returns a list with nodes 1 to the starting_value
def get_branch(input_value, branch=None):

    if branch is None:
        branch = list()
        branch.append(input_value)

    if input_value % 2 == 0:
        next_value = input_value / 2
    else:
        next_value = input_value * 3 + 1

    branch.append(next_value)

    if next_value == 1:
        branch.reverse()
        return branch

    return get_branch(next_value, branch)


# returns the desired image coordinates from the cartesian inputs, assuming (0, 0)
def cartesian_to_raw(x, y):
    x += graphic.width / 2
    y = graphic.height - y

    return x, y


# returns a list of node positions (in raw image coordinates) from a branch of integer nodes
def node_positions(branch):
    positions = []

    correction = math.pi/2
    segment_length = coral_gui.length
    even_angle = coral_gui.even_angle
    odd_angle = coral_gui.odd_angle
    stem_angle = 0

    last_position = None

    for node in branch:
        if node == 1:
            position = [0, 0]
            stem_angle += odd_angle
            last_position = position
            positions.append(cartesian_to_raw(position[0], position[1]))
            continue

        stem_radians = math.radians(stem_angle)

        position[0] = last_position[0] + math.cos(stem_radians + correction) * segment_length
        position[1] = last_position[1] + math.sin(stem_radians + correction) * segment_length

        if node % 2 == 0:
            stem_angle += even_angle
        else:
            stem_angle += odd_angle

        last_position = position
        positions.append(cartesian_to_raw(position[0], position[1]))

    return positions


# draws a branch of integer nodes
def draw_branch(branch):
    draw = ImageDraw.Draw(graphic)
    points = node_positions(branch)

    # draws a line between each positional node
    draw.line(points, width=coral_gui.width, fill=coral_gui.color_selected, joint="curve")

    # draws points at each positional node
    for point in points:
        radius = coral_gui.width/3
        draw.ellipse((point[0]-radius, point[1]-radius, point[0]+radius, point[1]+radius), fill='white')


# returns all the prime numbers within v_range
def get_primes(v_range):
    primes = []
    for x in v_range:
        prime = False
        for p in range(2, x):

            if x == 1:
                prime = True
                break
            if x % p == 0:
                prime = False
                break
            else:
                prime = True

        if prime:
            primes.append(x)

    return primes


# returns the starting nodes
def define_starting_nodes():
    nodes = []

    if coral_gui.primes_only:
        nodes = get_primes(coral_gui.range_selected)
    else:
        for value in coral_gui.range_selected:
            nodes.append(value)

    return nodes


# saves the the graphic and performs other relevant things
def save_image():
    i = 0

    if 'Coral Graphics' not in os.listdir(os.getcwd()):
        os.mkdir('Coral Graphics')

    for file in os.listdir(coral_gui.output_directory):
        if 'CoralGraphic' in file:
            i += 1

    if i == 0:
        i = ''

    graphic.save(os.path.join(coral_gui.output_directory, f'CoralGraphic{i}.jpg'))

    if 'Desktop' not in coral_gui.output_directory:
        os.startfile(coral_gui.output_directory)

    graphic.show()


# ensures that system does not ignore print() updates
def config_gui():
    class Unbuffered(object):
        def __init__(self, stream):
            self.stream = stream

        def write(self, data):
            self.stream.write(data)
            self.stream.flush()

        def writelines(self, datas):
            self.stream.writelines(datas)
            self.stream.flush()

        def __getattr__(self, attr):
            return getattr(self.stream, attr)

    sys.stdout = Unbuffered(sys.stdout)


def main():
    config_gui()

    # used to define the instance coral_gui's attributes
    coral_gui.start_get_and_clean()

    print('New Process Initiated')
    branches = []

    print(f'Getting Branches...', end=' ')
    starting_nodes = define_starting_nodes()
    # fills the list "branches" with branches from each starting node
    for starting_node in starting_nodes:
        branches.append(get_branch(starting_node))
    print('Done')

    # reverses the order of branches by len() : shortest first
    branches.sort(reverse=True)

    print('Drawing Branches...', end=" ")
    # draws each branch
    for branch in branches:
        draw_branch(branch)
    print('Done')

    print('Saving Image...', end=" ")
    save_image()
    print('Done')
    print('Process Complete')
    print()


if __name__ == '__main__':
    main()

