

import pygame
import sys
import random
import pygbutton
import time

from pygame.locals import *

pygame.init()
pygame.mixer.init()
pygame.font.init()
pygame.key.set_repeat(100, 100)             #enables holding down a key instead only keyup / keydown, parameter delay and interval
pygame.display.set_caption('PSEtris')

smallfont = pygame.font.SysFont('Arial', 22)
mediumfont = pygame.font.SysFont('Arial', 30)
BIGFONT = pygame.font.SysFont('Arial', 60)

FPSCLOCK = pygame.time.Clock()
FPS = 30

offsetx = 50                
offsety = 100              

ELEMENTHEIGHT = 60
ELEMENTWIDTH = 50
GAPSIZE = 3
WINDOWWIDTH = 18 * ELEMENTWIDTH + 17 * GAPSIZE + 2 * offsetx
WINDOWHEIGHT = 900
SPEED = 4

INITSCREENWIDTH = 500
INITSCREENHEIGHT = 400

#            R    G    B
GRAY     = (100, 100, 100)
NAVYBLUE = ( 60,  60, 100)
WHITE    = (255, 255, 255)
RED      = (255,   0,   0)
GREEN    = (  0, 220,   0)
BLUE     = (  0,   0, 255)
YELLOW   = (255, 255,   0)
ORANGE   = (240, 128,   0)
PURPLE   = (255,   0, 255)
CYAN     = (  0, 255, 255)
BLACK    = (  0,   0,   0)
DARKGREEN =( 51, 132,  17)

BGCOLOR = WHITE

global Score, sound, soundlabel
sound = True
soundlabel = 'Sound On'


DISPLAYSURF = pygame.display.set_mode((INITSCREENWIDTH, INITSCREENHEIGHT))
errorsound = pygame.mixer.Sound('boing.wav')
rightsound = pygame.mixer.Sound('click.wav')
fanfare = pygame.mixer.Sound('fanfare2.wav')

buttonEASY = pygbutton.PygButton((100, 300, 80, 40), 'MG')
buttonMEDIUM = pygbutton.PygButton((200, 300, 80, 40), 'TM')
buttonHARD = pygbutton.PygButton((300, 300, 80, 40), 'MG + TM')
buttonSOUND = pygbutton.PygButton((400, 350, 150, 40), 'SoundOn')

PSE = {'H' : ( 1, 1), 'Li': ( 1, 2), 'Na': ( 1, 3), 'K' : ( 1, 4), 'Rb': ( 1, 5), 'Cs': ( 1, 6), 'Fr': ( 1, 7),
       'Be': ( 2, 2), 'Mg': ( 2, 3), 'Ca': ( 2, 4), 'Sr': ( 2, 5), 'Ba': ( 2, 6), 'Ra': ( 2, 7),
       'Sc': ( 3, 4), 'Y' : ( 3, 5), 'La': ( 3, 6), 'Ac': ( 3, 7),
       'Ti': ( 4, 4), 'Zr': ( 4, 5), 'Hf': ( 4, 6),
       'V' : ( 5, 4), 'Nb': ( 5, 5), 'Ta': ( 5, 6),
       'Cr': ( 6, 4), 'Mo': ( 6, 5), 'W' : ( 6, 6),
       'Mn': ( 7, 4), 'Tc': ( 7, 5), 'Re': ( 7, 6),
       'Fe': ( 8, 4), 'Ru': ( 8, 5), 'Os': ( 8, 6),
       'Co': ( 9, 4), 'Rh': ( 9, 5), 'Ir': ( 9, 6),
       'Ni': (10, 4), 'Pd': (10, 5), 'Pt': (10, 6),
       'Cu': (11, 4), 'Ag': (11, 5), 'Au': (11, 6),
       'Zn': (12, 4), 'Cd': (12, 5), 'Hg': (12, 6),
       'B' : (13, 2), 'Al': (13, 3), 'Ga': (13, 4), 'In': (13, 5), 'Tl': (13, 6),
       'C' : (14, 2), 'Si': (14, 3), 'Ge': (14, 4), 'Sn': (14, 5), 'Pb': (14, 6),
       'N' : (15, 2), 'P' : (15, 3), 'As': (15, 4), 'Sb': (15, 5), 'Bi': (15, 6),
       'O' : (16, 2), 'S' : (16, 3), 'Se': (16, 4), 'Te': (16, 5), 'Po': (16, 6),
       'F' : (17, 2), 'Cl': (17, 3), 'Br': (17, 4), 'I' : (17, 5), 'At': (17, 6),
       'He': (18, 1), 'Ne': (18, 2), 'Ar': (18, 3), 'Kr': (18, 4), 'Xe': (18, 5), 'Rn': (18, 6)}

