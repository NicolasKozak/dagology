__author__ = "\n".join(["Nicolas Kozak (nicolas.kozak5@gmail.com)"])

import random
from math import atan

def shortest_path(node, weights, distances, predecessors):
    for v, w in weights.items():
        new_distance = distances[node] + w
        if distances[v] > new_distance:
            distances[v], predecessors[v] = new_distance, node


def longest_path(node, weights, distances, predecessors):
    for v, w in weights.items():
        new_distance = distances[node] - w
        if distances[v] > new_distance:
            distances[v], predecessors[v] = new_distance, node

def greedy_shortest_path(node, weights, distances, predecessors):
    if weights:
        min_neighbor = min(weights, key=weights.get)
        new_distance = distances[node] + weights[min_neighbor]
        if distances[min_neighbor] > new_distance:
            distances[min_neighbor] = new_distance
            predecessors[min_neighbor] = node

def greedy_longest_path(node, weights, distances, predecessors):
    if weights:
        max_neighbor = max(weights, key=weights.get)
        new_distance = distances[node] - weights[max_neighbor]
        if distances[max_neighbor] > new_distance:
            distances[max_neighbor] = new_distance
            predecessors[max_neighbor] = node
            
def random_path(node, weights, distances, predecessors):
    if weights:
        successors = list(weights.keys())
        random_successor = random.choice(successors)
        new_distance = distances[node] + weights[random_successor]
        if distances[random_successor] > new_distance:
            distances[random_successor] = new_distance
            predecessors[random_successor] = node
    

# Calculations

def get_angles_relative_to_geodesic(coordinates, weights):
    angles = {}
    for u, v in weights.keys():
        t1, x1 = coordinates[u]
        t2, x2 = coordinates[v]
        sign = 1.0 if x1 == 0.5 or (x1 < 0.5) ^ (x2 > x1) else -1.0
        angles[(u, v)] = sign * atan(abs(x2 - x1) / (t2 - t1))
    return angles