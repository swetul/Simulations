# -*- coding: utf-8 -*-
"""
Created on Tue Nov 10 16:41:54 2020

@author: Swetul Patel

Simulation of the ALOHA broadcast system.
"""

import simpy
import scipy as sci

runTime = 10000
numChannels = 1
interT = 2
stations = 8
poisMean = 10


class Network(object):
    """
    A Netowrk has a limited number of channels available to
    transmit frames. defualt: 1
    
    Stations wait for a channel to become available. When a channel
    is available it receives a frame from a station and waits for it
    to finish "transmit time, Tf" time units.
    
    """

    def __init__(self, env, numChannels):
        self.env = env
        self.status = 'idle'
        self.channels = simpy.Resource(env, numChannels)
        self.eventList = []
        self.Q = []
        
    def transmit(self, frame):
        yield self.env.timeout(frame.tf)
        print("Frame {} from station {} successfully transmitted".format(frame.num, frame.station))
    
    def checkCollision(transmitT, tf):
        for i in self.Q:
            if(i.)
    
    def arrival_event(self,frame,Smean):
        interT = sci.stats.poisson.rvs(frame.Pmean, size = 1)
        frame.Tf = sci.stats.expon.rvs(mean=0.5)
        self.Q.append(frame)
        self.eventList.append(Event(frame,'arrival', interT))
        
        
        
class Event(object):
    def __init__(self, frame, typee, interT):
        self.frame = frame
        self.eventTime = env.now + interT
        

class Station:
    """
    A station contains frames based on a random distribution.
    Each frame arrives at the station at a given time. 
    
    
    """
    def __init__(self,env, network, number, mean):
        self.env = env
        self.network = network
        self.number = number
        self.Pmean = mean
        self.frameList = []
    
    def generate_frame(self):
        tf = sci.stats.expon(mean=0.5)
        self.frameList.append(Frame(self.env.now, tf, self.number, env.now))
    
    def check_frame_list(self):
        if self.frameList:
            frameTosend = self.frameList[0]
        
        if(self.network.checkCollision(frameTosend.senseTime, frameTosend.tf)):
            # collision
            self.frameList[0].update_senseTime()
        else:
            self.network.arrival_event(self.frameList[0])
            self.frameList.pop(0)
    

class System(object):
    """
    A system consists on stations that are looking to transmit frames over a network which contains channels.
    
    """
    
    def __init__(self, env, network, station, mean):
        self.env = env
        self.network = Network(env, numChannels)
        self.stations = []
        for i in range(station):
            self.stations.append(Station(env,network, i, mean[0]))
            print('done')  
        

class Frame:
    def __init__(self,senseTime,tf, station, start):
        self.senseTime = senseTime
        self.tf = tf
        self.station = station
        self.start = start
    
    
    

    
    
    
def setup(env, channel, interT, station, mean):
    """
    Creates a network with "channel" number of channels and "station" number of stations in the "env" environment.
    These values can be modified at the top section of the program after the import statements
    
    """
    network = Network(env, channel)
    system = System(env, network, station, mean)
    transmitList = []
        
    while True:
        system.stations







# Set-up environment
env = simpy.Environment()
Pmean = [poisMean]
env.process(setup(env, numChannels, interT, stations, Pmean))
env.run(until=runTime)
    

    
    








