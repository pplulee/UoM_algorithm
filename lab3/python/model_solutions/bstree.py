class bstree:
    def __init__(self):
        pass
        
    def size(self):
        if (self.tree()):
            return 1 + self.left.size() + self.right.size()
        return 0
        
    def tree(self):
        return hasattr(self, 'value')
        
    def insert(self, value):
        if (self.tree()):
            if(value < self.value):
                self.left.insert(value)
            elif (value > self.value):
                self.right.insert(value)
        else:
            self.left = bstree();
            self.right = bstree();
            self.value = value;
        
    def find(self, value):
        if self.tree():
            if (value == self.value):
                return True
            elif (value < self.value):
                return self.left.find(value)
            else:
                return self.right.find(value)
        return False
        
    # You can update this if you want
    def print_set_recursive(self, depth):
        if (self.tree()):
            for i in range(depth):
                print(" ", end='')
            print("%s" % self.value)
            self.left.print_set_recursive(depth + 1)
            self.right.print_set_recursive(depth + 1)
            
    # You can update this if you want
    def print_set(self):
        print("Tree:\n")
        self.print_set_recursive(0)
        
    def print_stats(self):
        # TODO update code to record and print statistic
        print("Placeholder - remove this print statement")
            
            
