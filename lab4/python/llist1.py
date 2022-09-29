import sys

class llist:
    def __init__(self, value=None, priority=0):
        self.value = value
        self.priority = priority
        self.next = None
        self.prev = None
        
    def contains(self, value, priority):
        tmp_next = self.next
        while (not tmp_next == None):
            if ((tmp_next.value == value) and (tmp_next.priority == priority)):
                return True
            tmp_next = tmp_next.next
        
        return False
        
    def insert(self, value, priority):
        node = llist(value, priority)
        node.next = self.next
        if (not self.next == None):
            self.next.prev = node
        node.prev = self
        self.next = node
        
    def is_empty(self):
        # Assumes single dummy
        return (self.next == None)
        
    def pop_min(self):
        if (not self.next == None):
            best = sys.maxsize
            best_node = None
            next = self.next
            while (not next == None):
                if (next.priority < best):
                    best = next.priority
                    best_node = next
                next = next.next
            value = best_node.value
            
            # Remove best_node
            if (not best_node.prev == None):
                best_node.prev.next = best_node.next
            if (not best_node.next == None):
                best_node.next.prev = best_node.prev
                
            return value
            
        return None
        
    def print(self):
        sys.stdout.write("<%s,%d> followed by... \n" % (self.value, self.priority))
        if (not self.next == None):
            self.next.print()
        else:
            print("End of List\n")
        
