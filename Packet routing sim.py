""" 
Swetul Patel
Purpose: Simulating a Reverse Path Forwarding algorithm for Source-Based tree broadcast routing
"""
import simpy
from scipy.stats import poisson

import random


GlobalEnd = True


class link:
    def __init__(resource, router):
        self.resource = resource
        self.router = router


# receivedfrom = "R3"
# for i in linksR1:
#     if i.router1 != receivedFrom or i.router2 != receivedfrom:
#         with i.resource.request() as req
#             yield req
#             transmit


class Message:
    def __init__(self, env, number):
        self.Rnum = number
        self.creation_time = env.now
        self.transmit_time = 0
        self.end_time = 0


class Router(object):
    """
    A station receives frames based on a random distribution.
    Each frame arrives at the station at a given time. 
    """

    def __init__(self, env, neighbors, number, RT, links):
        # key attributes
        self.env = env
        self.neighbors = neighbors
        self.number = number
        self.Rtable = RT
        self.links - links

        # stats attributes
        # station resources
        self.frameList = simpy.Resource(self.env, capacity=1)
        self.arrivalQ = []
        self.transmitQ = []

        self.env.process(self.generate_arrivals())
        self.env.process(self.run_router())

    def generate_arrivals(self):
        """
        Generates Frames for a station using the poission distribution 

        """
        msg = 0
        while True:
            # get distribution value to get interT
            dist = poisson.rvs(20, size=1)
            interT = dist[0]

            # yield station for interT time
            yield self.env.timeout(interT)

            arrivalQ.append(Message(self.env, self.number))

            msg = msg + 1
            if msg == 10:
                break

    def run_router():
        while True and GlobalEnd:
            if len(self.transmitQ) != 0:
                if self.transmitQ[0].number == self.number:
                    yield self.env.process(self.broadcast(self.transmitQ.pop(0)))

    def broadcast(self, msg):

        transmitted = 0
        transmit_onLink = copy.deepcopy(self.links)
        while True:
            if len(transmit_onLink) == 0:
                break

            for i in range(len(transmit_onLink)):
                if i.resource.count() == 0:
                    with i.resource.request() as req:
                        if req:
                            print("Sending message")
                            transmit_onLink.pop(i)


# below is the routing table for each router
# to understand. if Rtable2[7] = 4, means to go from R2 -> R7, the shortest out going link for R2 is through R4
# -1 implies itself, any number 0-9 is the router number with current outgoing link
#routerN= [R0,R1,R2,R3,R4,R5,R6,R7,R8,R9]
Rtable0 = [-1, 8, 8, 8, 8, 6, 6, 8, 8, 9]
Rtable1 = [3, -1, 3, 4, 3, 3, 3, 3, 3, 3]
Rtable2 = [3, 3, -1, 3, 3, 5, 5, 4, 3, 5]
Rtable3 = [7, 1, 2, -1, 4, 2, 7, 7, 7, 7]
Rtable4 = [3, 1, 3, 3, -1, 3, 3, 3, 3, 3]
Rtable5 = [6, 2, 2, 2, 2, -1, 6, 6, 6, 6]
Rtable6 = [0, 7, 5, 7, 7, 5, -1, 7, 7, 9]
Rtable7 = [8, 3, 3, 3, 3, 6, 6, -1, 8, 6]
Rtable8 = [0, 7, 7, 7, 7, 7, 7, 7, -1, 0]
Rtable9 = [0, 6, 6, 6, 6, 6, 6, 6, 6, -1]


def runSim():

    # link resources
    c1 = simpy.Resource(env, capacity=1)
    c2 = simpy.Resource(env, capacity=1)
    c3 = simpy.Resource(env, capacity=1)
    c4 = simpy.Resource(env, capacity=1)
    c5 = simpy.Resource(env, capacity=1)
    c6 = simpy.Resource(env, capacity=1)
    c7 = simpy.Resource(env, capacity=1)
    c8 = simpy.Resource(env, capacity=1)
    c9 = simpy.Resource(env, capacity=1)
    c10 = simpy.Resource(env, capacity=1)
    c11 = simpy.Resource(env, capacity=1)
    c12 = simpy.Resource(env, capacity=1)
    c13 = simpy.Resource(env, capacity=1)
    c14 = simpy.Resource(env, capacity=1)

    LinksR0 = [link(c1, 9), link(c2, 6), link(c3, 8)]

    env = simpy.Environment()
    router = Router(env, [6, 8, 9], 0, Rtable0, LinksR0)
