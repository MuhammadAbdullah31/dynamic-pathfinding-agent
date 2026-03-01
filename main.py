import pygame, random
from constants import *
from node import Node
from algorithms import search

pygame.init()
WIN = pygame.display.set_mode((WIN_WIDTH, WIN_HEIGHT))
pygame.display.set_caption("Dynamic Pathfinding Agent")


def make_grid():
    return [[Node(i, j, GAP, ROWS) for j in range(ROWS)] for i in range(ROWS)]


def draw_grid(win):
    for i in range(ROWS):
        pygame.draw.line(win, GREY, (0, i * GAP), (WIDTH, i * GAP))
        pygame.draw.line(win, GREY, (i * GAP, 0), (i * GAP, WIDTH))


def draw_dashboard(win, metrics, algo, heuristic, dynamic, status):
    font = pygame.font.SysFont("Arial", 18)
    pygame.draw.rect(win, LIGHT_GREY, (WIDTH, 0, DASHBOARD_WIDTH, WIN_HEIGHT))
    x = WIDTH + 10

    texts = [
        f"Algorithm: {algo}",
        f"Heuristic: {heuristic}",
        f"Dynamic Mode: {'ON' if dynamic else 'OFF'}",
    ]

    if metrics:
        texts += [
            f"Nodes Visited: {metrics['nodes_visited']}",
            f"Path Cost: {metrics['path_cost']}",
            f"Execution Time: {metrics['execution_time']} ms"
        ]

    texts.append(f"Status: {status}")

    for i, text in enumerate(texts):
        win.blit(font.render(text, True, BLACK), (x, 20 + i * 30))


def draw(win, grid, metrics, algo, heuristic, dynamic, status):
    win.fill(WHITE)
    for row in grid:
        for node in row:
            node.draw(win)
    draw_grid(win)
    draw_dashboard(win, metrics, algo, heuristic, dynamic, status)
    pygame.display.update()


def get_clicked_pos(pos):
    y, x = pos
    return y // GAP, x // GAP


def move_agent(draw_func, grid, start, goal, path, algo, heuristic, dynamic):
    for i, node in enumerate(path[::-1]):

        if node not in (start, goal):
            node.color = (255, 165, 0)

        draw_func()
        pygame.time.delay(100)

        if dynamic and random.random() < 0.2:
            r, c = random.randint(0, ROWS - 1), random.randint(0, ROWS - 1)
            obstacle = grid[r][c]

            if obstacle not in (node, start, goal):
                obstacle.color = BLACK
                remaining = path[::-1][i + 1:]

                if any(n.color == BLACK for n in remaining):
                    for row in grid:
                        for n in row:
                            n.update_neighbors(grid)

                    new_path, new_metrics = search(
                        draw_func, grid, node, goal,
                        algorithm=algo, heuristic=heuristic
                    )

                    if new_path:
                        return move_agent(draw_func, grid, node, goal,
                                          new_path, algo, heuristic, dynamic)
                    return False
    return True


def main():
    grid = make_grid()
    start = goal = metrics = None
    status = "Idle"
    algo, heuristic = "A*", "Manhattan"
    dynamic = False
    run = True

    while run:
        draw(WIN, grid, metrics, algo, heuristic, dynamic, status)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                r, c = get_clicked_pos(pygame.mouse.get_pos())
                if r < ROWS and c < ROWS:
                    node = grid[r][c]
                    if not start:
                        start, node.color = node, GREEN
                    elif not goal and node != start:
                        goal, node.color = node, BLUE
                    elif node not in (start, goal):
                        node.color = BLACK

            if pygame.mouse.get_pressed()[2]:
                r, c = get_clicked_pos(pygame.mouse.get_pos())
                if r < ROWS and c < ROWS:
                    node = grid[r][c]
                    node.color = WHITE
                    if node == start: start = None
                    if node == goal: goal = None

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE and start and goal:
                    status = "Searching..."
                    for row in grid:
                        for n in row:
                            n.update_neighbors(grid)

                    path, metrics = search(
                        lambda: draw(WIN, grid, None, algo, heuristic, dynamic, status),
                        grid, start, goal,
                        algorithm=algo, heuristic=heuristic
                    )

                    if path:
                        status = "Goal Reached"
                        if not move_agent(
                                lambda: draw(WIN, grid, metrics, algo, heuristic, dynamic, status),
                                grid, start, goal, path, algo, heuristic, dynamic):
                            status = "No Path Found"
                    else:
                        status = "No Path Found"

                elif event.key == pygame.K_a:
                    algo = "GBFS" if algo == "A*" else "A*"

                elif event.key == pygame.K_h:
                    heuristic = "Euclidean" if heuristic == "Manhattan" else "Manhattan"

                elif event.key == pygame.K_d:
                    dynamic = not dynamic

                elif event.key == pygame.K_r:
                    for row in grid:
                        for n in row:
                            if random.random() < 0.3 and n not in (start, goal):
                                n.color = BLACK

                elif event.key == pygame.K_c:
                    grid = make_grid()
                    start = goal = metrics = None
                    status = "Idle"

    pygame.quit()


if __name__ == "__main__":
    main()