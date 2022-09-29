import sys

class llist:
    # We will use a dummy node (value = None, priority = 0) for the head of the list
    def __init__(self, value=None, priority=0):
        self.value = value
        self.priority = priority
        self.next = None
        self.prev = None

    def contains(self, value, priority):
        # Linear Search
        tmp_next = self.next;
        while (not tmp_next == None):
            if (tmp_next.value == value and tmp_next.priority == priority):
                return True
            tmp_next = tmp_next.next
        return False
        
    def insert(self, value, priority):
        node = llist(value, priority)
        here = self
        
        while (not (here.next == None) and here.next.priority < priority):
            here = here.next
        
        # insert after here
        node.next = here.next
        if (not (here.next == None)):
            here.next.prev = node
            
        here.next = node
        node.prev = here
        
    def is_empty(self):
        return (self.next == None)
        
    # This is why we use the dummy - we can then just moves the nodes in the list around without
    # needing to change the value of the first node after we remove the minimum element
    def pop_min(self):
        if (not self.next == None):
            # The best will always be the first
            node = self.next
            value = node.value
            
            # Remove
            self.next = node.next
            if (not node.next == None):
                node.next.prev = node.prev
                
            return value
        return None

    def print(self):
        sys.stdout.write("<%s,%d> followed by... \n" % (self.value, self.priority))
        if (not self.next == None):
            self.next.print()
        else:
            print("End of List\n")

    
