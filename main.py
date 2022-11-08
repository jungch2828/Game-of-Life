import pygame
from random import choice

pygame.init()

WHITE = (255,255,255)
BLACK = (0,0,0)
GRAY = (127,127,127)
CLOCK = pygame.time.Clock()

block_size = 15
block_per_width = 75
block_per_height = 50
screen_width = block_size * block_per_width
screen_height = block_size * block_per_height
line_width = int(block_size/10)
line_color = GRAY
block_color = WHITE
board_running = False
tick_running = 20
tick = 60
generation = 0
show_generation = True
font = pygame.font.SysFont(None,block_size*2)

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Game of Life')

class Cell:

    def __init__(self,row,col,state=0,state_next=0):
        self.row = row
        self.col = col
        self.state = state
        self.state_next = state_next

    def func(self):
        cnt = 0
        for r,c in [[1,1],[1,0],[1,-1],[0,1],[0,-1],[-1,1],[-1,0],[-1,-1]]:
            if 0 <= self.row+r <= block_per_height-1 and 0 <= self.col+c <= block_per_width-1:
                if board[self.row+r][self.col+c].state == 1:
                    cnt += 1

        if self.state == 0:
            if cnt == 3:
                self.state_next = 1
            else:
                self.state_next = 0
        else:
            if cnt >= 4 or cnt <= 1:
                self.state_next = 0
            else:
                self.state_next = 1
    
    def draw(self):
        pygame.draw.rect(screen,block_color,((block_size*self.col,block_size*self.row),(block_size,block_size)))

def draw_grid():
    for x in range(block_size,screen_width,block_size):
        pygame.draw.line(screen,line_color,(x,0),(x,screen_height),line_width)
    for y in range(block_size,screen_width,block_size):
        pygame.draw.line(screen,line_color,(0,y),(screen_width,y),line_width)

board = []
for row in range(block_per_height):
    board.append([])
    for col in range(block_per_width):
        board[row].append(Cell(row,col))

while True:
    for event in pygame.event.get(): 
        if event.type == pygame.QUIT: #close display
            pygame.quit()
        if event.type == pygame.KEYDOWN: #keyboard event
            if event.key == pygame.K_SPACE: #start/stop
                board_running = not board_running
            if event.key == pygame.K_c: #clear board
                for row in range(block_per_height):
                    for col in range(block_per_width):
                        board[row][col].state = 0
            if event.key == pygame.K_r: #random generate
                for row in range(block_per_height):
                    for col in range(block_per_width):
                        board[row][col].state = choice((0,1))
            if event.key == pygame.K_g: #show/hide generation
                show_generation = not show_generation
            if event.key == pygame.K_i: #initialize generation
                generation = 0
            if event.key == pygame.K_UP: #increase running speed
                if tick_running < 40:
                    tick_running *= 1.1
            if event.key == pygame.K_DOWN: #increase running speed down
                if tick_running > 1:
                    tick_running *= 0.9
        if event.type == pygame.MOUSEBUTTONDOWN: #mouse event
            if not board_running:
                mouse_row = pygame.mouse.get_pos()[1]//block_size
                mouse_col = pygame.mouse.get_pos()[0]//block_size
                board[mouse_row][mouse_col].state = not board[mouse_row][mouse_col].state

    mouse_row = pygame.mouse.get_pos()[1]//block_size
    mouse_col = pygame.mouse.get_pos()[0]//block_size

    screen.fill(BLACK)

    if board_running:
        generation += 1
        tick = tick_running
        line_color = BLACK
        for row in range(block_per_height):
            for col in range(block_per_width):
                board[row][col].func()
        for row in range(block_per_height):
            for col in range(block_per_width):
                board[row][col].state = board[row][col].state_next
    else:
        tick = 60
        line_color = GRAY

    for row in range(block_per_height):
        for col in range(block_per_width):
            if board[row][col].state == 1:
                board[row][col].draw()

    draw_grid()

    text = font.render(str(generation),True,(200,200,200))
    text_width = text.get_rect()[2]
    if show_generation:
        screen.blit(text,(screen_width-text_width-5,5))

    pygame.display.flip()
    CLOCK.tick(tick)
