"""
Lab07
Author: Morgan Lecrone
Class: CSCI 141

This program sorts items into boxes in three different ways.
"""
import operator
from dataclasses import dataclass
@dataclass
class box:
    """
    This is a dataclass that represents a box.

    Attributes:
        id (int): The ID of the box.
        capacity (float): The total capacity of the box.
        remaining (float): The remaining capacity of the box.
        items (list): The items in the box.
    """
    id: int
    capacity: float
    remaining: float
    items: list

@dataclass
class item:
    """
    This is a dataclass that represents an item.

    Attributes:
        name (str): The name of the item.
        weight (float): The weight of the item.
    """
    name: str
    weight: float

def read_file(file_name):
    """
    This function reads a file containing box capacities and items.

    :param file_name: The name of the file to read from.
    :return: A list of empty boxes and a list of items.
    """
    box_list = []
    items_list = []
    file = open("TestData-2/" + file_name)
    id = 0
    for capacity in file.readline().split(" "):
        id += 1
        box_list.append(box(id, float(capacity), float(capacity), []))
    for line in file:
        line = line.split(" ")
        items_list.append(item(line[0], float(line[1])))
    return box_list, items_list

def roomiest(box_list, items_list):
    """
    This function sorts the items into boxes starting with the box that currently has the most space.
    :param box_list: A list of empty boxes.
    :param items_list: A list of items.
    :return: A list of filled boxes and a list of leftover items.
    """
    leftovers = []
    items_list = sorted(items_list, key=operator.attrgetter("weight"), reverse=True)
    for item in items_list:
        box_list = sorted(box_list, key=operator.attrgetter("remaining"), reverse=True)
        box = box_list[0]
        if item.weight <= box.remaining:
            box.items.append(item)
            box.remaining -= item.weight
        else:
            leftovers.append(item)
    return box_list, leftovers

def tightest_fit(box_list, items_list):
    """
    This function sorts the items into boxes starting with the box that currently has the least possible space to fit
    the item.
    :param box_list: A list of empty boxes.
    :param items_list: A list of items.
    :return: A list of filled boxes and a list of leftover items.
    """
    leftovers = []
    items_list = sorted(items_list, key=operator.attrgetter("weight"), reverse=True)
    for item in items_list:
        box_list = sorted(box_list, key=operator.attrgetter("remaining"))
        in_box = False
        for box in box_list:
            if (item.weight <= box.remaining) and not in_box:
                box.items.append(item)
                box.remaining -= item.weight
                in_box = True
        if not in_box:
            leftovers.append(item)
    return box_list, leftovers

def one_box_at_a_time(box_list, items_list):
    """
    This function sorts the items into boxes one box at a time.
    :param box_list: A list of empty boxes.
    :param items_list: A list of items.
    :return: A list of filled boxes and a list of leftover items.
    """
    items_list = sorted(items_list, key = operator.attrgetter("weight"), reverse=True)
    for box in box_list:
        i = 0
        while i < len(items_list):
            if items_list[i].weight <= box.remaining:
                box.remaining -= items_list[i].weight
                box.items.append(items_list.pop(i))
            else:
                i += 1
    return box_list, items_list

def print_result(box_list, leftovers):
    """
    This function displays the list of boxes and their contents as well as any leftover items.
    :param box_list: A list of boxes.
    :param leftovers: A list of leftover items.
    """
    box_list = sorted(box_list, key=operator.attrgetter("id"))
    if len(leftovers) == 0:
        print("All items successfully packed into boxes!")
    else:
        print("Unable to pack all items!")
    for box in box_list:
        print("Box ", box.id, " of weight capacity ", box.capacity, " contains:")
        for item in box.items:
            print("\t" + item.name, " of weight ", item.weight)
    for item in leftovers:
        print(item.name, " of weight ", item.weight, " got left behind.")

def main():
    """
    This function reads box and item data from a file specified by the user.  Then, it employs three different
    strategies of sorting the items into boxes.  Finally, it displays the result of these three strategies.
    """
    file_name = input("Enter data file: ")
    box_list, items_list = read_file(file_name)
    box_list, leftovers = roomiest(box_list, items_list)
    print("\nResults from Greedy Strategy 1")
    print_result(box_list, leftovers)
    box_list, items_list = read_file(file_name)
    box_list, leftovers = tightest_fit(box_list, items_list)
    print("\nResults from Greedy Strategy 2")
    print_result(box_list, leftovers)
    box_list, items_list = read_file(file_name)
    box_list, leftovers = one_box_at_a_time(box_list, items_list)
    print("\nResults from Greedy Strategy 3")
    print_result(box_list, leftovers)

if __name__ == "__main__":
    main()