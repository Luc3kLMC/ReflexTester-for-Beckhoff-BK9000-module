from pymodbus.client.sync import ModbusTcpClient
import time
import pygame
import os
import sys
import random

pygame.init()
WIDTH = 800
HEIGHT = 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beckhoff Reflex Tester (c) Luc3k")
position = 20
font = pygame.font.SysFont("arial", 16)

# had only 6 coils, if you have more (or less) then edit here, then you have to
# edit relay.coilState in cleanVariablesOnStart(), and 'relay' in line 52
RELAYS_COUNT = 6

firstLineY = 100 # coords for blitting purposes - rectangles indicating coil states
secondLineY = 200
thirdLineY = 300

class Relay: 
    def __init__(self, coilCount,coilState, TurnOnTicker, TurnOnControl,tickerTempo,score, timeStart, timeEnd, timeAvg, timeAggregate):
        self.coilCount = coilCount
        self.coilState = coilState
        self.TurnOnTicker = TurnOnTicker
        self.TurnOnControl = TurnOnControl
        self.tickerTempo = tickerTempo
        self.score = score
        self.timeStart = timeStart
        self.timeEnd = timeEnd
        self.timeAvg = timeAvg
        self.timeAggregate = timeAggregate
        pass

def cleanVariablesOnStart():
    relay.coilCount = RELAYS_COUNT
    relay.coilState = [False, False, False, False, False, False,]
    relay.TurnOnTicker = 0
    relay.TurnOnControl = False
    relay.tickerTempo = 20
    relay.score = 0
    relay.timeStart = 0
    relay.timeEnd = 0
    relay.timeAvg = 0
    relay.timeAggregate = 0
    

relay = Relay(RELAYS_COUNT,[False, False, False, False, False, False,],0,False,20,0,0,0,0,0)

blitTxt = [(font.render(str("BECKHOFF REFLEX TESTER"), True, (255, 255, 255))),
           (font.render(str("KEY 1-6 TO TURN OFF RELAY 1-6"), True, (255, 255, 255))),
           (font.render(str("PRESS SPACE TO START"), True, (255, 255, 255))),
           (font.render(str(float(relay.timeAvg)), True, (255, 255, 255))), ]


run = True
game = False
menu = True

drawMenuOnce = False

SERVER_HOST = "192.168.200.200"  # update with your Beckhoff IP when configured
SERVER_PORT = 502

c = ModbusTcpClient(SERVER_HOST)

def watchdogReset():
    c.write_register(0x1121, 0xBECF)
    c.write_register(0x1121, 0xAFFE)

def turnOffAllRelays():
    for i in range(relay.coilCount):
        relay.coilState[i] = False
        c.write_coil(i, relay.coilState[i])
        result = c.read_coils(i, 1)
        print(result.bits[0])

def upkeepCoilsState():  # called repetitively to keep coil active
        c.write_coil(0, relay.coilState[0])
        c.write_coil(1, relay.coilState[1])
        c.write_coil(2, relay.coilState[2])
        c.write_coil(3, relay.coilState[3])
        c.write_coil(4, relay.coilState[4])
        c.write_coil(5, relay.coilState[5])

def turnOnRandomRelay():
    x = random.randint(0,5)
    if relay.coilState[x] == False:
        relay.coilState[x] = True
        c.write_coil(x, relay.coilState[0])
        relay.TurnOnTicker = 0
        relay.TurnOnControl = True
        relay.timeStart = time.time()
        

def correctPlayScoreHandler():
    relay.score += 1
    relay.timeEnd = time.time()
    relay.timeAggregate += relay.timeEnd - relay.timeStart
    relay.timeAvg = relay.timeAggregate / relay.score
    print(relay.timeAvg)

def setTickerTempoRandomValue():
    x = random.randint(4,20)
    relay.tickerTempo = x

def gameOverCheckAndHandler():
    global drawMenuOnce,game,menu
    if relay.score >= 4:
        blitTxt[3] = (font.render(str("YOUR AVG TIME FROM 4 HITS: "+str(float(relay.timeAvg))), True, (255, 255, 255)))
        relay.score = 0
        drawMenuOnce = False
        game = False
        menu = True

c.connect()
watchdogReset()

while run == True:

    while menu == True:
        if drawMenuOnce == False:
            pygame.draw.rect(screen, (0,0,random.randint(0,255)), pygame.Rect(0, 0, 800, 600))
            for i in range(len(blitTxt)):   # blit info txt on screen
                screen.blit(blitTxt[i], (0, i * position))
                
            pygame.display.flip()
            drawMenuOnce = True
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    cleanVariablesOnStart()
                    c.connect()
                    watchdogReset()
                    menu = False
                    game = True
                if event.key == pygame.K_ESCAPE:
                    turnOffAllRelays()
                    c.close()
                    menu = False
                    run = False


    while game == True:
        if relay.TurnOnControl != True:
            relay.TurnOnTicker += 1
        if relay.TurnOnTicker >= relay.tickerTempo:
            turnOnRandomRelay()
            setTickerTempoRandomValue()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    if (relay.coilState[0] != False):
                        relay.coilState[0] = not relay.coilState[0]
                        relay.TurnOnControl = False
                        correctPlayScoreHandler()
                if event.key == pygame.K_2:
                    if (relay.coilState[1] != False):
                        relay.coilState[1] = not relay.coilState[1]
                        relay.TurnOnControl = False
                        correctPlayScoreHandler()
                if event.key == pygame.K_3:
                    if (relay.coilState[2] != False):
                        relay.coilState[2] = not relay.coilState[2]
                        relay.TurnOnControl = False
                        correctPlayScoreHandler()
                if event.key == pygame.K_4:
                    if (relay.coilState[3] != False):
                        relay.coilState[3] = not relay.coilState[3]
                        relay.TurnOnControl = False
                        correctPlayScoreHandler()
                if event.key == pygame.K_5:
                    if (relay.coilState[4] != False):
                        relay.coilState[4] = not relay.coilState[4]
                        relay.TurnOnControl = False
                        correctPlayScoreHandler()
                if event.key == pygame.K_6:
                    if (relay.coilState[5] != False):
                        relay.coilState[5] = not relay.coilState[5]
                        relay.TurnOnControl = False
                        correctPlayScoreHandler()
                if event.key == pygame.K_ESCAPE:
                    turnOffAllRelays()
                    game = False
                    menu = True

        gameOverCheckAndHandler()
        upkeepCoilsState()
        clock.tick(30)
        pygame.display.flip()
