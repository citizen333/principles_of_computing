"""
Student portion of Zombie Apocalypse mini-project
"""

import random
from poc.zombie_apocalypse import poc_grid
from poc.zombie_apocalypse import poc_queue
# import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7

class Queue:
    """
    A simple implementation of a FIFO queue.
    """

    def __init__(self):
        """ 
        Initialize the queue.
        """
        self._items = []

    def __len__(self):
        """
        Return the number of items in the queue.
        """
        return len(self._items)
    
    def __iter__(self):
        """
        Create an iterator for the queue.
        """
        for item in self._items:
            yield item

    def __str__(self):
        """
        Return a string representation of the queue.
        """
        return str(self._items)

    def enqueue(self, item):
        """
        Add item to the queue.
        """        
        self._items.append(item)

    def dequeue(self):
        """
        Remove and return the least recently inserted item.
        """
        return self._items.pop(0)

    def clear(self):
        """
        Remove all items from the queue.
        """
        self._items = []

class Apocalypse(poc_grid.Grid):
    """
    Class for simulating zombie pursuit of human on grid with
    obstacles
    """

    def __init__(self, grid_height, grid_width, obstacle_list = None, 
                 zombie_list = None, human_list = None):
        """
        Create a simulation of given size with given obstacles,
        humans, and zombies
        """
        poc_grid.Grid.__init__(self, grid_height, grid_width)
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = list(zombie_list)
        else:
            self._zombie_list = []
        if human_list != None:
            self._human_list = list(human_list)  
        else:
            self._human_list = []
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list = []
        self._human_list = []
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.append((row, col))
        
    def num_zombies(self):
        """
        Return number of zombies
        """
        return len(self._zombie_list)      

    def zombies(self):
        """
        Generator that yields the zombies in the order they were
        added.
        """
        for zombie in self._zombie_list:
            yield tuple(zombie)

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.append((row, col))
        
    def num_humans(self):
        """
        Return number of humans
        """
        return len(self._human_list)
    
    def humans(self):
        """
        Generator that yields the humans in the order they were added.
        """
        for human in self._human_list:
            yield tuple(human)
        
    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        entity_dict = {
            ZOMBIE: self._zombie_list,
            HUMAN: self._human_list
        }
        grid_height = self.get_grid_height()
        grid_width = self.get_grid_width()
        visited = poc_grid.Grid(grid_height, grid_width)
        distance_field = [[grid_width * grid_height] * grid_width
                          for _ in range(grid_height)]
        boundary = Queue()
        for cell in entity_dict[entity_type]:
            boundary.enqueue(cell)
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
        while len(boundary) > 0:
            current_cell = boundary.dequeue()
            neighbours_list = poc_grid.Grid.four_neighbors(self,
                                                           current_cell[0],
                                                           current_cell[1])
            for neighbour in neighbours_list:
                if (visited.is_empty(neighbour[0], neighbour[1])
                    and self.is_empty(neighbour[0], neighbour[1])):
                    visited.set_full(neighbour[0], neighbour[1])
                    distance =(
                        distance_field[current_cell[0]][current_cell[1]] + 1
                    )
                    distance_field[neighbour[0]][neighbour[1]] = distance
                    boundary.enqueue(neighbour)
        
        return distance_field
        
    
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        dummy_human_list = list()
        for human in self._human_list:
            new_distance = zombie_distance_field[human[0]][human[1]]
            possible_moves = [human]
            neighbours_list = self.eight_neighbors(human[0], human[1])
            for neighbour in neighbours_list:
                if self.is_empty(neighbour[0], neighbour[1]):
                    neighbour_distance =\
                        zombie_distance_field[neighbour[0]][neighbour[1]]
                    if neighbour_distance > new_distance:
                        new_distance = neighbour_distance
                        possible_moves = list()
                    if neighbour_distance >= new_distance:
                        possible_moves.append(neighbour)
            dummy_human_list.append(random.choice(possible_moves))
        
        self._human_list = dummy_human_list

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        dummy_zombie_list = list()
        for zombie in self._zombie_list:
            new_distance = human_distance_field[zombie[0]][zombie[1]]
            possible_moves = [zombie]
            neighbours_list = self.four_neighbors(zombie[0], zombie[1])
            for neighbour in neighbours_list:
                if self.is_empty(neighbour[0], neighbour[1]):
                    neighbour_distance =\
                        human_distance_field[neighbour[0]][neighbour[1]]
                    if neighbour_distance < new_distance:
                        new_distance = neighbour_distance
                        possible_moves = list()
                    if neighbour_distance <= new_distance:
                        possible_moves.append(neighbour)
            dummy_zombie_list.append(random.choice(possible_moves))
        
        self._zombie_list = dummy_zombie_list

# Start up gui for simulation - You will need to write some code above
# before this will work without errors

# poc_zombie_gui.run_gui(Apocalypse(30, 40))

obj = Apocalypse(3, 3, [], [(1, 1)], [])
obj.add_human(1, 1)
print(obj)
print("humans", str(list(obj.humans())))
print("zombies", str(list(obj.zombies())))