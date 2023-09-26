from __future__ import annotations
from abc import ABC, abstractmethod
from enum import auto
from base_enum import BaseEnum
from mountain import Mountain
from trail import Trail

class PersonalityDecision(BaseEnum):
    TOP = auto()
    BOTTOM = auto()
    STOP = auto()

class WalkerPersonality(ABC):

    def __init__(self) -> None:
        self.mountains = []

    def add_mountain(self, mountain: Mountain) -> None:
        self.mountains.append(mountain)

    @abstractmethod
    def select_branch(self, top_branch: Trail, bottom_branch: Trail) -> PersonalityDecision:
        raise NotImplementedError()

class TopWalker(WalkerPersonality):
    def select_branch(self, top_branch: Trail, bottom_branch: Trail) -> PersonalityDecision:
        # Always select the top branch
        return PersonalityDecision.TOP

class BottomWalker(WalkerPersonality):
    def select_branch(self, top_branch: Trail, bottom_branch: Trail) -> PersonalityDecision:
        # Always select the bottom branch
        return PersonalityDecision.BOTTOM

class LazyWalker(WalkerPersonality):
    def select_branch(self, top_branch: TrailStore, bottom_branch: TrailStore) -> PersonalityDecision:
        """
        Try looking into the first mountain on each branch,
        take the path of least difficulty.
        """

        top_m = top_branch.store.__class__.__name__ == "TrailSeries"
        bot_m = bottom_branch.store.__class__.__name__ == "TrailSeries"
        if top_m and bot_m:
            # If both mountains have the same difficulty and length,
            # take the path with the smaller index.
            if top_branch.store.mountain.difficulty_level == bottom_branch.store.mountain.difficulty_level and top_branch.store.mountain.length == bottom_branch.store.mountain.length:
                if top_branch.store.__class__.__name__ == "TrailSeries" and bottom_branch.store.__class__.__name__ == "TrailSeries":
                    if top_branch.store.mountain.index < bottom_branch.store.mountain.index:
                        return PersonalityDecision.TOP
                    else:
                        return PersonalityDecision.BOTTOM
            # Otherwise, take the path of least difficulty.
            elif top_branch.store.mountain.difficulty_level < bottom_branch.store.mountain.difficulty_level:
                return PersonalityDecision.TOP
            else:
                return PersonalityDecision.BOTTOM
        # If one of them has a mountain, don't take it.
        # If neither do, then take the top branch.
        if top_m:
            return PersonalityDecision.BOTTOM
        return PersonalityDecision.TOP
