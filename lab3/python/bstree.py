import config


class bstree:
    def __init__(self):
        self.verbose = config.verbose
        self.insert_count = 0
        self.find_count = 0

    def size(self):
        return 0 if not self.tree() else 1 + self.left.size() + self.right.size()

    def tree(self):
        # This counts as a tree if it has a field self.value
        # it should also have sub-trees self.left and self.right
        return hasattr(self, 'value')

    def insert(self, value):
        self.insert_count += 1
        if self.tree():
            # if tree is not NULL then insert into the correct sub-tree
            if value < self.value:
                return self.left.insert(value)
            elif value > self.value:
                return self.right.insert(value)
            else:
                # already exist
                return True
        else:
            # otherwise create a new node containing the value
            self.value = value
            self.left = bstree()
            self.right = bstree()
            return True

    def find(self, value):
        self.find_count += 1
        if self.tree():
            if value == self.value:
                return True
            elif value < self.value:
                return self.left.find(value)
            else:
                return self.right.find(value)
        return False

    # You can update this if you want
    def print_set_recursive(self, depth):
        if self.tree():
            for i in range(depth):
                print(" ", end='')
            print("%s" % self.value)
            self.left.print_set_recursive(depth + 1)
            self.right.print_set_recursive(depth + 1)

    # You can update this if you want
    def print_set(self):
        print("Tree:\n")
        self.print_set_recursive(0)

    def height(self):
        return 1 + max(self.left.height(), self.right.height()) if self.tree() else 0

    def get_insert_stats(self):
        if self.tree():
            return self.insert_count + self.left.get_insert_stats() + self.right.get_insert_stats()
        else:
            return self.insert_count

    def get_find_stats(self):
        if self.tree():
            return self.find_count + self.left.get_find_stats() + self.right.get_find_stats()
        else:
            return self.find_count

    def print_stats(self):
        print("Height:", self.height())
        print("Size:", self.size())
        print("Inserts:", self.get_insert_stats())
        print("Finds:", self.get_find_stats())
