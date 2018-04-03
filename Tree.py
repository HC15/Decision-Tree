from collections import deque


class Tree:

    def __init__(self):
        self.root = None

    # Get internal nodes of Tree, used for pruning since you don't need to prune leaf nodes
    def get_internal_nodes(self):
        internal_nodes = []
        queue = deque([self.root])
        while len(queue) > 0:
            current_node = queue.pop()
            if current_node.zero is not None and current_node.one is not None:
                internal_nodes.append(current_node)
            if current_node.zero is not None:
                queue.append(current_node.zero)
            if current_node.one is not None:
                queue.append(current_node.one)
        return internal_nodes

    # Traverse the Tree using a data set and return how accurate the Tree is
    def traverse(self, data):
        if self.root is not None and len(data) > 0:
            correct = 0
            for example in data:
                if self.root.traverse_node(example) == example["Class"]:
                    correct += 1
            return correct / len(data)
        else:
            return 0.0

    # Print the Tree recursively
    def print_tree(self):
        if self.root is not None:
            self.root.print_node()

    # Prune the tree using validation data set
    def prune_tree(self, validation):
        prune = True
        while prune:  # Keep pruning if it can improve performance
            performance_current = self.traverse(validation)  # Performance of Tree on validation before pruning

            internal_nodes = self.get_internal_nodes()  # Get internal nodes to visit
            prune_best = internal_nodes[0]  # Used to store the best node to prune
            performance_best = 0.0  # Keep track of best prune so far
            while len(internal_nodes) > 0:  # Keep testing pruning until all nodes are used
                prune_current = internal_nodes.pop()  # Pop from internal nodes because lower depth
                attribute_temp = prune_current.attribute  # Store attribute to restore later
                zero_temp = prune_current.zero  # Store zero of node to restore later
                one_temp = prune_current.one  # Store one of node to restore later

                prune_current.attribute = prune_current.most_common_class()  # Make Node its most common class
                prune_current.zero = None  # Make pruned node a leaf
                prune_current.one = None  # Make pruned node a leaf
                performance_new = self.traverse(validation)  # Test performance after prune

                # Restore test pruned node to original state
                prune_current.attribute = attribute_temp
                prune_current.zero = zero_temp
                prune_current.one = one_temp
                # If test performance is better then previous best, make it new candidate to be pruned
                if performance_new > performance_best:
                    prune_best = prune_current
                    performance_best = performance_new

            # Check if performance of tree improves, if it doesn't then stop pruning
            if performance_best > performance_current:
                # Prune Node if makes a difference by setting it to most common class and making it a leaf
                prune_best.attribute = prune_best.most_common_class()
                prune_best.zero = None
                prune_best.one = None
            else:
                prune = False
