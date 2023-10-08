from __future__ import annotations

from mountain import Mountain
from algorithms.binary_search import binary_search

class MountainOrganiser:

    def __init__(self) -> None:
        """
        initialises 2 lists one to hold all the mountains, and one to just hold difficulties and a variable to check if we are inserting
        Complexity: O(1) best and worst case
        """
        self.mountains = []
        self.mountain_difficulty = []
        self.is_insert = False

    def cur_position(self, mountain: Mountain) -> int:
        """
        Retrieves the current position of the mountain in the list or finds the position the mountain should be inserted into'
        Complexity: best case is O(1) where the item being inserted is in the middle
        worst case is O(log(n)) where n is the total number of moutnains
        """
        #first we check if we are inserting or searching for a mountain
        if self.is_insert or mountain in self.mountains:
            #we get the difficulty of the current mountain then find its position using binary search
            #on the dificulty list of mountains
            difficulty = mountain.difficulty_level
            pos = binary_search(self.mountain_difficulty, difficulty)
            #if the mountain is not in the list but a mountain with the same difficulty is already in the list then we insert is to the right
            if mountain not in self.mountains and difficulty in self.mountain_difficulty:
                pos += 1
            #if the mountain is already in the list we get the index of it
            if mountain in self.mountains and difficulty in self.mountain_difficulty:
                pos = self.mountains.index(mountain)
            #finally return the position
            return pos
        #if we arent inserting and its not in the list then we raise a key error
        else:
            raise KeyError

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Adds a mountain to the list based on its difficulty and using cur_position to find its location
        Complexity: best case is O(m) where m is the size of the input list and the position they should be placed in is always the middle
        the worst case is O(mlogm + n) where m is the size of the input list and m is the number of mountains already in the list
        """
        #first we change is inset to true then we iterate through the list of mountains
        self.is_insert = True
        for mountain in mountains:
            #we get the position of the current mountain using cur_position and then insert the moutnain
            #into the list of mountains and the mountain difficulty into the list of difficulties given the position from cur_position
            pos = self.cur_position(mountain)
            self.mountains.insert(pos, mountain)
            self.mountain_difficulty.insert(pos, mountain.difficulty_level)
        #finally we reset is insert to false
        self.is_insert = False
