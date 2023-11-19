from pygame import key, K_DOWN, K_UP, K_LEFT, K_RIGHT, K_u, K_j, event
import pickle
from sklearn.ensemble import RandomForestClassifier

import msgParser
import carState
import carControl
import sys
import msvcrt
import keyboard
import pygame
import numpy as np

class Driver(object):
    '''
    A driver object for the SCRC
    '''

    def __init__(self, stage):
        '''Constructor'''
        self.WARM_UP = 0
        self.QUALIFYING = 1
        self.RACE = 2
        self.UNKNOWN = 3
        self.stage = stage

        self.parser = msgParser.MsgParser()

        self.state = carState.CarState()

        self.control = carControl.CarControl()

        self.steer_lock = 0.785398
        self.max_speed = 100
        self.prev_rpm = None

        self.storingData = ""
        pygame.init()
        fps = 60
        fpsClock = pygame.time.Clock()
        width, height = 640, 480
        self.screen = pygame.display.set_mode((width, height))


    def init(self):
        '''Return init string with rangefinder angles'''
        self.angles = [0 for x in range(19)]

        for i in range(5):
            self.angles[i] = -90 + i * 15
            self.angles[18 - i] = 90 - i * 15

        for i in range(5, 9):
            self.angles[i] = -20 + (i - 5) * 5
            self.angles[18 - i] = 20 - (i - 5) * 5
        pygame.init()
        self.fps = 60
        self.fpsClock = pygame.time.Clock()
        width, height = 640, 480
        screen = pygame.display.set_mode((width, height))

        return self.parser.stringify({'init': self.angles})

    def drive(self, msg):
        self.screen.fill((20, 20, 20))
        steerkey=0
        gearkey=0
        racekey=0

        keys = key.get_pressed()
        if keys[K_DOWN]:
            racekey = "s"
        if keys[K_UP]:
            racekey = "w"
        if keys[K_LEFT]:
            steerkey = "a"
        if keys[K_RIGHT]:
            steerkey = "d"
        if keys[K_u]:
            gearkey="u"
        if keys[K_j]:
            gearkey="j"
        for e in event.get():
            pass


        # print("Steer:"+str(steerkey))
        # print("Gear:"+str(gearkey))
        # print("Race:"+str(racekey))

        self.state.setFromMsg(msg)

        speed = self.state.getSpeedX()
        accel = self.control.getAccel()

        self.storingData = msg
        #self.steer(steerkey)
        #self.gear(gearkey)
        #self.speed(racekey)

        pickled_model = pickle.load(open('model2.pkl', 'rb'))

        str = self.state.getTrack()

        key_stroke = [[self.state.getGear(), self.state.getAngle(), self.state.getCurLapTime(), self.state.getDistFromStart(),
             self.state.getDistRaced(), self.state.lastLapTime, self.state.getRacePos(), self.state.getRpm(),
             self.state.getSpeedX(), self.state.getSpeedY(), self.state.getSpeedZ(), self.state.getTrackPos(),
             str[0], str[1], str[2], str[3], str[4], str[5], str[6], str[7], str[8], str[9], str[10], str[11], str[12],
             str[13], str[14], str[15], str[16], str[17], str[18]]]

        #l1 = self.state.getTrack()
        #print(type(l1))

        #print(key_stroke)
        prediction = pickled_model.predict(key_stroke)
        #print(type(prediction))

        predicted_arr = prediction.tolist()

        predicted_arr1= []
        predicted_arr1.append(predicted_arr[0][0])
        predicted_arr1.append(predicted_arr[0][1])
        predicted_arr1.append(predicted_arr[0][2])

        self.control.setAccel(predicted_arr1[0])
        self.control.setSteer(predicted_arr1[1])
        self.control.setBrake(predicted_arr1[2])
        self.gear()


        #if prediction=='None':
            #racekey ='w'
        #self.speed(racekey)




        #self.state.store('Dataset.csv', steerkey,gearkey,racekey)
        return self.control.toMsg()

    def steer(self,key):
        angle = self.state.angle
        dist = self.state.trackPos
        steervalue=0

        if key == "a":
            steervalue =1


        elif key == "d":
            steervalue =-1


        else:
            if steervalue > 0:
               steervalue -= 0.1
            elif steervalue < 0:
                steervalue += 0.1

        self.control.setSteer(steervalue)
        #self.control.setSteer(((angle - dist * 0.5) / self.steer_lock) + self.steer_value)


    def gear(self):
        '''
        rpm = self.state.getRpm()
        gear = self.state.getGear()
        speed = self.state.getSpeedX()
        # print("Current Gear:"+str(gear))

        if key == "u":
            if gear < 6:
                gear += 1
        elif key == "j" :
            if gear > -1:
                gear -= 1

        self.control.setGear(gear)
        '''

        rpm = self.state.getRpm()
        gear = self.state.getGear()

        if self.prev_rpm == None:
            up = True
        else:
            if (self.prev_rpm - rpm) < 0:
                up = True
            else:
                up = False

        if up and rpm > 7000:
            gear += 1

        if not up and rpm < 3000:
            gear -= 1

        self.control.setGear(gear)
        
    def speed(self,key):
        
        speed = self.state.getSpeedX()
        accel = self.control.getAccel()

        angle = self.state.angle
        dist = self.state.trackPos

        if key == "w":
            print("go up")
            self.control.setBrake(0)
            accel +=0.5
            if accel > 1:
                accel = 1.0
        elif key == "s":
            accel = 0
            self.control.setBrake(1)
            #self.control.setSteer(((angle - dist * 0.5) / self.steer_lock) + self.steer_value)

        else:
            self.control.setBrake(0)
            accel=0

        self.control.setAccel(accel)

    def onShutDown(self):
        pass

    def onRestart(self):
        pass