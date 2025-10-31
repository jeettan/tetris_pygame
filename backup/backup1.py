import pygame
import random

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((500,600))

pygame.display.set_caption("Tetris!")

BLOCK_SIZE = 30
GAME_BOARD_STARTING_POSITION_X = 60
GAME_BOARD_STARTING_POSITION_Y = 70
GAME_BOARD_HEIGHT = 15
GAME_BOARD_WIDTH = 10
GAME_SPEED = 300

CURRENT_POINT = 0

TIMER_EVENT = pygame.USEREVENT + 1
pygame.time.set_timer(TIMER_EVENT, GAME_SPEED)

text_font = pygame.font.SysFont('Arial', 25)
img = text_font.render("Next", True, (255,255,255))
point_text = text_font.render("Point", True, (255,255,255))

GRAY = (211,211,211)
ORANGE = (255,165,0)
BLUE = (0,153,153)
LIGHT_BLUE = (102,255,255)
YELLOW = (255,255,0)
PURPLE = (186,85,211)
GREEN = (170, 255, 0)
RED = (253, 63, 89)

clock = pygame.time.Clock()

class createTetrisBlock(object):

    def __init__(self):
 
        blocks = {"J": {"w": 3, "h": 2}, "I": {"w": 4, "h": 1}, "L": {"w": 3, "h": 2}, "O": {"w": 2, "h": 2}, "T": {"w":3, "h": 2}, "S": {"w": 3, "h": 2}, "Z": {"w": 3, "h": 2}}

        keys = list(blocks)
        current_block = random.choice(keys)

        self.x = 4
        self.y = 0
        self.width = blocks[current_block]['w']
        self.height = blocks[current_block]['h']
        self.block = current_block

    def draw(self):
        screen.fill('black')
        if(self.block == "J"):
            draw_tetris_block_J(self.x, self.y, GAME_BOARD_STARTING_POSITION_X, GAME_BOARD_STARTING_POSITION_Y)
        elif(self.block == "I"):
            draw_tetris_block_I(self.x, self.y, GAME_BOARD_STARTING_POSITION_X, GAME_BOARD_STARTING_POSITION_Y)
        elif(self.block == "L"):
            draw_tetris_block_L(self.x,self.y, GAME_BOARD_STARTING_POSITION_X, GAME_BOARD_STARTING_POSITION_Y)
        elif(self.block == "O"):
            draw_tetris_block_O(self.x,self.y, GAME_BOARD_STARTING_POSITION_X, GAME_BOARD_STARTING_POSITION_Y)
        elif(self.block == "T"):
            draw_tetris_block_T(self.x,self.y, GAME_BOARD_STARTING_POSITION_X, GAME_BOARD_STARTING_POSITION_Y)
        elif(self.block == "S"):
            draw_tetris_block_S(self.x,self.y, GAME_BOARD_STARTING_POSITION_X, GAME_BOARD_STARTING_POSITION_Y)
        elif(self.block == "Z"):
            draw_tetris_block_Z(self.x,self.y, GAME_BOARD_STARTING_POSITION_X, GAME_BOARD_STARTING_POSITION_Y)

    def display(self):

        display_x = 260
        display_y = 110

        if(self.block == "J"):
            draw_tetris_block_J(self.x, self.y, display_x, display_y)
        elif(self.block == "I"):
            draw_tetris_block_I(self.x, self.y, display_x, display_y)
        elif(self.block == "L"):
            draw_tetris_block_L(self.x,self.y, display_x,display_y)
        elif(self.block == "O"):
            draw_tetris_block_O(self.x,self.y, display_x, display_y)
        elif(self.block == "T"):
            draw_tetris_block_T(self.x,self.y, display_x, display_y)
        elif(self.block == "S"):
            draw_tetris_block_S(self.x,self.y, display_x, display_y)
        elif(self.block == "Z"):
            draw_tetris_block_Z(self.x,self.y, display_x, display_y)

