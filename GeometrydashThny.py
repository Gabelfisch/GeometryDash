# (c) Gabriel Sinz
# pygame reference: https://www.pygame.org/docs/

import pygame, time as Time
from sys import exit

# vars----------------------------------------------------------------
# isRunning's
pygame.init()
isGameRunning = True
isChooseLevels = True
isAftergame = True
isGeneralLoop = True
isEditLevel = False

#gravity, jumping usw.
gravity = 0
isOnBlck = False
pos_Y = None
isJump = False

#level
level = None

#text
font = pygame.font.Font("fonts/MinecraftRegular-Bmg3.otf", 40)
font2 = pygame.font.Font("fonts/MinecraftRegular-Bmg3.otf", 20)
txtBgSize = 20

# Editor
userInput = ""
inputRect = pygame.Rect(100, 400, 800, 40)
active = True
showLevel = False

# screen
screenH = 500
screenW = 1000
screen = pygame.display.set_mode((screenW,screenH))
pygame.display.set_caption("Geometry Dash")

clock = pygame.time.Clock()
time = 0
wait = 1

# Colors
color = "#c0e8ec"

# Debug--------------------------------------------------

#Mouse Pos
def mousepos():
    if event.type == pygame.MOUSEMOTION:
        print(event.pos)
#Mouse collision with a rect  
def mouseRect(a):
    if event.type == pygame.MOUSEMOTION:
        if a.collidepoint(event.pos):
            print(event.pos)
            
#KeyPressed
def keyPrsd(keyToTest):
    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
        print(f"key {keyToTest} pressed")

# --------------------- rects ------------------------------------------------------

# Sufaces
backGround = pygame.image.load("Pictures/BG.png").convert()
bgRect = backGround.get_rect(topleft = (0,0))
floor = pygame.image.load("Pictures/floor.png").convert_alpha()
floorRect = floor.get_rect(topleft = (0,300))




# -------------- Classes --------------------

