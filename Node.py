from collections import deque


class Node:

    def __init__(self, attribute, guess, depth):
        self.attribute = attribute
        self.guess = guess
        self.depth = depth
        self.zero = None
        self.one = None

    # Count class (attribute of its leafs) of the node and returns the most common one
    def most_common_class(self):
        count_class = [0, 0]
        queue = deque([self])
        while len(queue) > 0:
            current_node = queue.pop()
            if current_node.zero is None and current_node.one is None:
                if current_node.attribute == '0' and not current_node.guess:
                    count_class[0] += 1
                elif current_node.attribute == '1' and not current_node.guess:
                    count_class[1] += 1
            if current_node.zero is not None:
                queue.append(current_node.zero)
            if current_node.one is not None:
                queue.append(current_node.one)

        if count_class[0] >= count_class[1]:
            return '0'
        else:
            return '1'

    # Traverse the node using the example
    def traverse_node(self, example):
        if self.zero is None and self.one is None:
            return self.attribute
        else:
            if example[self.attribute] == '0':
                if self.zero is not None:
                    return self.zero.traverse_node(example)
            elif example[self.attribute] == '1':
                if self.one is not None:
                    return self.one.traverse_node(example)

    # Print edges so Tree looks correct when printing
    def print_edges(self):
        for edge in range(self.depth):
            print("| ", end='')

    # Print the information of node
    def print_node(self):
        if self.zero is None and self.one is None:
            print(' ' + self.attribute)  # If node is a leaf, then it means it contains the class
        else:
            print()

            if self.zero is not None:
                self.print_edges()
                print(self.attribute + " = 0 :", end='')  # If the node zero has something print current
                self.zero.print_node()  # Visit zero

            if self.one is not None:
                self.print_edges()
                print(self.attribute + " = 1 :", end='')  # If the node's one has something print current
                self.one.print_node()  # Visit one