class LandedBlocks(object):

    block_shape = {"J": [['J',0,0],['J','J','J']], "I": [['I','I','I','I']], "L": [[0,0,'L'], ['L','L','L']], "O": [['O','O'], ['O','O']], "T": [[0,'T',0],['T','T','T']], "S": [[0, 'S', 'S'], ['S','S',0]], "Z": [['Z','Z',0],[0,'Z','Z']]}

    def __init__(self):        

        self.blocks = [ [0]*10 for i in range(15)]

    def updateLandedBlocks(self, x_index, y_index, block_name):

        for iy, y_value in enumerate(self.block_shape[block_name]):
            for ix, x_value in enumerate(y_value):
                if(x_value == 0):
                    continue
                self.blocks[y_index + iy][x_index + ix] = x_value

    def draw_landed_blocks(self):

        for iy, y_value in enumerate(self.blocks):
            for ix, x_value in enumerate(y_value):
                if self.blocks[iy][ix] != 0:

                    color_code = {"J": BLUE, "I": LIGHT_BLUE, "L": ORANGE, "O": YELLOW, "T": PURPLE, "S": GREEN, "Z": RED}

                    current_color = color_code[x_value]

                    block_position_x = (ix * BLOCK_SIZE) + GAME_BOARD_STARTING_POSITION_X
                    block_position_y = (iy * BLOCK_SIZE) + GAME_BOARD_STARTING_POSITION_Y
                    draw_game_board()
                    pygame.draw.rect(screen, current_color, pygame.Rect(block_position_x, block_position_y, BLOCK_SIZE, BLOCK_SIZE))
            
currentBlock = createTetrisBlock()
nextBlock = createTetrisBlock()
CurrentLandedBlocks = LandedBlocks()

def set_game_over():

    global game_over
    game_over = True
    text_font = pygame.font.SysFont('Arial', 40)
    img = text_font.render("GAME OVER", True, (255,0,0))
    screen.blit(img, (120,280))

def check_row_clear():

    global CURRENT_POINT

    upgrade = pygame.mixer.Sound("sounds/upgrade.mp3")

    for index,row in enumerate(reversed(CurrentLandedBlocks.blocks)):
        clearRow = False
        for item in row:
           clearRow = True
           if(item == 0):
               clearRow = False
               break
        
        if(clearRow == True):
            upgrade.play()
            CURRENT_POINT += 40
            onBoardIndex = GAME_BOARD_HEIGHT - index - 1

            for numb in range(onBoardIndex, 0, -1):
                for index2,item in enumerate(CurrentLandedBlocks.blocks[onBoardIndex]):
                    temp = CurrentLandedBlocks.blocks[numb -1][index2] 
                    CurrentLandedBlocks.blocks[numb -1][index2] = 0
                    CurrentLandedBlocks.blocks[numb][index2] = temp

