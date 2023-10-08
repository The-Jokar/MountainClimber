from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.
    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.
    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27

    def __init__(self, level = 0) -> None:
        #Initialize the hash table
        self.count = 0
        self.level = level
        self.hash_table: ArrayR[tuple[K, V]] = ArrayR(self.TABLE_SIZE)

    def hash(self, key: K) -> int:
        #Checking
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1

    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """

        #Get the position in the hash tables using the previously hash function in the hash method
        result = self.hash_table[self.hash(key)]

        #See if the slot is empty
        if result == None:
            raise KeyError

        #See if the key matches the key at this position
        elif result[0] == key:
            return result[1]

        #Check to see if it is an InfiniteHashtable
        elif type(result) == InfiniteHashTable:
            return result[key][1]
        else:
            raise KeyError

    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        Best case complexity is O(1), but can become O(N) with hash collisions and when rehashing is needed
        """

        #Used to calculate the position in hash table using hash function
        pos = self.hash(key)

        #Incremental count of the key value pairs in the hash function 
        self.count += 1

        if (self.hash_table[pos] is None) or (type(self.hash_table[pos]) == tuple and self.hash_table[pos][0] == key):
            #Checking to see if slot is empty or has a tuple with the same key
            self.hash_table[pos] = (key, value)
        elif type(self.hash_table[pos]) == InfiniteHashTable:
            self.hash_table[pos][key] = value 
        else:
            #Else, if slot has a different value pair create an infiniteHashTable rehash
            result = self.hash_table[pos]
            self.hash_table[pos] = InfiniteHashTable(self.level + 1)
            self.hash_table[pos][result[0]] = result[1]
            self.hash_table[pos][key] = value

    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        Best case Complexity is O(1), but can also become O(N) due to its recursive nature 
        navigating through the nested InfiniteHashTable during hash collisions (up to N times)
        """
        pos = self.hash(key)
        if self.hash_table[pos] == None:
            raise KeyError

        entry = self.hash_table[pos]

        if isinstance(entry, InfiniteHashTable):
            del entry[key]
            self.count -= 1

            if len(entry) == 0:
                self.hash_table[pos] = None
            elif len(entry) == 1:
                for index in entry.hash_table:
                    if index is not None:
                        self.hash_table[pos] = index
                        break
        elif entry[0] == key:
            self.hash_table[pos] = None
            self.count -= 1
        else:
            raise KeyError("Key not found")


    def __len__(self) -> int:
        #Returning length of count
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        raise NotImplementedError()

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        Best case Complexity is O(1), but can also become O(N) due to its recursive nature 
        navigating through the nested InfiniteHashTable during hash collisions (up to N times)
        """
        
        #Calculate current position in hash table depending on the key
        pos = self.hash(key)
        if self.hash_table[pos] is None:
            raise KeyError 
        #Check if slot has an Infinite Hash Table
        elif type(self.hash_table[pos]) == InfiniteHashTable:
            return [pos] + self.hash_table[pos].get_location(key)
        elif self.hash_table[pos][0] == key:
            return [pos]
        #If none of conditions are met, raise an error
        else:
            raise KeyError


    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        Best case Complexity is O(1), but can also become O(N) due to its recursive nature 
        navigating through the nested InfiniteHashTable during hash collisions (up to N times)
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.
        Complexity depends depends on the number of keys in the table and the nesting level, 
        possibly reaching the threshold O(K*N), where K is the number of keys and N is the nesting level
        """
        sorted_keys = []

        #if current is none, create it based on current level
        if current == None:
            if self.level == 0:
                current = [self.hash('')] + [self.hash(i) for i in 'abcdefghijklmnopqrstuvwxyz']
            else: 
                raise Exception('The function cannot be called')

        for i in current:
            result = self.hash_table[i]

            if type(result) == InfiniteHashTable:
                #Recursively collect keys if it contains an infinite hash tables
                sorted_keys += result.sort_keys(current)

            elif type(result) == tuple:
                #Add key to the sorted list if the slot contains a key-value
                sorted_keys.append(result[0]) 
        #Return sorted keys
        return sorted_keys