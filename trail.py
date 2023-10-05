from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain
from data_structures.linked_stack import LinkedStack

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Trail
    bottom: Trail
    following: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        return self.following.store

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Removing the mountain at the beginning of this series.
        """
        if self.mountain == None: 
            raise ValueError
        else:
            return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain in series before the current one.
        """
        try:
            return TrailSeries(mountain, Trail(self))
        except:
            raise ValueError

    def add_empty_branch_before(self) -> TrailStore:
        """Returns a *new* trail which would be the result of:
        Adding an empty branch, where the current trailstore is now the following path.
        """
        try:
            return TrailSplit(Trail(None), Trail(None), Trail(self))
        except:
            raise ValueError

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain after the current mountain, but before the following trail.
        """
        try:
            return TrailSeries(self.mountain, Trail(TrailSeries(mountain, self.following)))
        except:
            raise ValueError

    def add_empty_branch_after(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch after the current mountain, but before the following trail.
        """
        try:
            return TrailSeries(self.mountain, Trail(TrailSplit(Trail(None), Trail(None), self.following)))
        except:
            raise ValueError

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain before everything currently in the trail.
        """
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch before everything currently in the trail.
        """
        return Trail(TrailSplit(Trail(None), Trail(None), self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        from personality import PersonalityDecision
        remaining_paths = LinkedStack()
        no_paths = False
        current_path = self.store

        while not no_paths:
            if isinstance(current_path, TrailSeries):
                personality.add_mountain(current_path.mountain)
                current_path = current_path.following.store

            elif isinstance(current_path, TrailSplit):
                remaining_paths.push(current_path.following)
                choice = personality.select_branch(current_path.top, current_path.bottom)

                if choice == PersonalityDecision.BOTTOM:
                    current_path = current_path.bottom.store
                
                elif choice == PersonalityDecision.TOP:
                    current_path = current_path.top.store

                elif choice == PersonalityDecision.STOP:
                    return
            
            elif len(remaining_paths) != 0:
                temp = remaining_paths.pop()
                current_path = temp.store
            
            else:
                no_paths = True
        
        return
        

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        

    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!
        pass

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        pass