class Text():
    def __init__(self):
        super().__init__()
    
    def esc():
        textT = font2.render("Press ESC to choose Level", False, "white")
        textR = textT.get_rect(topleft = (20, 20))
        screen.blit(textT, textR)
    
    def level1():
        global isChooseLevels, isGameRunning
        
        textT = font.render("Level 1", False, "Pink")
        textR = textT.get_rect(center = (screenW//2, 40))
        pygame.draw.rect(screen, color, textR, txtBgSize, 8)
        screen.blit(textT, textR)      
    
        if (textR.collidepoint(pygame.mouse.get_pos())) and \
        ((event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1)):
            isChooseLevels = False
            isGameRunning = True
            level1()
            
    def customLevel():
        global isChooseLevels, isGameRunning, level
        
        if showLevel:
            textT = font.render("Custom Level", False, "Pink")
            textR = textT.get_rect(center = (screenW//2, 380))
            pygame.draw.rect(screen, color, textR, txtBgSize, 8)
            screen.blit(textT, textR)      
        
            if (textR.collidepoint(pygame.mouse.get_pos())) and \
            ((event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1)):
                isChooseLevels = False
                isGameRunning = True
                f = open("EditorLevel.txt", "r")
                level = f.read()
                f.close()
                print(level)
                
                return level
        
    
    def level2():
        global isChooseLevels, isGameRunning
        
        textT = font.render("Level 2", False, "Pink")
        textR = textT.get_rect(center = (screenW//2, 100))
        pygame.draw.rect(screen, color, textR, txtBgSize, 8)
        screen.blit(textT, textR)      
        
        if (textR.collidepoint(pygame.mouse.get_pos())) and \
        ((event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1)):
            isChooseLevels = False
            isGameRunning = True
            level2()
    
    
        return isChooseLevels, isGameRunning
    
    def levelEditor():
        global isChooseLevels, isGameRunning, isEditLevel
        
        textT = font.render("Level Editor", False, "Pink")
        textR = textT.get_rect(center = (screenW//2, screenH - 50))
        pygame.draw.rect(screen, color, textR, txtBgSize, 8)
        screen.blit(textT, textR)      
    
        if (textR.collidepoint(pygame.mouse.get_pos())) and \
        ((event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1)):
            isChooseLevels = False
            isGameRunning = False
            isEditLevel = True
            print(isGameRunning)
        
        return isChooseLevels, isGameRunning, isEditLevel
   

    def closeEditor():
        global isEditLevel, isAftergame, isChooseLevels
        
        textT = font.render("Close and Save Editor", False, "Pink")
        textR = textT.get_rect(center = (screenW//2, 40))
        screen.blit(textT, textR)      
    
        if (textR.collidepoint(pygame.mouse.get_pos())) and \
        ((event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1)):
            #save the level
            userLevel = open("EditorLevel.txt", "w")
            userLevel.write(userInput)
            userLevel.close()
            
            # close editor
            isEditLevel = False
            isAftergame = False
            isChooseLevels = True 
            
            
        return isEditLevel, isAftergame, isChooseLevels
            #userLevel = open("EditorLevel.txt", "r")
            #print(userLevel.read())


    def gameOver():
        global isAftergame, isChooseLevels

        textT = font.render("you won! / other levels", False, "White")
        textR = textT.get_rect(center = (screenW//2, screenH//2.5))
        #pygame.draw.rect(screen, color, textR, txtBgSize, 8)
        screen.blit(textT, textR)      
    
        if (textR.collidepoint(pygame.mouse.get_pos())) and \
        ((event.type == pygame.MOUSEBUTTONDOWN) and (event.button == 1)):
            isAftergame = False
            
        isChooseLevels = True
    
        
        return isAftergame, isChooseLevels
    
        
class Block(pygame.sprite.Sprite):
    def __init__(self, type, posDelay, posy):
        super().__init__()
        
        self.posY = posy        
        self.type = type
        
        if type == "#" or type == "§":
            self.image = pygame.image.load("pictures/block2.png").convert_alpha()
            self.rect = self.image.get_rect(bottomleft = (200+posDelay, self.posY))
            
        elif type == "^":
            self.image = pygame.image.load("pictures/spike.png").convert_alpha()
            self.rect = self.image.get_rect(bottomleft = (200+posDelay, self.posY + 25))
        
    def mouseCol(self):   
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                print(event.pos)
                
    def playerCol(self):
        global pos_Y
        
        if pygame.sprite.spritecollide(self, player, False):
            pos_Y = self.rect.y
        
        return pos_Y
    
    def destroy(self):
        if self.rect.x <= -100:
            self.kill()
            #self.rect.x = 300
    
    def finishGame(self):
        global isGameRunning, isAftergame
        
        if self.type == "§":
            if self.rect.x <= - 50:
                isGameRunning = False
                isAftergame = True
                
                
        return isGameRunning, isAftergame
        

    def update(self):
        self.rect.x -= 2.7
        self.mouseCol()
        self.destroy()
        self.playerCol()
        self.finishGame()
        
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("pictures/player.png").convert_alpha()
        self.rect = self.image.get_rect(bottomleft = (100,300))
        self.gravity = 0
        
    def playerInput(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and (self.rect.bottom >= 300 or isJump):
            self.gravity = -14
            self.gravity += 0.9
            self.rect.y += self.gravity

    def applyGravity(self):
        if not isOnBlck:
            self.gravity += 0.9
            self.rect.y += self.gravity
            if self.rect.bottom >= 300:
                self.rect.bottom = 300
            
    def colBlock(self):
        global isJump, isOnBlck, isGameRunning, isAftergame, block, time
        
        for item in block:
            if pygame.sprite.spritecollide(item, player, False):
                if self.rect.y >= pos_Y:
                    #isGameRunning = False
                    #isAftergame = True
                    block = pygame.sprite.Group()
                    Time.sleep(wait)
                    generateLvl()
                    time = 0
                    
                elif self.rect.y <= pos_Y:
                    if item.type == "^":
                        block = pygame.sprite.Group()
                        Time.sleep(wait)
                        generateLvl()
                        time = 0
                        
                    else:
                        isOnBlck = True
                        isJump = True
                        self.rect.y = pos_Y - 24
                        
            elif not pygame.sprite.spritecollide(item, player, False) and not isOnBlck:
                isOnBlck = False
#                gravity = 0
                
        return isJump, isOnBlck, isGameRunning, isAftergame, time


    def update(self):
 
        self.colBlock()
        self.playerInput()
        self.applyGravity()



# -------------------- defs --------------------------

def level1():
    global level
    level = "^^<<<^>#<<<^>>>>#<<<^<<<^<<<#§"
    return level

def level2():  
    global level
    level = "v#<<<v#<<<v#<<<^>>#<<<<^<<<^<<<^<<<^<<<^<<<<# #  #   #  <<# <<#<<#<<v#5              §"
    return level

def textInput():
    # has to be in the event Loop!!!
    global userInput
    
    #if event.type == pygame.MOUSEBUTTONDOWN:
        #if 
    
    if event.type == pygame.KEYDOWN:
        if active:
            if event.key == pygame.K_BACKSPACE:
                userInput = userInput[:-1]
            else:
                userInput += event.unicode
            
    
    return userInput        

# Text
def text():
    textT = font.render(f"score {int(time/10)}", False, "Pink")
    textR = textT.get_rect(center = (500, 20))
    pygame.draw.rect(screen, color, textR, txtBgSize, 8)
    screen.blit(textT, textR)
    
def generateLvl():
    
    blckTuple = ("#","^","§")
    x = 0
    tempY = 0
    for item in level:
        y = 275
        x += 100
        if item == " ":
            tempY += 25
            x -= 100
        elif item == ">":
            x += 25
            x -= 100
        elif item == "<":
            x -= 25
            x -= 100
        elif item == "v":
            tempY -= 25
            x -= 100
        
        elif item in blckTuple:
            y -= tempY
            block.add(Block(item, x, y))
            tempY = 0
            
        else:
            x -= 100

def drawEditorTxt():
    #global
    
    #BG
    screen.blit(backGround, bgRect)
    screen.blit(floor,floorRect)
    #Text
    textSurf = font.render(userInput, True, "#000000")
    pygame.draw.rect(screen, "yellow", inputRect, 2)   
    screen.blit(textSurf,inputRect)
    inputRect.w = max(200, textSurf.get_width())
    
    if inputRect.x + inputRect.w >= screenW - 100:
        inputRect.x -= 5
    elif inputRect.x < 100:
        inputRect.x +=5 
        
    #screen.blit(textSurf,(20,20))
    #return
        
        

# ----------------------------- GameLoop --------------------------------------

# Player
player = pygame.sprite.GroupSingle()
player.add(Player())

block = pygame.sprite.Group()

# Test if level is there
try:
    f = open("EditorLevel.txt", "r")
    userInput = f.read()
    f.close()
    showLevel = True
            
except:
    f = open("EditorLevel.txt", "x")
    f.close()


# ------------------------- Game Loop --------------------------------------
while isGeneralLoop:
    block.empty()

    while isChooseLevels:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
                
        screen.fill("lightgreen")
        Text.level1()
        Text.level2()
        Text.customLevel()
        Text.levelEditor()
        pygame.display.update()


# ---------------------------- GameRunning ---------------
    if isGameRunning:
        generateLvl()

    while isGameRunning:
        
        isOnBlck = False
        isJump = False
        time += 1
        
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                exit()
                
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                isGameRunning = False
                isAftergame = False
                isChooseLevels = True
    
#----Debug------------
                
#    mousepos()
#    keyPrsd(#ausgabewert erinfgebr)
        
#---- BG ----
        screen.blit(backGround, bgRect)
        screen.blit(floor,floorRect)
        text()
        Text.esc()

#----Block --------
        block.update()
        block.draw(screen)
        
#----Player --------
        player.update()
        player.draw(screen)
        
#----Display & Clock --- 
        pygame.display.update()
        clock.tick(50)


# Level Editor ------------------------------------
    if isEditLevel:
        try:
            f = open("EditorLevel.txt", "r")
            userInput = f.read()
            f.close()
            showLevel = True
            
        except:
            f = open("EditorLevel.txt", "x")
            f.close()
      
    while isEditLevel:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT):
                pygame.quit()
                exit()
            if (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                isEditLevel = False
                isAftergame = False
                isChooseLevels = True
                
            textInput()
# BG
        level = userInput
        block.empty()
        generateLvl()
        drawEditorTxt()
        block.draw(screen)
        Text.closeEditor()
        
        pygame.display.flip()

# ------------------------------- AfterGame -----------------------------------
        
    while isAftergame:
        for event in pygame.event.get():
            if (event.type == pygame.QUIT) or \
                (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                pygame.quit()
                exit()
                
        Text.gameOver()
        textSurf = font.render(userInput, True, "#000000")
        pygame.display.update()
        clock.tick(50)
    #clock.tick(50)
            
    
    