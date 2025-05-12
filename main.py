import pygame
import math
from simpleai.search import SearchProblem, astar

pygame.init()
pygame.display.set_caption("A* Chaser!")
screen = pygame.display.set_mode((800,800))
screen.fill((0,0,0))
clock = pygame.time.Clock()
gameover = False

# Helper Function is_Wall: map collision check for any pixel position
def is_wall(px, py):
    tile_x = px // 40 #each square on the map is 40px x 40px
    tile_y = py // 40
    if 0 <= tile_x < 20 and 0 <= tile_y < 20: #bounds check
        return map[tile_y][tile_x] == 2 #returns true or false
    return True #returns true if out of bounds

# Helper Function get_astar: this calls the pathing algorithm and returns the first recommended direction
def get_astar_direction(ax, ay, px, py):
    start = (ax // 40, ay // 40) #convert coords to square in map
    goal = (px // 40, py // 40)
    problem = GameWalkPuzzle(map, start, goal) # <--THE MOST IMPORTANT LINE
    result = astar(problem) 
    #print(result.path()) #this shows the WHOLE path, but we're only gonna use the first one
    if result and len(result.path()) > 1:
        return result.path()[1][0]  # return "up", "down", etc.
    return None

#class gameWalkPuzzle: Taken from https://github.com/simpleai-team/simpleai/tree/master/samples/search
class GameWalkPuzzle(SearchProblem):
    def __init__(self, board, start, goal):
        self.board = board
        self.start = start
        self.goal = goal
        super(GameWalkPuzzle, self).__init__(initial_state=start)

    def actions(self, state):
        actions = []
        x, y = state
        for move in ["up", "down", "left", "right"]:
            new_x, new_y = x, y
            if move == "up": new_y -= 1
            elif move == "down": new_y += 1
            elif move == "left": new_x -= 1
            elif move == "right": new_x += 1
            if 0 <= new_x < len(self.board[0]) and 0 <= new_y < len(self.board):
                if self.board[new_y][new_x] != 2:
                    actions.append(move)
        return actions

    def result(self, state, action):
        x, y = state
        if action == "up": return (x, y - 1)
        elif action == "down": return (x, y + 1)
        elif action == "left": return (x - 1, y)
        elif action == "right": return (x + 1, y)

    def is_goal(self, state):
        return state == self.goal

    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        return abs(x - gx) + abs(y - gy) #uses Manhattan metric
    

# CONSTANTS
LEFT = 0
RIGHT = 1
UP = 2
DOWN = 3
SPACE = 4
keys = [False, False, False, False, False]


#in a real game, you could use other numbers to represent objects like trees, rocks, etc.
map = [
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2],
    [2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2],
    [2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 0, 2, 2],
    [2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 2],
    [2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2],
    [2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2],
    [2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2],
    [2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2],
    [2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2],
    [2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2],
    [2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 0, 2],
    [2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
    [2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2, 2, 0, 2, 2],
    [2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2],
    [2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 0, 2, 0, 0, 2],
    [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
]

#brick = pygame.image.load('brick.png') #used for walls

xpos = 400
ypos = 440
ax = 50
ay = 50
avx = 0
avy = 0
ad = "right"



ticker = 0 #this ticker was created so we don't call the A* algorithm more than once as we pass through a junction in the map

while not gameover:#GAME LOOP------------------------------------------------------
    clock.tick(60)
    ticker+=1

    #event queue and keyboard input for player
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameover = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT: keys[LEFT] = True
            elif event.key == pygame.K_RIGHT: keys[RIGHT] = True
            elif event.key == pygame.K_UP: keys[UP] = True
            elif event.key == pygame.K_DOWN: keys[DOWN] = True
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT: keys[LEFT] = False
            elif event.key == pygame.K_RIGHT: keys[RIGHT] = False
            elif event.key == pygame.K_UP: keys[UP] = False
            elif event.key == pygame.K_DOWN: keys[DOWN] = False

    # Player movement
    vx = vy = 0
    if keys[LEFT] and not is_wall(xpos-4, ypos) and not is_wall(xpos-4, ypos+18): vx = -3
    elif keys[RIGHT]and not is_wall(xpos+22, ypos) and not is_wall(xpos+22, ypos+18): vx = 3
    if keys[UP] and not is_wall(xpos, ypos-4) and not is_wall(xpos+18, ypos-4): vy = -3
    elif keys[DOWN] and not is_wall(xpos, ypos+22) and not is_wall(xpos+18, ypos+22): vy = 3

    xpos += vx
    ypos += vy

    #AI movement
    #move in a direction back and forth (bouncing off walls)
    
    #moving right or left
    if ad == "right" or ad == "left":
        if ad == "left" and not is_wall(ax-4, ay) and not is_wall(ax-4, ay+18):
            avx = -3
            #print("here")
        else:
            ad = "right"
        if ad == "right" and not is_wall(ax+22, ay) and not is_wall(ax+22, ay+18):
            avx = 3
        else:
            ad = "left"
        
        #check if there's an open space above or below
        if (not is_wall(ax, ay-24) and not is_wall(ax+19, ay-24)) or (not is_wall(ax, ay+44) and not is_wall(ax+19, ay+44)):
            ##print("there's a hole above or below me!", end = " ")
            # There's a vertical junction; let's check A* to see if we should turn
            if ticker > 20:
                move = get_astar_direction(ax, ay, xpos, ypos)
                ticker = 0
                if move == "up" and ad != "down":
                    ad = "up"
                    avx, avy = 0, -3
                elif move == "down" and ad != "up":
                    ad = "down"
                    avx, avy = 0, 3
                #print("a* says to move", ad)
            
    #up and down movement
    if ad == "up" or ad == "down":
        if ad == "up" and not is_wall(ax, ay-20) and not is_wall(ax+19, ay-20):
            avy = -3
            #print("going up.", end = " ") #for testing upwards collision
        else:
            ad = "down"
            #print("bonk up.", end = " ") #for testing upwards collision
        if ad == "down" and not is_wall(ax, ay+22) and not is_wall(ax+19, ay+20): avy = 3
        else: ad = "up"
        
        #check if there's an open space left or right
        if (not is_wall(ax-24, ay) and not is_wall(ax-24, ay+19)) or (not is_wall(ax+42, ay) and not is_wall(ax+42, ay+19)):
            #print("there's a hole to the left or right of me!", end = " ")
            # There's a horizontal junction; let's check A* to see if we should turn
            if ticker > 20:
                move = get_astar_direction(ax, ay, xpos, ypos)
                #print("move is:", move)
                ticker = 0
                if move == "left":
                    ad = "left"
                    avx, avy = -3, 0
                    #print("i just moved left")
                elif move == "right":
                    #print("setting avx to 3")
                    ad = "right"
                    avx, avy = 3, 0
                #print("a* says to move", ad, end = " ")
    
    #print("avx is", avx)
    #update final AI position for this game loop
    ax += avx
    ay += avy

    #render section------------------------------------------------------------
    screen.fill((0, 0, 0))
    #draw the map
    for i in range(20):
        for j in range(20):
            if map[i][j] == 2:
                #screen.blit(brick, (j * 40, i * 40), (0, 0, 40, 40))
                pygame.draw.rect(screen,(100,0,0),(j * 40, i * 40, 40, 40))
                
    pygame.draw.rect(screen, (0, 255, 0), (xpos, ypos, 20, 20)) #draw the player
    pygame.draw.rect(screen, (200, 0, 255), (ax, ay, 20, 20)) #draw the AI
    pygame.display.flip()

pygame.quit()

