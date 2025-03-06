import pygame
import math
import heapq

WIDTH=800

WIN=pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Dijkstra's Algorithm")

RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 255, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165 ,0)
GREY = (128, 128, 128)
TURQUOISE = (64, 224, 208)

class Node:

    def __init__(self, row, col, width, total_rows):
        self.row=row
        self.col=col
        self.x=width*row
        self.y=width*col
        self.color=WHITE
        self.neighbours=[]
        self.width=width
        self.total_rows=total_rows

    def get_pos(self):
        return self.row,self.col

    def is_closed(self):
        return self.color==RED

    def is_open(self):
        return self.color==GREEN

    def is_barrier(self):
        return self.color==BLACK

    def is_start(self):
        return self.color==ORANGE

    def is_end(self):
        return self.color==TURQUOISE

    def reset(self):
        self.color=WHITE

    def make_closed(self):
        self.color=RED

    def make_open(self):
        self.color=GREEN

    def make_barrier(self):
        self.color=BLACK

    def make_start(self):
        self.color=ORANGE

    def make_end(self):
        self.color=TURQUOISE

    def make_path(self):
        self.color=PURPLE

    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))

    def update_neighbors(self, grid):
        """ Update neighbors considering barriers. """
        self.neighbors = []
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]  # Up, Down, Left, Right

        for dr, dc in directions:
            r, c = self.row + dr, self.col + dc
            if 0 <= r < self.total_rows and 0 <= c < self.total_rows:
                if not grid[r][c].is_barrier():
                    self.neighbors.append(grid[r][c])


    def __lt__(self, other):
        return False


def h(p1,p2):
    x1,y1=p1
    x2,y2=p2

def make_grid(rows,width):

    grid=[]
    gap=width//rows

    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node=Node(i,j,gap,rows)
            grid[i].append(node)

    return grid

def draw_grid(win,rows,width):

    gap=width//rows
    for i in range(rows):
        pygame.draw.line(win,GREY,(0,i*gap),(width,i*gap))
        for j in range(rows):
            pygame.draw.line(win,GREY,(j*gap,0),(j*gap,width))


def draw(win,grid,rows,width):

    win.fill(WHITE)

    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win,rows,width)
    pygame.display.update()


def get_clicked_pos(pos,rows,width):

    gap=width//rows
    x,y=pos

    row=x//gap
    col=y//gap

    return row,col


def reconstruct_path(came_from, current, draw):
    """ Reconstruct the path from end to start. """
    while current in came_from:
        current = came_from[current]
        current.make_path()
        draw()


def dijkstra(draw, grid, start, end):

    pq = []
    heapq.heappush(pq, (0, start))
    distances = {node: float("inf") for row in grid for node in row}
    distances[start] = 0
    came_from = {}

    while pq:
        current_distance, current_node = heapq.heappop(pq)

        if current_node == end:
            reconstruct_path(came_from, end, draw)
            end.make_end()
            return True

        for neighbor in current_node.neighbors:
            new_distance = current_distance + 1

            if new_distance < distances[neighbor]:
                distances[neighbor] = new_distance
                came_from[neighbor] = current_node
                heapq.heappush(pq, (new_distance, neighbor))
                neighbor.make_open()

        draw()

        if current_node != start:
            current_node.make_closed()

    return False


def main(win,width):

    ROWS=50
    grid=make_grid(ROWS,width)

    start=None
    end=None

    run=True
    started=False

    while run:
        draw(win,grid,ROWS,WIDTH)

        for event in pygame.event.get():

            if event.type==pygame.QUIT:
                run=False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_pos(pos,ROWS,width)
                node=grid[row][col]

                if not start and node!=start:
                    start=node
                    start.make_start()

                elif not end and node!=end:
                    end=node
                    end.make_end()

                elif node!=start and node!=end:
                    node.make_barrier()


            elif pygame.mouse.get_pressed()[2]:
                pos=pygame.mouse.get_pos()
                row,col=get_clicked_pos(pos,ROWS,width)
                node=grid[row][col]

                node.reset()

                if node==start:
                    start=None
                elif node==end:
                    end=None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    started = True
                    dijkstra(lambda: draw(win, grid, ROWS, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)


    pygame.quit()


main(WIN,WIDTH)