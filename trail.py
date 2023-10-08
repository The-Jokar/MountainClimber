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
        """
        Removes the branch, should just leave the remaining following trail.
        Complexity: O(1) for best and worst case
        """
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
        Complexity: O(1) for best and worst case
        """
        if self.mountain == None: 
            raise ValueError
        else:
            return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain in series before the current one.
        Complexity: O(1) for best and worst case
        """
        try:
            return TrailSeries(mountain, Trail(self))
        except:
            raise ValueError

    def add_empty_branch_before(self) -> TrailStore:
        """Returns a *new* trail which would be the result of:
        Adding an empty branch, where the current trailstore is now the following path.
        Complexity: O(1) for best and worst case
        """
        try:
            return TrailSplit(Trail(None), Trail(None), Trail(self))
        except:
            raise ValueError

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain after the current mountain, but before the following trail.
        Complexity: O(1) for best and worst case
        """
        try:
            return TrailSeries(self.mountain, Trail(TrailSeries(mountain, self.following)))
        except:
            raise ValueError

    def add_empty_branch_after(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch after the current mountain, but before the following trail.
        Complexity: O(1) for best and worst case
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
        Complexity: O(1) for best and worst case
        """
        return Trail(TrailSeries(mountain, self))

    def add_empty_branch_before(self) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch before everything currently in the trail.
        Complexity: O(1) for best and worst case
        """
        return Trail(TrailSplit(Trail(None), Trail(None), self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """
        Follow a path and add mountains according to a personality.
        Complexity: O(n) for best and worst case where n is the total number of trails 
        """
        #first importing personality and establishing variables, no path which tells us when we've exhausted alll paths
        #remaining path which is a linked stack that will contain all the possible paths to go after encountering a trail split
        from personality import PersonalityDecision
        remaining_paths = LinkedStack()
        no_paths = False
        current_path = self.store

        #while loop will continue to iterate until there are no more paths to travel
        while not no_paths:
            #if we encounter a trail series the mountain is added and the path we follow is updated to be following
            if isinstance(current_path, TrailSeries):
                personality.add_mountain(current_path.mountain)
                current_path = current_path.following.store

            #if we encounter a trailsplit first we push the following paths onto the stack so they can be accessed later
            #and then choose the personality
            elif isinstance(current_path, TrailSplit):
                remaining_paths.push(current_path.following)
                choice = personality.select_branch(current_path.top, current_path.bottom)

                #if the personailty decision is bottom we take the bottom path of the split
                if choice == PersonalityDecision.BOTTOM:
                    current_path = current_path.bottom.store
                
                #if the personailty decision is top we take the top path of the split
                elif choice == PersonalityDecision.TOP:
                    current_path = current_path.top.store

                #if the personailty decision is stop we stop follwing paths and end the function
                elif choice == PersonalityDecision.STOP:
                    return
            
            #if there is still paths for us to follow we take the next path of the top of the stack and start the loop again
            elif len(remaining_paths) != 0:
                temp = remaining_paths.pop()
                current_path = temp.store
            
            #if there is no paths left we switch no paths to true and the while loop ends
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
