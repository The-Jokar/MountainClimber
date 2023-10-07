from __future__ import annotations
from mountain import Mountain
from mountain_organiser import MountainOrganiser

class MountainManager:

    def __init__(self) -> None:
        """
        Initialises a list of mountains and creates an instance of moutnain organiser
        Complexity: O(1)
        """
        self.mountains = []
        self.organiser = MountainOrganiser()

    def add_mountain(self, mountain: Mountain) -> None:
        """
        Adds a mountain to the list
        Complexity: O(1)
        """
        self.mountains.append(mountain)

    def remove_mountain(self, mountain: Mountain) -> None:
        """
        Removes a mountain from the list
        Complexity: O(1)
        """
        self.mountains.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        """
        Edits an already existing mountain
        Complexity: O(1)
        """
        pos = self.mountains.index(old)
        self.mountains[pos] = new

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        """
        Groups mountains with the same sifficulty level
        Complexity: O(n) for best and worst case where n is the number of moutnains already in the list
        """
        res = []
        #we iterate through all the mountains and compare them to the given dif and if they are the same append them to the result
        for mount in self.mountains:
            if mount.difficulty_level == diff:
                res.append(mount)
        
        return res


    def group_by_difficulty(self) -> list[list[Mountain]]:
        """
        Groups all mountains with the same difficult together
        Complexity: best and worst case is O(nlogn) where n is the number of mountains in the existing list
        """
        #first we clear the organisers list
        self.organiser.lst_mountains = []
        self.organiser.mountains_difficulty = []
        #then add all the mountains to the organiser adn get a sorted list returned
        self.organiser.add_mountains(self.mountains)
        sorted_list = self.organiser.lst_mountains
        #initialise variables inorder to slice the list into smaller lists
        res = []
        lower = 0
        upper = 1
        prev_dif = 0
        
        #iterate through the sorted list
        for i in range(len(sorted_list)):
            #get the difficulty level fo the current 
            cur_dif = sorted_list[i].difficulty_level
            #if the current mountains difficulty is the same as the orevious we increse upper by 1
            if cur_dif == prev_dif:
                upper += 1
            #if the previous dif isnt assigned yet and prev wasnt the same as current
            elif prev_dif != 0:
                #then we append a sliced list from the lower bound to the upper bound which contains all the mountains with that difficulty
                res.append(sorted_list[lower:upper])
                #then we set lower to upper and increase upper by one
                lower = upper
                upper += 1
                #finally the cur dif becomes prev dif
            prev_dif = cur_dif
        
        #finally we append the last slice after we reach the end of the list and then return the result
        res.append(sorted_list[lower:upper])
        return res
    

                

