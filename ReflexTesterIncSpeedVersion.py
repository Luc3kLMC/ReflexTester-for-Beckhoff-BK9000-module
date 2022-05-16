from pymodbus.client.sync import ModbusTcpClient
import time
import pygame
import os
import sys
import random

pygame.init()
WIDTH = 1000
HEIGHT = 600
clock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Beckhoff Reflex Tester (c) Luc3k")
position = 20
font = pygame.font.SysFont("arial", 16)
blitTxt = [(font.render(str("BECKHOFF REFLEX TESTER"), True, (255, 255, 255))),
           (font.render(str("KEY 1-6 TO TURN OFF RELAY 1-6"), True, (255, 255, 255))),
           (font.render(str("PRESS SPACE TO START"), True, (255, 255, 255))), ]

# had only 6 coils, if you have more (or less) then edit here, then you have to
# edit 'relay' line 39
RELAYS_COUNT = 6

firstLineY = 100 # coords for blitting purposes - rectangles indicating coil states
secondLineY = 200
thirdLineY = 300

class Relay:     
    def __init__(self, coilCount,coilState, TurnOnTicker, TurnOnControl,tickerTempo,score,tempoChanger):
        self.coilCount = coilCount
        self.coilState = coilState
        self.TurnOnTicker = TurnOnTicker
        self.TurnOnControl = TurnOnControl
        self.tickerTempo = tickerTempo
        self.score = score
        self.tempoChanger = tempoChanger
        pass

relay = Relay(RELAYS_COUNT,[False, False, False, False, False, False,],0,False,20,0,0)



for i in range(len(blitTxt)):   # blit info txt on screen
    screen.blit(blitTxt[i], (0, i * position))

run = True

SERVER_HOST = "192.168.200.200"
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

def correctPlayScoreAndTempoHandler():
    relay.score += 1
    relay.tempoChanger += 1
    if relay.tempoChanger >= 2:
        relay.tickerTempo -= 2

def gameOverWhen6RelaysOn():
    global run
    x = 0
    for i in range(6):
        if relay.coilState[i] == True:
            x += 1
    if x >= 6:
        run = False



c.connect()
watchdogReset()

while run:
    #if relay.TurnOnControl != True:
    relay.TurnOnTicker += 1
    if relay.TurnOnTicker >= relay.tickerTempo:
        turnOnRandomRelay()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_1:
                if (relay.coilState[0] != False):
                    relay.coilState[0] = not relay.coilState[0]
                    relay.TurnOnControl = False
                    correctPlayScoreAndTempoHandler()
            if event.key == pygame.K_2:
                if (relay.coilState[1] != False):
                    relay.coilState[1] = not relay.coilState[1]
                    relay.TurnOnControl = False
                    correctPlayScoreAndTempoHandler()
            if event.key == pygame.K_3:
                if (relay.coilState[2] != False):
                    relay.coilState[2] = not relay.coilState[2]
                    relay.TurnOnControl = False
                    correctPlayScoreAndTempoHandler()
            if event.key == pygame.K_4:
                if (relay.coilState[3] != False):
                    relay.coilState[3] = not relay.coilState[3]
                    relay.TurnOnControl = False
                    correctPlayScoreAndTempoHandler()
            if event.key == pygame.K_5:
                if (relay.coilState[4] != False):
                    relay.coilState[4] = not relay.coilState[4]
                    relay.TurnOnControl = False
                    correctPlayScoreAndTempoHandler()
            if event.key == pygame.K_6:
                if (relay.coilState[5] != False):
                    relay.coilState[5] = not relay.coilState[5]
                    relay.TurnOnControl = False
                    correctPlayScoreAndTempoHandler()
            if event.key == pygame.K_ESCAPE:
                turnOffAllRelays(relay.coilCount, relay.coilState)
                c.close()
                run = False

    gameOverWhen6RelaysOn()
    upkeepCoilsState()
    clock.tick(30)
    pygame.display.flip()
