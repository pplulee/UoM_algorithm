import sys

class llist:
    def __init__(self, value1=None, value2=None, priority=0):
        self.value1 = value1
        self.value2 = value2
        self.priority1 = priority
        self.priority2 = priority
        self.next = None
        self.prev = None
        
    def contains(self, value, priority):
        return False
        
    def insert(self, value, priority):
        if (self.value1 == None):
            self.value1=value
            self.priority1=priority
        else:
            self.value2 = value
            self.priority2 = priority
            if (self.priority2 < self.priority1):
                tv = self.value1
                tp = self.priority1
                self.value1 = self.value2
                self.priority1 = self.priority2
                self.value2 = tv
                self.priority2 = tp
        
    def is_empty(self):
        return False
        
    def pop_min(self):
        res = self.value1
        self.value1 = self.value2
        self.priority1 = self.priority2
        self.value2 = None
        return res
        
    def print(self):
        print("No print implemented")
        