def draw_game_board():
    for i in range(GAME_BOARD_HEIGHT):
        for j in range(GAME_BOARD_WIDTH):
            pygame.draw.rect(screen, GRAY, pygame.Rect(GAME_BOARD_STARTING_POSITION_X + (j *BLOCK_SIZE), GAME_BOARD_STARTING_POSITION_Y + (i*BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE), 1)

def draw_tetris_block_J(current_x, current_y, STARTING_X, STARTING_Y):

    block_position_x = (current_x * BLOCK_SIZE) + STARTING_X
    block_position_y = (current_y * BLOCK_SIZE) + STARTING_Y

    pygame.draw.rect(screen, BLUE, pygame.Rect(block_position_x, block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, BLUE, pygame.Rect(block_position_x, block_position_y + 30, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, BLUE, pygame.Rect(block_position_x + 30, block_position_y + 30, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, BLUE, pygame.Rect(block_position_x + 60, block_position_y + 30, BLOCK_SIZE, BLOCK_SIZE))

def draw_tetris_block_I(current_x, current_y, STARTING_X, STARTING_Y):

    block_position_x = (current_x * BLOCK_SIZE) + STARTING_X
    block_position_y = (current_y * BLOCK_SIZE) + STARTING_Y

    pygame.draw.rect(screen, LIGHT_BLUE, pygame.Rect(block_position_x, block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, LIGHT_BLUE, pygame.Rect(block_position_x + BLOCK_SIZE, block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, LIGHT_BLUE, pygame.Rect(block_position_x + (BLOCK_SIZE * 2), block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, LIGHT_BLUE, pygame.Rect(block_position_x + (BLOCK_SIZE * 3), block_position_y, BLOCK_SIZE, BLOCK_SIZE))

def draw_tetris_block_L(current_x, current_y, STARTING_X, STARTING_Y):

    block_position_x = (current_x * BLOCK_SIZE) + STARTING_X
    block_position_y = (current_y * BLOCK_SIZE) + STARTING_Y

    pygame.draw.rect(screen, ORANGE, pygame.Rect(block_position_x + (BLOCK_SIZE * 2), block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, ORANGE, pygame.Rect(block_position_x, block_position_y + (BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, ORANGE, pygame.Rect(block_position_x + (BLOCK_SIZE), block_position_y + (BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, ORANGE, pygame.Rect(block_position_x + (BLOCK_SIZE * 2), block_position_y + (BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE))

def draw_tetris_block_O(current_x, current_y, STARTING_X, STARTING_Y):

    block_position_x = (current_x * BLOCK_SIZE) + STARTING_X
    block_position_y = (current_y * BLOCK_SIZE) + STARTING_Y

    pygame.draw.rect(screen, YELLOW, pygame.Rect(block_position_x, block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(block_position_x + BLOCK_SIZE, block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(block_position_x, block_position_y + BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, YELLOW, pygame.Rect(block_position_x + (BLOCK_SIZE), block_position_y + (BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE))

def draw_tetris_block_T (current_x, current_y, STARTING_X, STARTING_Y):

    block_position_x = (current_x * BLOCK_SIZE) + STARTING_X
    block_position_y = (current_y * BLOCK_SIZE) + STARTING_Y

    pygame.draw.rect(screen, PURPLE, pygame.Rect(block_position_x + BLOCK_SIZE, block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, PURPLE, pygame.Rect(block_position_x, block_position_y + BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, PURPLE, pygame.Rect(block_position_x + (BLOCK_SIZE), block_position_y + BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, PURPLE, pygame.Rect(block_position_x + (BLOCK_SIZE * 2), block_position_y + BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))


def draw_tetris_block_S(current_x, current_y, STARTING_X, STARTING_Y):

    block_position_x = (current_x * BLOCK_SIZE) + STARTING_X
    block_position_y = (current_y * BLOCK_SIZE) + STARTING_Y

    pygame.draw.rect(screen, GREEN, pygame.Rect(block_position_x + BLOCK_SIZE, block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, GREEN, pygame.Rect(block_position_x + (BLOCK_SIZE * 2), block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, GREEN, pygame.Rect(block_position_x, block_position_y + BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, GREEN, pygame.Rect(block_position_x + BLOCK_SIZE, block_position_y + (BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE))

def draw_tetris_block_S(current_x, current_y, STARTING_X, STARTING_Y):

    block_position_x = (current_x * BLOCK_SIZE) + STARTING_X
    block_position_y = (current_y * BLOCK_SIZE) + STARTING_Y

    pygame.draw.rect(screen, GREEN, pygame.Rect(block_position_x + BLOCK_SIZE, block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, GREEN, pygame.Rect(block_position_x + (BLOCK_SIZE * 2), block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, GREEN, pygame.Rect(block_position_x, block_position_y + BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, GREEN, pygame.Rect(block_position_x + BLOCK_SIZE, block_position_y + (BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE))

def draw_tetris_block_Z(current_x, current_y, STARTING_X, STARTING_Y):

    block_position_x = (current_x * BLOCK_SIZE) + STARTING_X
    block_position_y = (current_y * BLOCK_SIZE) + STARTING_Y

    pygame.draw.rect(screen, RED, pygame.Rect(block_position_x, block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(block_position_x + BLOCK_SIZE, block_position_y, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(block_position_x + BLOCK_SIZE, block_position_y + BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, RED, pygame.Rect(block_position_x + (BLOCK_SIZE * 2), block_position_y + (BLOCK_SIZE), BLOCK_SIZE, BLOCK_SIZE))


def createGameTick():
    global CURRENT_POINT
    draw_game_board()
    check_row_clear()
    CurrentLandedBlocks.draw_landed_blocks()
    nextBlock.display()
    if((CurrentLandedBlocks.blocks[currentBlock.y][currentBlock.x])):
        set_game_over()
    screen.blit(img, (390,70))
    screen.blit(point_text, (390,190))
    point_numb = text_font.render(str(CURRENT_POINT), True, (255,255,255))
    screen.blit(point_numb, (390,230))
    pygame.display.update()

def tetrisTouchdown(): 
    CurrentLandedBlocks.updateLandedBlocks(currentBlock.x, currentBlock.y, currentBlock.block)

running = True
game_over = False

while running:

    clock.tick(35)
  
    for event in pygame.event.get():
    
        if event.type == pygame.QUIT:
            running = False
        if (game_over == False):
            if event.type == TIMER_EVENT:
                currentBlock.draw()

                if(currentBlock.y + currentBlock.height < len(CurrentLandedBlocks.blocks)):

                    setpoint = CurrentLandedBlocks.block_shape[currentBlock.block]

                    for ind1, row in enumerate(setpoint):
                        for ind2, item in enumerate(row):

                            if(row[ind2] == 0):
                                continue

                            if(CurrentLandedBlocks.blocks[currentBlock.y + 1 + ind1][currentBlock.x + ind2]):
                                tetrisTouchdown()
                                currentBlock = nextBlock
                                nextBlock = createTetrisBlock()
                                break

                if currentBlock.y < GAME_BOARD_HEIGHT - currentBlock.height:
                        currentBlock.y += 1
                else:
                    tetrisTouchdown()
                    currentBlock = nextBlock
                    nextBlock = createTetrisBlock()

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_RIGHT:
                    if currentBlock.x < GAME_BOARD_WIDTH - currentBlock.width and CurrentLandedBlocks.blocks[currentBlock.y][currentBlock.x + currentBlock.width] == 0:
                        currentBlock.x +=1
                        currentBlock.draw()

                elif event.key == pygame.K_LEFT:
                    if currentBlock.x > 0 and CurrentLandedBlocks.blocks[currentBlock.y][currentBlock.x -1] == 0:
                        currentBlock.x -=1
                        currentBlock.draw()

                elif event.key == pygame.K_DOWN:
                    last_block = GAME_BOARD_HEIGHT - currentBlock.height
                    setpoint = CurrentLandedBlocks.block_shape[currentBlock.block]

                    found = False
                    for i in range(GAME_BOARD_HEIGHT):

                        for index, block in enumerate(setpoint[-1]):
                            if(block == 0):
                                continue
                            
                            if(CurrentLandedBlocks.blocks[i][currentBlock.x + index] != 0):
                                last_block = i
                                last_block = last_block - currentBlock.height
                                found = True
                                break
                        if found:
                            break

                    currentBlock.y = last_block
                    tetrisTouchdown()
                    currentBlock = nextBlock
                    nextBlock = createTetrisBlock()

                elif event.key == pygame.K_SPACE:

                    print("--------LANDED BLOCKS---------")

                    for item in CurrentLandedBlocks.blocks:
                        print(item)

        createGameTick()

pygame.quit()