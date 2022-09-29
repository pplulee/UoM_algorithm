import config

class bstree:
    def __init__(self):
        self.verbose = config.verbose
        
    def size(self):
        if (self.tree()):
            return 1 + self.left.size() + self.right.size()
        return 0
        
    def tree(self):
        # This counts as a tree if it has a field self.value
        # it should also have sub-trees self.left and self.right
        return hasattr(self, 'value')
        
    def insert(self, value):
        if (self.tree()):
            # TODO if tree is not NULL then insert into the correct sub-tree
            print("Placeholder - remove this print statement")
        else:
            # TODO otherwise create a new node containing the value
            print("Placeholder - remove this print statement")
        
    def find(self, value):
        if self.tree():
            # TODO complete the find function
            print("Placeholder - remove this print statement")
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
            
            