upperBound = [[1, 0], [2, 1], [3, 3], [4, 3], [5, 3], [6, 3], [7, 3], [8, 3], [9, 3], [10, 3], [11, 3],
              [12, 3], [13, 1], [14, 1], [15, 1], [16, 1], [17, 1], [18, 0]]

GroupNumbersandGridPositions = [(1, 0), (2, 1), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3), (8, 3), (9, 3), (10, 3), (11, 3),
              (12, 3), (13, 1), (14, 1), (15, 1), (16, 1), (17, 1), (18, 0)]

elements = []
solved = []

def initGame():
    DISPLAYSURF = pygame.display.set_mode((INITSCREENWIDTH, INITSCREENHEIGHT))
    while True:
        DISPLAYSURF.fill(WHITE)
        writeInitScreen()
        drawDifficultyButtons()
        DrawSoundButton(soundlabel)
        initEventHandling()
        pygame.display.update()
pass

def Soundlabel():
    global soundlabel
    if sound == True:
        soundlabel = 'Sound On'
    else:
        soundlabel = 'Sound Off'

def writeInitScreen():
    LogoSurface = BIGFONT.render('Let\'s play PSEtris', True, BLUE)
    DifficultySurface = smallfont.render('MG = Main groups, TM = Transition metals', True, BLACK)
    DISPLAYSURF.blit(LogoSurface, ((INITSCREENWIDTH - LogoSurface.get_width()) / 2, 100))
    DISPLAYSURF.blit(DifficultySurface, ((INITSCREENWIDTH - DifficultySurface.get_width()) / 2, 250))

def drawDifficultyButtons():
    buttonEASY.draw(DISPLAYSURF)
    buttonMEDIUM.draw(DISPLAYSURF)
    buttonHARD.draw(DISPLAYSURF)

def DrawSoundButton(soundlabel):
    buttonSOUND = pygbutton.PygButton((400, 350, 80, 40), soundlabel)
    buttonSOUND.draw(DISPLAYSURF)

def initEventHandling():
    global sound
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_m:
                sound = not sound
                Soundlabel()
        if 'click' in buttonSOUND.handleEvent(event):
            sound = not sound
            Soundlabel()
        if 'click' in buttonEASY.handleEvent(event):
            setGamestate('MG')
            GameLoop()
        if 'click' in buttonMEDIUM.handleEvent(event):
            setGamestate('TM')
            GameLoop()
        if 'click' in buttonHARD.handleEvent(event):
            setGamestate('MG+TM')
            GameLoop()


    
def setGamestate(difficulty):
    groupdict=  {1: ['H', 'Li', 'Na', 'K', 'Rb', 'Cs', 'Fr'],
                 2: ['Be', 'Mg', 'Ca', 'Sr', 'Ba', 'Ra'],
                 3: ['Sc', 'Y', 'La', 'Ac'],
                 4: ['Ti', 'Zr', 'Hf'],
                 5: ['V', 'Nb', 'Ta'],
                 6: ['Cr', 'Mo', 'W'],
                 7: ['Mn', 'Tc', 'Re'],
                 8: ['Fe', 'Ru', 'Os'],
                 9: ['Co', 'Rh', 'Ir'],
                10: ['Ni', 'Pd', 'Pt'],
                11: ['Cu', 'Ag', 'Au'],
                12: ['Zn', 'Cd', 'Hg'],
                13: ['B', 'Al', 'Ga', 'In', 'Tl'],
                14: ['C', 'Si', 'Ge', 'Sn', 'Pb'],
                15: ['N', 'P', 'As', 'Sb', 'Bi'],
                16: ['O', 'S', 'Se', 'Te', 'Po'],
                17: ['F', 'Cl', 'Br', 'I', 'At'],
                18: ['He', 'Ne', 'Ar', 'Kr', 'Xe', 'Rn']}
    resetUpperBound()
    if difficulty == 'MG':
        groups = [1, 2, 13, 14, 15, 16, 17, 18]
        for number in groups:
            elements.append(groupdict[number])
    if difficulty == 'TM':
        groups = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        for number in groups:
            elements.append(groupdict[number])
    if difficulty == 'MG+TM':
        groups = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
        for number in groups:
            elements.append(groupdict[number])
    solved.clear()
    global ElementonScreen, Score, ScoreTimeStart
    ScoreTimeStart = time.monotonic()
    ElementonScreen = False
    Score = 0
