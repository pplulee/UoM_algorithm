import sys
import random

# This will have a large impact on performance, try playing with it
MAX_LEVEL = 20

class node:
    def __init__(self, value, priority,levels):
        self.priority = priority
        self.value = value
        self.height = levels
        self.next = [None] * levels

class skiplist:
    def __init__(self):
        self.levels = 1
        self.size = 0
        self.header = node(None,sys.maxsize,MAX_LEVEL)
        for i in range(MAX_LEVEL):
            self.header.next[i] = self.header
            
    def is_empty(self):
        return self.size <= 0
        
    # Returns the last node with priority less than 'priority'
    #
    # Records in 'updates' the nodes along the path that would need updating if a node to
    # their right on their level were to be inserted e.g. the nodes at which the decision
    # to go 'down' is made
    def search(self, priority, updates):
        node = self.header
        level = MAX_LEVEL
        while (level > 0):
            level = level - 1
            
            while (node.next[level].priority < priority):
                node = node.next[level]
            
            # Record the node where we go down at a particular level
            if (not updates == None):
                updates[level] = node
        
        return node
        
    def insert(self, value, priority):
        updates = [None] * MAX_LEVEL
        insert_at = self.search(priority, updates)
        
        levels = 1
        while (levels < MAX_LEVEL and random.randint(0,1) == 0):
            levels = levels + 1
        
        new_node = node(value,priority,levels)
        
        for i in range(levels):
            new_node.next[i] = updates[i].next[i]
            updates[i].next[i] = new_node
            
        self.size = self.size + 1
        
    def contains(self, value, priority):
        node = self.search(priority, None).next[0]
        while (node.priority == priority and (not node.value == None) and (not node.value == value)):
            node = node.next[0]
        return (node.priority == priority and (not node.value == None) and node.value == value)
        
    def pop_min(self):
        min = self.header.next[0]
        res = min.value
        
        for i in range(min.height):
            self.header.next[i] = min.next[i]
        
        self.size = self.size - 1
        return res
        
    # There are probably nicer ways to print a skiplist
    def print(self):
    
        node = self.header
        sys.stdout.write("(%s,%s,%s)\n" % (node.value, node.priority, node.height))
        node = node.next[0]
        while (not node == self.header):
            sys.stdout.write("(%s,%s,%s)\n" % (node.value, node.priority, node.height))
            node = node.next[0]
        
