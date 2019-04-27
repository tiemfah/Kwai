from random import choice
from copy import deepcopy
import glob, os

map_pool_list = []

def file_to_array(file):
    temp = open(file, 'r').read().splitlines()
    table = [row.split(",") for row in temp]
    return table

for file in glob.glob("resource/mapping/*.csv"):
    map_pool_list.append(file_to_array(file))

def get_map():
    return deepcopy(choice(map_pool_list))

def add_map(map_list):
    for row in deepcopy(choice(map_pool_list)):
        map_list.append(row)