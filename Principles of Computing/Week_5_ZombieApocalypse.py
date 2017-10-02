"""
Zombie Apocalypse mini-project
"""

import random
import poc_grid
import poc_queue
import poc_zombie_gui

# global constants
EMPTY = 0 
FULL = 1
FOUR_WAY = 0
EIGHT_WAY = 1
OBSTACLE = 5
HUMAN = 6
ZOMBIE = 7


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
        self._grid_height = grid_height
        self._grid_width = grid_width
        if obstacle_list != None:
            for cell in obstacle_list:
                self.set_full(cell[0], cell[1])
        if zombie_list != None:
            self._zombie_list = poc_queue.Queue()
            for zombie in list(zombie_list):
                self._zombie_list.enqueue(zombie)
        else:
            self._zombie_list = poc_queue.Queue()
        if human_list != None:
            self._human_list = poc_queue.Queue()
            for human in list(human_list):
                self._human_list.enqueue(human)
        else:
            self._human_list = poc_queue.Queue()
        
    def clear(self):
        """
        Set cells in obstacle grid to be empty
        Reset zombie and human lists to be empty
        """
        poc_grid.Grid.clear(self)
        self._zombie_list.clear()
        self._human_list.clear()
        
    def add_zombie(self, row, col):
        """
        Add zombie to the zombie list
        """
        self._zombie_list.enqueue((row, col))
        print "Zombie locations: ", self._zombie_list
                
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
            yield zombie

    def add_human(self, row, col):
        """
        Add human to the human list
        """
        self._human_list.enqueue((row, col))
        print "Human locations: ", self._human_list
        
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
            yield human   

    def compute_distance_field(self, entity_type):
        """
        Function computes and returns a 2D distance field
        Distance at member of entity_list is zero
        Shortest paths avoid obstacles and use four-way distances
        """
        # create empty visited grid with original size
        # create 2d list distance_field with original size, 
        # initialize cells to be of value height*width
        visited = poc_grid.Grid(self._grid_height, self._grid_width)
        distance_field = [[self._grid_height * self._grid_width
                          for dummy_col in range(self._grid_width)]
                          for dummy_row in range(self._grid_height)]
        
        # create boundary and initialize as copy of human/ zombie list
        boundary = poc_queue.Queue()
        if entity_type == ZOMBIE:
            for cell in list(self._zombie_list):
                boundary.enqueue(cell)
        if entity_type == HUMAN:
            for cell in list(self._human_list):
                boundary.enqueue(cell)
         
        # set visited to 1 with set_full method and 
        # distance_field to 0 for all cells in boundary       
        for cell in boundary:
            visited.set_full(cell[0], cell[1])
            distance_field[cell[0]][cell[1]] = 0
            
        # breadth-first-search:
        # dequeue boundary cells and get their four neighbours
        # next check if cell has not been visited an is empty, 
        # if so update visited and boundary queue.
        # further update neighbour cell's distance to be distance to current + 1
        while boundary:
            current = boundary.dequeue()
            for neighbour_cell in visited.four_neighbors(current[0], current[1]):
                if visited.is_empty(neighbour_cell[0], neighbour_cell[1]) and self.is_empty(neighbour_cell[0], neighbour_cell[1]):
                    visited.set_full(neighbour_cell[0], neighbour_cell[1])
                    boundary.enqueue(neighbour_cell)
                    distance_field[neighbour_cell[0]][neighbour_cell[1]] = distance_field[current[0]][current[1]] + 1
        return distance_field
       
    def move_humans(self, zombie_distance_field):
        """
        Function that moves humans away from zombies, diagonal moves
        are allowed
        """
        for human in list(self._human_list):
            move = random.choice(self._move(zombie_distance_field, HUMAN, human))
            self._human_list.dequeue()
            self._human_list.enqueue(move[0])

    def move_zombies(self, human_distance_field):
        """
        Function that moves zombies towards humans, no diagonal moves
        are allowed
        """
        for zombie in list(self._zombie_list):
            move = random.choice(self._move(human_distance_field, ZOMBIE, zombie))
            self._zombie_list.dequeue()
            self._zombie_list.enqueue(move[0])

    def _move(self, distance_field, entity_type, entity):
        """
        Helper function that calculates an entity type's next move.
        """
        neighbours = self.four_neighbors(entity[0], entity[1]) if entity_type == ZOMBIE else self.eight_neighbors(entity[0], entity[1])
        move = [(entity, distance_field[entity[0]][entity[1]])]
        
        for cell in neighbours:
            if self.is_empty(cell[0], cell[1]):
                dist = distance_field[cell[0]][cell[1]]
                if entity_type == HUMAN:
                    if dist > move[0][1]:
                        move = [(cell, dist)]
                    elif dist == move[0][1]:
                        move.append((cell, dist))
                elif entity_type == ZOMBIE:
                    if dist < move[0][1]:
                        move = [(cell, dist)]
                    elif dist == move[0][1]:
                        move.append((cell, dist))
        return move


# Start up gui for simulation - You will need to write some code above
# before this will work without errors

poc_zombie_gui.run_gui(Apocalypse(30, 40))