pass

def resetUpperBound():
    upperBound.clear()
    for i in GroupNumbersandGridPositions:
        upperBound.append(list(i))


def GameLoop(element = None, ElementX = 700, ElementY = 850):
    DISPLAYSURF = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    while True:
        checkforGameEnd()
        DISPLAYSURF.fill(BGCOLOR)
        drawPSE()
        drawGroupNumbers()
        drawSolvedElements()
        element, ElementX, ElementY = ElementLogic(element, ElementX, ElementY)
        ElementX, ElementY = EventHandling(ElementX, ElementY)
        checkPosition(element, ElementX, ElementY)
        drawElement(element, ElementX, ElementY)
        drawHighlight(ElementX)
        drawScore()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
pass

def checkforGameEnd():
    global Score
    if elements == []:
        DISPLAYSURF.fill(BGCOLOR)
        finalscore = BIGFONT.render('Final Score: ' + str(Score), True, (0, 0, 0))
        DISPLAYSURF.blit(finalscore, ((WINDOWWIDTH / 2 - finalscore.get_width() / 2), 100))
        pygame.display.update()
        if sound == True:
            pygame.mixer.Sound.play(fanfare)
        time.sleep(4)
        initGame()
pass

def drawPSE():
    for Element in PSE:
        XCoordinate = gridx_to_pixelx(PSE[Element][0])
        YCoordinate = gridy_to_pixely(PSE[Element][1])
        if 1 <= PSE[Element][0] <= 2 or 13 <= PSE[Element][0] <= 18:
            GROUPCOLOR = GREEN
        else:
            GROUPCOLOR = ORANGE
        pygame.draw.rect(DISPLAYSURF, GROUPCOLOR, (XCoordinate, YCoordinate, ELEMENTWIDTH, ELEMENTHEIGHT), 0)
pass

def drawGroupNumbers():
    for number in GroupNumbersandGridPositions:
        groupnumbertextsurface = smallfont.render(str(number[0]), True, (0, 0, 0))
        grouptextcoordx = gridx_to_pixelx(number[0]) + ((ELEMENTWIDTH - groupnumbertextsurface.get_width()) / 2)
        grouptextcoordy = gridy_to_pixely(GroupNumbersandGridPositions[(number[1])][1])+30
        DISPLAYSURF.blit(groupnumbertextsurface, (grouptextcoordx, grouptextcoordy))
pass

def drawSolvedElements():
    for x in solved:
        solvedtextsurface = mediumfont.render(x, True, (0, 0, 0))
        textcoordx = gridx_to_pixelx(PSE[x][0]) + ((ELEMENTWIDTH - solvedtextsurface.get_width()) / 2)
        textcoordy = gridy_to_pixely(PSE[x][1]) + ((ELEMENTHEIGHT - solvedtextsurface.get_height()) / 2)
        DISPLAYSURF.blit(solvedtextsurface, (textcoordx, textcoordy))
pass

def ElementLogic(element = None, ElementX = 700, ElementY = 850):
    global ElementonScreen, Score
    if ElementonScreen is False:
        z = random.randint(5, 13)
        ElementX = gridx_to_pixelx(z - 1)
        ElementY = 850
        element = pickRandomElement()
    else:
        ElementY -= SPEED
    return element, ElementX, ElementY
pass

def pickRandomElement():
    if [] in elements:
        elements.remove([])
        checkforGameEnd()
    r = random.randint(0, (len(elements) - 1))
    element = elements[r][0]
    global ElementonScreen
    ElementonScreen = True
    return element
pass

