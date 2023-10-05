from __future__ import annotations

from mountain import Mountain
from algorithms.binary_search import binary_search

class MountainOrganiser:

    def __init__(self) -> None:
        self.mountains = []
        self.mountain_difficulty = []
        self.is_insert = False

    def cur_position(self, mountain: Mountain) -> int:
        if self.is_insert or mountain in self.mountains:
            difficulty = mountain.difficulty_level
            pos = binary_search(self.mountain_difficulty, difficulty)
            if mountain not in self.mountains and difficulty in self.mountain_difficulty:
                pos += 1
            if mountain in self.mountains and difficulty in self.mountain_difficulty:
                pos = self.mountains.index(mountain)
            return pos
        else:
            raise KeyError

    def add_mountains(self, mountains: list[Mountain]) -> None:
        self.is_insert = True
        for mountain in mountains:
            pos = self.cur_position(mountain)
            self.mountains.insert(pos, mountain)
            self.mountain_difficulty.insert(pos, mountain.difficulty_level)
        self.is_insert = False

    def __str__(self):
        return self.mountains
