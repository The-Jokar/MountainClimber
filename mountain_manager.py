from __future__ import annotations
from mountain import Mountain
from mountain_organiser import MountainOrganiser

class MountainManager:

    def __init__(self) -> None:
        self.mountains = []
        self.organiser = MountainOrganiser()

    def add_mountain(self, mountain: Mountain) -> None:
        self.mountains.append(mountain)

    def remove_mountain(self, mountain: Mountain) -> None:
        self.mountains.remove(mountain)

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        pos = self.mountains.index(old)
        self.mountains[pos] = new

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        res = []
        for mount in self.mountains:
            if mount.difficulty_level == diff:
                res.append(mount)
        
        return res


    def group_by_difficulty(self) -> list[list[Mountain]]:
        self.organiser.lst_mountains = []
        self.organiser.mountains_difficulty = []
        self.organiser.add_mountains(self.mountains)
        sorted_list = self.organiser.lst_mountains
        res = []
        lower = 0
        upper = 1
        prev_dif = 0
        
        for i in range(len(sorted_list)):
            cur_dif = sorted_list[i].difficulty_level
            if cur_dif == prev_dif:
                upper += 1
            elif prev_dif != 0:
                res.append(sorted_list[lower:upper])
                lower = upper
                upper += 1
            prev_dif = cur_dif
            
        res.append(sorted_list[lower:upper])
        return res
    

                

