import sys

# Set CHECK_HB here to check whether the Height-Balance property holds.  This slows things down a lot
CHECK_HB = False


def max(a, b):
    if (a > b):
        return a
    return b
    
def height(tree):
    if (not tree == None):
        return tree.depth
        
    return 0
    
def insert_inner(tree, value, priority):
    if (not tree == None):
        if (tree.priority > priority):
            tree.left = insert_inner(tree.left,value,priority)
        else:
            tree.right = insert_inner(tree.right,value,priority)
            
        tree.depth = max(height(tree.left), height(tree.right)) + 1
        tree.rebalance()
    else:
        # Otherwise create a new node containing the value
        tree = avltree()
        tree.value = value
        tree.priority = priority
        
    return tree

# Observe that the minimum node cannot have a left sub-child
# Therefore, deleting it is comaratively straightforward e.g.
# we do not need to choose which subtree to lift
def pop_min_inner(tree, parent):
    if (not tree == None):
        res = None
        if (not tree.left == None):
            res = pop_min_inner(tree.left, tree)
            tree.depth = max(height(tree.left), height(tree.right)) + 1
            tree.rebalance()
            parent.left = tree
        # Min node (base case for recursion)
        else:
            res = tree.value
            if (not tree.right == None):
                parent.left = tree.right
            else:
                parent.left = None
        return res
    sys.stderr.write("Tried to pop from empty AVL tree\n")
    sys.exit(-1)
    return None

        
class avltree:
    def __init__(self, priority=0, value=None, left=None, right=None, depth=1):
        # An empty tree is represented by a node with NONE value.  Cannot insert None into tree.
        # We only use the left subtree of the sentinel
        self.value = value
        self.left = left
        self.right = right
        self.depth = depth
        self.priority = priority
        
    def actualHeight(self):
        if ((not self.left == None) and (not self.right == None)):
            return 1 + max(left.actualHeight(), right.actualHeight)
        else:
            return 0
            
    def hasHeightBalanceProperty(self):
        if ((not self.left == None) and self.value == None):
            return self.left.hasHeightBalanceProperty()
        
        if ((not self.left == None) and (not self.right == None)):
            left = self.left.actualHeight()
            right = self.right.actualHeight()
            difference = left - right
            if (difference < 0):
                difference = -difference
            return ((difference <= 1) and self.left.hasHeightBalanceProperty() and self.right.hasHeightBalanceProperty())
            
        return True
        
    def checkHeightBalanceProperty(self):
        if (CHECK_HB):
            if (not self.hasHeightBalanceProperty()):
                sys.stderr.write("HeightBalanceProperty violated\n")
                sys.exit(-1)
                
    def sentinel(self):
        return self.value == None
        
    def is_empty(self):
        if (self.sentinel()):
            return self.left == None
        
        return self.left == None and self.right == None
        
    def copy(self):
        if (not (self.left == None) and not (self.right == None)):
            return avltree(self.priority, self.value, self.left.copy(), self.right.copy(), self.depth)
        elif (not self.left == None):
            return avltree(self.priority, self.value, self.left.copy(), self.right, self.depth)
        elif (not self.right == None):
            return avltree(self.priority, self.value, self.left, self.right.copy(), self.depth)
        else:
            return avltree(self.priority, self.value, self.left, self.right, self.depth)
        
    def shallow_copy(self):
        return avltree(self.priority, self.value, self.left, self.right, self.depth)

    def rightRotate(self):
        l = self.left
        if (not l.right == None):
            self.left = l.right
        else:
            self.left = None
        l.right = self.shallow_copy()
        
        self.depth = max(height(self.left), height(self.right)) + 1
        l.depth = max(height(l.left), self.depth) + 1
        
        self.value = l.value
        self.priority = l.priority
        self.left = l.left
        self.right = l.right
        self.depth = l.depth
        # self.print()
        
        
    def leftRotate(self):
        r = self.right
        if (not r.left == None):
            self.right = r.left
        else:
            self.right = None
        r.left = self.shallow_copy()
        
        self.depth = max(height(self.left), height(self.right)) + 1
        r.depth = max(height(r.right), self.depth) + 1
        
        self.value = r.value
        self.priority = r.priority
        self.left = r.left
        self.right = r.right
        self.depth = r.depth
 
    def getBalance(self):
        if (self.left == None and self.right == None):
            return 0
            
        balance = height(self.right) - height(self.left)
        return balance
        
    def rebalance(self):
        parentBalance = self.getBalance()
        
        if (parentBalance == -2): # left child update
            if (self.left.getBalance() <= 0):
                # print("Case Right")
                self.rightRotate()
            else:
                # print("Case RightLeft")
                self.left.leftRotate()
                self.rightRotate()
                
        if (parentBalance == 2): # right child update
            if (self.right.getBalance() >= 0):
                # print("Case Left")
                return self.leftRotate()
            else:
                # print ("Case LeftRight")
                self.right.rightRotate()
                self.leftRotate()
            
        # print("No change")
        
    def insert(self, value, priority):
        if (value == None):
            sys.stderr.write("Cannot insert None into tree, ignoring...\n")
            return
            
        if (self.sentinel()):
            # sentinel case
            self.left = insert_inner(self.left,value,priority)
            self.checkHeightBalanceProperty()
            # self.print()
            return
            
        sys.stderr.write("Tree is corrupted\n")
        sys.exit(-1)
        return
        
    def contains(self, value, priority):
        if (self.sentinel() and (not self.left == None)):
            return self.left.contains(value, priority)
        else:
            if (self.priority == priority):
                # if we have the right priority and right value return true
                if (value == self.value):
                    return True
                # if we have the right priority but wrong value then one of the children
                # might have the same priority and, if so, we should search there.  We
                # cannot make assumptions about which child
                return (( (not self.left == None) and (self.left.priority == priority) and self.left.contains(value, priority)) or ((not self.right == None) and (self.right.priority == priority) and self.right.contains(value, priority)))
            if (priority < self.priority and not (self.left == None)):
                return self.left.contains(value, priority)
            elif (not self.right == None):
                return self.right.contains(value, priority)
        # Should not get here
        return False
        
    def pop_min(self):
        if (self.sentinel()):
            res = pop_min_inner(self.left, self)
            self.checkHeightBalanceProperty()
            return res
        sys.stderr.write("The tree is corrupted\n")
        sys.exit(-1)
        return None
        
    # You can update this if you want
    def print_recursive(self, depth):
        for i in range(depth):
            sys.stdout.write(" ")
        sys.stdout.write("(%s,%d,%d)\n" % (self.value, self.priority, self.depth))
        if (not self.left == None):
            self.left.print_recursive(depth + 1)
        else:
            for i in range(depth + 1):
                sys.stdout.write(" ")
            print("(NULL,-,0)")
        if (not self.right == None):
            self.right.print_recursive(depth + 1)
        else:
            for i in range(depth + 1):
                sys.stdout.write(" ")
            print("(NULL,-,0)")
        
     # You can update this if you want
    def print(self):
        print("Tree:")
        if (self.sentinel()):
            if (not self.left == None):
                self.left.print_recursive(0)
            else:
                print("Sentinal has no left")
        else:
            self.print_recursive(0)

    
