import sys
import csv
import math
import random
from Tree import Tree
from Node import Node


# Take path of csv file and return a list of dictionaries for each line
def read_csv(file_name):
    with open(file_name) as file_csv:
        reader = csv.DictReader(file_csv)
        return list(reader)


# Count attributes in data, index 0 is how many '0' and index 1 is how many '1'
def count_attribute(data, attribute):
    counter = [0, 0]
    for example in data:
        if example.get(attribute) == '0':
            counter[0] += 1
        elif example.get(attribute) == '1':
            counter[1] += 1
    return counter


# Split data into two list, index 0 is data with attribute having '0' and index 1 is data with attribute '1'
def split_data(data, attribute):
    data_split = [[], []]
    for example in data:
        if example.get(attribute) == '0':
            data_split[0].append(example)
        elif example.get(attribute) == '1':
            data_split[1].append(example)
    return data_split


# Calculate the entropy for H1
def entropy_impurity(counter, data_size):
    entropy = 0.0
    if data_size > 0:
        for i in range(2):
            probability = counter[i] / data_size
            if probability > 0:  # log(0) is undefined so first check
                entropy += (-1 * probability * math.log2(probability))
    return entropy


# Calculate the variance impurity for H2
def variance_impurity(counter, data_size):
    impurity = 1.0
    if data_size > 0:
        for i in range(2):
            impurity *= (counter[i] / data_size)
    return impurity


# Calculate gain depending on inputted heuristic
def information_gain(data, attribute, heuristic):
    count_class = count_attribute(data, "Class")

    gain = 0.0
    if heuristic == "H1":
        gain = entropy_impurity(count_class, len(data))
    elif heuristic == "H2":
        gain = variance_impurity(count_class, len(data))

    data_split = split_data(data, attribute)
    for i in range(2):
        if len(data_split[i]) != 0:
            if heuristic == "H1":
                gain -= ((len(data_split[i]) / len(data)) *
                         entropy_impurity(count_attribute(data_split[i], "Class"), len(data_split[i])))
            elif heuristic == "H2":
                gain -= ((len(data_split[i]) / len(data)) *
                         variance_impurity(count_attribute(data_split[i], "Class"), len(data_split[i])))
    return gain


# Build the Tree, return the Tree object after setting the root
def build_tree(data, heuristic):
    attributes = []
    for key in data[0].keys():
        if key != "Class":
            attributes.append(key)
    tree = Tree()
    tree.root = grow_tree(data, attributes, heuristic, 0)
    return tree


# Recursive function to make new Nodes for decision tree
def grow_tree(data, attributes, heuristic, depth):
    count_class = count_attribute(data, "Class")
    for i in range(2):
        if count_class[i] == len(data):  # Check if data only has one class to make a general Node classification
            return Node(str(i), False, depth)

    if len(attributes) == 0:  # If no more attributes, choose the most common class left in data
        if count_class[0] > count_class[1]:
            return Node('0', False, depth)
        elif count_class[0] < count_class[1]:
            return Node('1', False, depth)
        else:  # If equal count of both class, just guess one
            return Node(str(random.randint(0, 2)), True, depth)

    # Calculate which attribute has the highest information gain
    gain_highest = -sys.maxsize  # Lowest possible value, something will always be greater
    attribute_best = ""  # Keep trade of best attribute to split on
    for attribute in attributes:  # Iterate through all the attributes left
        gain = information_gain(data, attribute, heuristic)  # Calculate information gain based on which heuristic
        if gain > gain_highest:  # If new highest gain, there is a new best attribute to split on
            gain_highest = gain  # Update best gain
            attribute_best = attribute # Update attribute

    node_new = Node(attribute_best, False, depth)  # Make a new Node based on the best attribute
    attributes_new = []  # Update the new list of attributes
    for attribute in attributes:
        if attribute != attribute_best:  # Make sure the best attribute isn't in the new list
            attributes_new.append(attribute)

    data_split = split_data(data, attribute_best)  # Split the data to for creation of new nodes
    # Create a node when when attribute is equal to 0
    if len(data_split[0]) != 0:  # Check if there is any data before making the new node
        node_new.zero = grow_tree(data_split[0], attributes_new, heuristic, depth + 1)
    else:  # If there is no data, guess a classification so the Tree doesn't have any dead ends
        node_new.zero = Node(str(random.randint(0, 1)), True, depth + 1)

    # Create a node when attribute is equal to 1
    if len(data_split[1]) != 0:  # Check if there is any data before making the new node
        node_new.one = grow_tree(data_split[1], attributes_new, heuristic, depth + 1)
    else:  # If there is no data, guess a classification so the Tree doesn't have any dead ends
        node_new.one = Node(str(random.randint(0, 1)), True, depth + 1)

    return node_new  # Return the newly created node, in build_tree this will be the root