def EventHandling(ElementX=700, ElementY=850):
    global sound
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                if ElementX > offsetx: 
                    ElementX -= (ELEMENTWIDTH + GAPSIZE)
            if event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                if ElementX < (WINDOWWIDTH - offsetx - ELEMENTWIDTH): 
                    ElementX += (ELEMENTWIDTH + GAPSIZE)
            if event.key == pygame.K_UP or event.key == pygame.K_w:
                ElementY = getBlockCoordinateY(ElementX)
            if event.key == pygame.K_m:
                sound = not sound
    return ElementX, ElementY

def checkPosition(element, ElementX, ElementY):
    global ElementonScreen, Score
    trueXforElement = gridx_to_pixelx(PSE[element][0])
    trueYforElement = gridy_to_pixely(PSE[element][1])
    BlockCoordinateY = getBlockCoordinateY(ElementX)
    if trueXforElement == ElementX and (trueYforElement - SPEED) <= ElementY <= (trueYforElement + SPEED):
        ElementinrightPosition(element)
    elif trueXforElement != ElementX and ElementY <= (BlockCoordinateY + SPEED) or trueXforElement == ElementX and ElementY <= BlockCoordinateY :
        ElementinwrongPosition()
pass

def ElementinrightPosition(element):
    solved.append(element)
    global ElementonScreen, Score, ScoreTimeStart
    ElementonScreen = False
    upperBound[PSE[element][0] - 1][1] += 1
    scoretime = (int(100*time.monotonic()) - int(100*ScoreTimeStart))/100
    addscore = int(10 + (25 - (10 * scoretime)))
    if addscore < 10:
        Score += 10
    else:
        Score += addscore 
    print('Score:', Score)
    print('AddScore:', addscore)
    ScoreTimeStart = time.monotonic()
    if sound == True:
        pygame.mixer.Sound.play(rightsound)
    for elementlist in elements:
        if element in elementlist:
            elementlist.remove(element)
pass

def ElementinwrongPosition():
    global ElementonScreen, Score
    ElementonScreen = False
    Score -= 10
    if sound == True:
        pygame.mixer.Sound.play(errorsound)
    ScoreTimeStart = time.monotonic()
pass

def drawElement(element, ElementX, ElementY):
    global ScoreTimeStart
    ElementRect = pygame.draw.rect(DISPLAYSURF, BLACK, (ElementX, ElementY, ELEMENTWIDTH, ELEMENTHEIGHT), 2)
    movingElementText = mediumfont.render(element, True, (0, 0, 0))
    textcoordx = ElementRect.left + ((ElementRect.width - movingElementText.get_width()) / 2)
    textcoordy = ElementRect.top + ((ElementRect.height - movingElementText.get_height()) / 2)
    DISPLAYSURF.blit(movingElementText, (textcoordx, textcoordy))
pass

def drawHighlight(ElementX):
    group = pixelx_to_gridx(ElementX)
    HighlightYCoordinates = getBlockCoordinateY(ElementX)
    Highlight = pygame.draw.rect(DISPLAYSURF, BLUE, (ElementX, HighlightYCoordinates, ELEMENTWIDTH, ELEMENTHEIGHT), 4)
pass

def drawScore():
    ScoreTextSurface = mediumfont.render('Score: '+ str(Score), True, (0, 0, 0))
    DISPLAYSURF.blit(ScoreTextSurface, (5,5))
pass

def getBlockCoordinateY(ElementX):
    group = pixelx_to_gridx(ElementX)
    BlockCoordinateY = gridy_to_pixely(upperBound[(group - 1)][1]) + ELEMENTHEIGHT + GAPSIZE
    return BlockCoordinateY
pass

def gridx_to_pixelx(gridposition):
    return offsetx + ((gridposition - 1) * ELEMENTWIDTH) + ((gridposition - 1) * GAPSIZE)
def gridy_to_pixely(gridposition):
    return offsety + ((gridposition - 1) * ELEMENTHEIGHT) + ((gridposition - 1) * GAPSIZE)
def pixelx_to_gridx(ElementX):
    return int((ElementX - offsetx + ELEMENTWIDTH + GAPSIZE) / (ELEMENTWIDTH + GAPSIZE))
def pixely_to_gridy(ElementY):
    return int((ElementY - offsety + ELEMENTHEIGHT + GAPSIZE) / (ELEMENTHEIGHT + GAPSIZE))

initGame()
