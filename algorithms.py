import pygame
import math
import time
from queue import PriorityQueue

def h_manhattan(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def h_euclidean(p1, p2):
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def reconstruct_path(came_from, current, draw):
    path = []
    while current in came_from:
        path.append(current)
        current = came_from[current]
        if current.color != (0,255,0): current.color = (128,0,128)
        draw()
    return path

def search(draw, grid, start, goal, algorithm="A*", heuristic="Manhattan"):
    start_time, count, nodes_visited = time.time(), 0, 0
    open_set = PriorityQueue(); open_set.put((0, count, start))
    came_from = {}
    g_score = {node: float("inf") for row in grid for node in row}; g_score[start] = 0
    h_func = h_manhattan if heuristic=="Manhattan" else h_euclidean
    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit()

        current = open_set.get()[2]; open_set_hash.remove(current); nodes_visited += 1

        if current == goal:
            path = reconstruct_path(came_from, goal, draw)
            return path, {"nodes_visited": nodes_visited, "path_cost": len(path), 
                          "execution_time": round((time.time()-start_time)*1000,2)}

        for neighbor in current.neighbors:
            temp_g = g_score[current] + 1
            if temp_g < g_score[neighbor]:
                came_from[neighbor] = current; g_score[neighbor] = temp_g
                priority = temp_g + h_func(neighbor.get_pos(), goal.get_pos()) if algorithm=="A*" else h_func(neighbor.get_pos(), goal.get_pos())
                if neighbor not in open_set_hash:
                    count += 1; open_set.put((priority,count,neighbor)); open_set_hash.add(neighbor)
                    if neighbor != goal: neighbor.color = (255,255,0)

        draw()
        if current != start: current.color = (255,0,0)

    return None, None