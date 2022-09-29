import sys

class llist:
    def __init__self(self, value=None, priority=0):
        self.value = value
        self.priority = priority
        
    def contains(self, value, priority):
        return False
        
    def insert(self, value, priority):
        self.value = value
        
    def is_empty(self):
        return False
        
    def pop_min(self):
        return self.value
        
    def print(self):
        return
