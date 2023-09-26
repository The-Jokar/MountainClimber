from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from typing import TYPE_CHECKING, Union

from data_structures.linked_stack import LinkedStack

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality, PersonalityDecision

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
        """Follows the trail, calling personality.add_mountain for every mountain passed by.

        Args:
            personality: A WalkerPersonality object.
        """

        from personality import PersonalityDecision
        stack: list[TrailStore] = [self.store]
        while stack:
            current = stack.pop()

            if isinstance(current, TrailSeries):
                personality.add_mountain(current.mountain)
                stack.append(current.following.store)

            elif isinstance(current, TrailSplit):
                decision = personality.select_branch(current.top, current.bottom)
                
                if decision == PersonalityDecision.TOP:
                    stack.append(current.top.store)
                elif decision == PersonalityDecision.BOTTOM:
                    stack.append(current.bottom.store)
                # If decision is STOP, we don't add anything to the stack

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        pass

    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!
        pass

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        pass
