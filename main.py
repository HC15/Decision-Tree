import sys
from tree_builder import read_csv, build_tree


def main():
    # Get parameters from command line
    training = read_csv(sys.argv[1])
    validation = read_csv(sys.argv[2])
    test = read_csv(sys.argv[3])
    to_print = sys.argv[4]
    prune = sys.argv[5]

    # Loop for each heuristic
    heuristics = ["H1", "H2"]
    for heuristic in heuristics:
        decision_tree = build_tree(training, heuristic)  # Build decision tree

        # Print accuracy of each data set with no pruning
        print(heuristic, "NP Training", decision_tree.traverse(training))
        print(heuristic, "NP Validation", decision_tree.traverse(validation))
        print(heuristic, "NP Test", decision_tree.traverse(test))

        # Print tree if fourth parameter is "yes"
        if to_print == "yes":
            print()
            print(heuristic, "Decision Tree with No Pruning")
            decision_tree.print_tree()
            print()

        # Prune tree if fifth parameter is "yes"
        if prune == "yes":
            decision_tree.prune_tree(validation)  # Prune decision tree

            # Print accuracy of each data set with pruning
            print(heuristic, "P Training", decision_tree.traverse(training))
            print(heuristic, "P Validation", decision_tree.traverse(validation))
            print(heuristic, "P Test", decision_tree.traverse(test))

            # Prints tree again after pruning if fourth parameter is "yes"
            if to_print == "yes":
                print()
                print(heuristic, "Decision Trees with Pruning")
                decision_tree.print_tree()
                print()


if __name__ == "__main__":
    main()
