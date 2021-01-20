# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 15:45:35 2020

@author: swetu
"""

""" 
Swetul Patel  7802010
COMP 4300 Assignment 3 Part A
FALL 2020
Instructor: Michael Zapp

Purpose: Simulating a Reverse Path Forwarding algorithm for Source-Based tree broadcast routing

"""
import simpy
from scipy.stats import poisson


  
#each key in the dictionaries below is the router number
RouterStats = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
RouterMsgStats = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}

msgComplete = 0
MEAN = 20
NUM_MESSAGES = 10
REPLICATIONS = 1
Experiment = False




class link(object):
    """
    Link object is a shared connection with a resource that can be used to mimic a medium of transmission between two routers
    
    """
    def __init__(self,env,r1,r2,cost,num):
        self.env = env
        self.linkNum = num
        self.wire = simpy.Resource(env, capacity=1)
        self.cost = cost
        self.routers = [r1,r2]
    
    
        
    def findSharedRouter(self, current):
        """
        Since two routers share a link, the routers attribute, stores the number of the two routers.
        This function is used to ensure a router that wants to use this link knows which router it is shared with
        
        current - the router number that is currently making the request
    
        """
        for i in self.routers:
            if i != current:
                return i
    
    def transmitONlink(self, source, dest, msg):
        """
        Since Links is shared object it can access the destination router's queue function to simulate a "transmission" from
        source router to destination router.
        This process will yield if it has to wait for the link to be free or if it needs to block the connection to prevent collisions
        
        
        """
        with self.wire.request() as req:
            yield req
            # print("Time {}: Sending Msg {} from R{} to R{} origin {} count{}".format(self.env.now, msg.msgNum,source, dest, msg.Rnum, msg.msgCount))
            yield self.env.timeout(self.cost)
            global Network
            self.env.process(Network[dest].router_queue(msg, -1, source))




class Message(object):
    """
    A message object that can be passed along to other routers
    
    Rnum - router number that the message originated from
    msgNum - sequence number of message for a given router
    """
    def __init__(self, env, number,no):
        self.Rnum = number
        self.msgNum = no
        self.creation_time = env.now
        self.msgCount = 0
        

class Router(object):
    """
    A router receives messages based on a random distribution.
    Each messgae arrives at the router through a shared link with other routers or "from the hosts connected to it"(In this case,
    we will just mimic that by calling the function generate arrivals. 
    """

    def __init__(self, env, number, RT, links):
        # key attributes
        self.env = env
        self.number = number
        self.tableR = RT
        self.links = links
        self.transmitQ = simpy.PriorityResource(self.env, capacity=1)
        self.messageCounter = self.createMsgStorage()

        self.env.process(self.generate_arrivals())
        

    def createMsgStorage(self):
        """
        This function creates and returns a dictionary whose keys are the message number of each message 
        so we can keep track of how many routers each message has visited.
    
        """
        counter = {}
        for i in range(NUM_MESSAGES):
            counter[i] = 0
        return counter

    def generate_arrivals(self):
        """
        Generates Frames for a router using the poission distribution with mean 20

        """
        msg = 0
        
        while True:
   
            dist = poisson.rvs(MEAN, size=1)
            interT = dist[0]
            # yield station for interT time
            yield self.env.timeout(interT)
            #print("Time: {} -> Message created at R{} MSG {}".format(self.env.now, self.number,msg))
            
            self.env.process(self.router_queue(Message(self.env,self.number, msg), 2, self.number))
            msg = msg + 1
            
            if msg == NUM_MESSAGES:
                break
            
    
    def router_queue(self, msg, Spriority, origin):
        """
        Function that holds messages that need to be broadcasted. Any router can invoke this function through a shared link.
        If  there is no shared link, no access to the router queue. Messages are also ignoredhere. If they are not meant to be broadcasted
        because of the rules imposed by the RPF algorithm. 
        
        msg - the message to broadcast
        Spriority - priority the message assumes while waiting in the priority queue. 
        origin - the router that message is received from. If the message is local, the number is its own router number   
        """ 
        #check for availability in transmit Queue
        # if origin != self.number:
        #     print("Time {}: Arrival Msg {} from R{} at R{} origin {}".format(self.env.now, msg.msgNum,origin, self.number, msg.Rnum))
        
        #if message is on shortest path or if it is an internal message then broadcast
        if self.tableR[msg.Rnum] == origin or origin == self.number:
            
            with self.transmitQ.request(priority=Spriority) as req:
                yield req
                
                self.router_broadcast(msg, origin)
                    
        # else:
        #     print("Time: {} -> Message {} ignored at R{}  from origin{}".format(self.env.now, msg.msgNum,self.number,msg.Rnum))
                
                
                
    def router_broadcast(self, msg, origin):
        """
        Function broadcast message on all outgoing links
        
        msg - the message to broadcast
        origin - the router that message is received from. If the message is local, the number is its own router number
        
            
        """
        #sending self message out
        if origin == self.number:
            msg.creation_time = self.env.now
            # print("Time: {} -> Message {} broadcasted at R{}".format(self.env.now, msg.msgNum,self.number))
            for link in self.links:
                dest = link.findSharedRouter(self.number)
                self.env.process(link.transmitONlink(self.number, dest, msg))
                
        #sending message that arrived from the network
        else:
            #message from another router
            plus = Network[msg.Rnum].messageCounter[msg.msgNum] + 1
            Network[msg.Rnum].messageCounter[msg.msgNum] = plus
            #if message has hhit all routers
            if plus == 9:
                # print("Time: {} -> Message {} COMPLETED for R{} creation {}".format(self.env.now, msg.msgNum,msg.Rnum, msg.creation_time))
                routerStats(msg, (self.env.now - msg.creation_time))
                
            #go through all links and broadcast
            
            for link in self.links:
                
                if origin not in link.routers:
                    dest = link.findSharedRouter(self.number)
                    self.env.process(link.transmitONlink(self.number, dest, msg))
                    
       

def routerStats(ms,tx):
    """
    Function dynamically records stats of messages that have been to all the routers( i.e successful broadcast)
    ms - the message that was broadcasted
    tx - the time from initial transmission to successful arrival at all routers

    """
     
    RouterMsgStats[ms.Rnum] = RouterMsgStats[ms.Rnum] + 1
    RouterStats[ms.Rnum] = RouterStats[ms.Rnum] + tx

    global msgComplete
    msgComplete = msgComplete +1
    


# below is the routing table for each router
# to understand. if tableR2[7] = 4, means to go from R2 -> R7, the shortest out going link for R2 is a shared link with R4
# -1 implies itself, any number 0-9 is the router number with current outgoing link
#routerN= [R0,R1,R2,R3,R4,R5,R6,R7,R8,R9]
tableR0 = [-1, 8, 8, 8, 8, 6, 6, 8, 8, 9]
tableR1 = [3, -1, 3, 3, 4, 3, 3, 3, 3, 3]
tableR2 = [3, 3, -1, 3, 3, 5, 5, 3, 3, 5]
tableR3 = [7, 1, 2, -1, 4, 2, 7, 7, 7, 7]
tableR4 = [3, 1, 3, 3, -1, 3, 3, 3, 3, 3]
tableR5 = [6, 2, 2, 2, 2, -1, 6, 6, 6, 6]
tableR6 = [0, 7, 5, 7, 7, 5, -1, 7, 7, 9]
tableR7 = [8, 3, 3, 3, 3, 6, 6, -1, 8, 6]
tableR8 = [0, 7, 7, 7, 7, 7, 7, 7, -1, 0]
tableR9 = [0, 6, 6, 6, 6, 6, 6, 6, 0, -1]





Network = {}

if __name__=='__main__':
    env = simpy.Environment()
    
    #LinkX = link(env,Rs,Rd,cost,linkNumber)    #connects Rs and Rd
    Link1 = link(env,0,9,3,1)       #connects R0 and R9
    Link2 = link(env,0,6,4,2)       #connects R0 and R6
    Link3 = link(env,0,8,2,3)       #connects R0 and R8
    Link4 = link(env,6,9,2,4)       #connects R6 and R9
    Link5 = link(env,6,8,6,5)       #connects R6 and R8
    Link6 = link(env,6,7,3,6)       #connects R6 and R7
    Link7 = link(env,7,8,1,7)       #connects R7 and R8
    Link8 = link(env,6,5,5,8)       #connects R6 and R5
    Link9 = link(env,2,5,3,9)       #connects R5 and R2
    Link10 = link(env,1,3,1,10)     #connects R1 and R3
    Link11 = link(env,1,4,2,11)     #connects R1 and R4
    Link12 = link(env,3,4,3,12)     #connects R3 and R4
    Link13 = link(env,2,3,4,13)     #connects R3 and R2
    Link14 = link(env,3,7,2,14)     #connects R3 and R7
     
     
    #A list of link objects for each router
    LinksR0 = [Link1, Link2, Link3]
    LinksR1 = [Link10, Link11]
    LinksR2 = [Link9, Link13]
    LinksR3 = [Link10, Link12, Link13, Link14]
    LinksR4 = [Link11, Link12]
    LinksR5 = [Link8, Link9]
    LinksR6 = [Link2, Link4, Link5, Link6,Link8]
    LinksR7 = [Link6, Link7, Link14]
    LinksR8 = [Link3, Link5, Link7]
    LinksR9 = [Link1, Link4]
    
    
    LinksR = [LinksR0,LinksR1,LinksR2,LinksR3,LinksR4,LinksR5,LinksR6,LinksR7,LinksR8,LinksR9]
    TableR = [tableR0, tableR1,tableR2,tableR3,tableR4,tableR5,tableR6,tableR7,tableR8,tableR9]
    
    if not Experiment: 
        for i in range(10):
            Network[i] = Router(env, i, TableR[i], LinksR[i])
    
        env.run()
        totalTX = 0
        for i in RouterStats.keys():
            if i != -1:
                totalTX = totalTX + RouterStats[i]
                print("\nRouter {} Total Tx time: {} and Mean Tx time: {}".format(i, RouterStats[i],RouterStats[i]/NUM_MESSAGES))
           
        print("\nUnique messages sent: {}\n".format(msgComplete))
    
        print("Overall System Mean transmit time for a message: {}\n".format(totalTX/msgComplete))
    
    else: #experiment MODE
        for c in range(REPLICATIONS):
            
            totalTX = 0
            Network = {}
            RouterStats = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
            RouterMsgStats = {0:0, 1:0, 2:0, 3:0, 4:0, 5:0, 6:0, 7:0, 8:0, 9:0}
            msgComplete = 0
            
            for i in range(10):
                Network[i] = Router(env, i, TableR[i], LinksR[i])
            
            env.run()
            for j in RouterStats.keys():
                if j != -1:
                    totalTX = totalTX + RouterStats[j]
        
            print("Replication {}: Overall System Mean transmit time: {}".format(c, totalTX/msgComplete))
     
# END of Program
