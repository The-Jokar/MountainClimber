from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR
from data_structures.hash_table import LinearProbeTable

import unittest

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        """
        Initialises the base hash table, size of the internal hash table and the size index
        Complexity: O(1)
        """
        #checks if sizes have been input and if so updates ttable sizes
        if sizes is not None:
            self.TABLE_SIZES = sizes
        #creates the size index which will be updated if the table needs to be resized
        self.size_index = 0
        #initialises the array that is the external hash table as well as the count of the number of keys in the external table
        self.array:ArrayR[tuple[tuple[K1, K2], V]] = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0
        
        #initialises internal table sizes
        if internal_sizes != None:
            self.internal_sizes = internal_sizes
        else:
            self.internal_sizes = self.TABLE_SIZES


    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """
        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.

        Complexity: best case is O(1) where the keys are being inserted and there is nothing at key1's position so it returns after one iteration
        worst case is O(n * m) where n is the size of the external hash table and m is the size of the internal hash table it occurs when key1 already exists in the table
        and multiple conflicts occur when inserting both key1 and key2
        """
        #frist we get the position for key1
        pos1 = self.hash1(key1)
        array = self.array
        
        #begin iterating through the hash table
        for _ in range(self.table_size):
            #if there is an empty space as the position we update the position to a tuple containing key1 and a hash table
            if array[pos1] is None:
                if is_insert:
                    array[pos1] = (key1, LinearProbeTable(self.internal_sizes))
                    #count of external hash table is increased and hash function for internal table is updated to use hash2
                    self.count += 1
                    array[pos1][1].hash = lambda k: self.hash2(key2, array[pos1][1])
                    #get the position of the second key and the return a tuple of key1's positon and key2's position
                    pos2 = self.hash2(key2, array[pos1][1])
                    return (pos1, pos2)
                else:
                    #if we are not inserting raise a key error as a key should be there
                    raise KeyError(key1)

            #if key1 is already in the table 
            elif array[pos1][0] == key1:
                # we initiate hash 2 as the hash function
                array[pos1][1].hash = lambda k: self.hash2(key2, array[pos1][1])
                #get the postion of key2 in the internal table using the linear probe function
                pos2 = array[pos1][1]._linear_probe(key2, is_insert)
                #return position 1 and 2
                return (pos1, pos2)

            else:
                #otheriwse we increase position 1 by 1
                pos1 = (pos1 + 1) % self.table_size
        
        #if we have iterated through the whole table and not found the positons we raise full error if we
        #were inserting or key eror if we were searching
        if is_insert:
            raise FullError
        else:
            raise KeyError
                    

    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        Complexity: see keys
        """
        #returns an iterator of keys based on input
        keys = self.keys(key)
        return iter(keys)

    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        Complexity: best case is O(n) where the key is none amd n is the size of the external hash table
        worst case is O(n * m) where a key is given and it is at the end of the hash table and n is the size of the external hash table
        and m is the size of the internal hash table
        """
        #initialise variable for function
        res = []
        array = self.array

        #if the key is none get all top level keys and append them to results
        if key == None:
            for i in range(len(array)):
                if array[i] != None:
                    res.append(array[i][0])
        
        # if there is a given key for that key get all bottom level keys and append them to the result
        else:
            for i in range(len(array)):
                if array[i][0] == key:
                    for i in len(array[i][1]):
                        if array[i][1] != None:
                            res.append(array[i][1][0])
        
        return res
            

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        Complexity: see values
        """
        #creates an iterator for given values
        values = self.values(key)
        return iter(values)

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        res = []
        array = self.array

        #if key is None get all values by using 2 for loops one for external table and one for the internal tables
        if key is None:
            for i in range(len(array)):
                if array[i] != None:
                    for j in range(len(array[i][1])):
                        if array[i][1][j] is not None:
                            res.append(array[i][1][j][1])
            return res
        
        #other wise we find the position of the key then get all values for that key by iterating through the internal hash table
        else:
            for i in range(len(self)):
                if array[i][0] == key:
                    pos = i

            for i in range(len(self.internal_sizes)):
                if array[pos][1][i] is not None:
                    res.append(array[pos][1][i][1])

            return res

    def __contains__(self, key: tuple[K1, K2]) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        Complexity: see linear probe
        """
        #linear probe then returns the value
        pos = self._linear_probe(key[0], key[1], False)
        return self.array[pos[0]][1][pos[1]][1]


    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        Complexity: see linear probe
        """
        #linear probes to get the positions
        pos = self._linear_probe(key[0], key[1], True)
        array = self.array

        #inputs key data pair at the position and increases count
        if array[pos[0]][1][pos[1]] is not None:
            array[pos[0]][1].count += 1
            self.count+=1
        array[pos[0]][1][pos[1]] = (key[1], data)

        #rehashes the table if the table size becomes too large
        if len(self) > self.table_size / 2:
            self._rehash()

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        Complexity: see linear probe
        """
        #linear probes for the positions
        pos = self._linear_probe(key[0], key[1], False)
        array = self.array

        #if there are not other keys in the internal table we remove the table and set pos1 to None
        if self.keys(key[0]) == [key[1]]:
            array[pos[0]] = None
            self.count -= 2
        #if there are more key data pairs in the internal table we set pos2 to none
        else:
            array[pos[0]][1][pos[1]] = None
            array[pos[0]][1].count -= 1 
        

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        #creates a copy of the array and increases the size index
        old_array = self.array
        self.size_index += 1

        #if we are already at maximum table size end function
        if self.size_index == (len(self.TABLE_SIZES) - 1):
            return
        
        #reset current array anf count
        self.array = ArrayR(self.TABLE_SIZES[self.size_index])
        self.count = 0

        #iterate through the array copy and ass everthing back into the array
        for item in old_array:
            if item is not None:
                key, value = item
                self.hash_table[key] = value


        
    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return len(self.array)

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        pass
