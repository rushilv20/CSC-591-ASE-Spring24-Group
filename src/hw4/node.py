class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None

    def walk(self, fun, depth=0):
        fun(self, depth, not (self.left or self.right))
        if self.left:
            self.left.walk(fun, depth + 1)
        if self.right:
            self.right.walk(fun, depth + 1)

    def show(self, show_func, max_depth):
        def data_to_hex(data):
            return round(data.mid().data_to_hex(self.data), ndigits=6)

        max_depth = 0

        def show_node(node, depth, is_leaf, post):
            nonlocal max_depth
            post = post if is_leaf else f"{data_to_hex(node.data)}\t{node.data.mid().cells}"
            max_depth = max(max_depth, depth)
            print(('|.. ' * depth) + post)

        self.walk(show_node)
        print("")
        print(("    " * max_depth) + f"{data_to_hex(self.data)}\t{self.data.mid().cells}")
        print(("    " * max_depth) + "_\t" + str(self.data.cols.names))
