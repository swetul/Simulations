# Simulations

In this repository are simulations for networking and Event based algorithms.

## 1. Aloha broadcast system (Aloha sim.py)

- In this simulation, the goal was to understand the impact of congestion on a single medium of communication on the overall network performance.
- Aloha broadcast system involves use of radio communications on a fixed frequency. Therefore collisions in transmission often affect network performance as colliding transmittors often have to retransmit
- This simulation involved testing different implementations of avoidance and back-off delays to improve overall network performance.
- This mini project involved using simpy and scipy libraries to run the simulations and do statistical analysis.
- Note: the theoratical maximum performance from the aloha system is 18%, however simulations showed that a 10% netowrk performance can be acheived with strict protocols.

## 2. Packet routing simulation (Packet routing sim.py)

- In this simulation, the goal was to understand how congestion and network implementation affects the overall packet transmission time i.e the moment it is sent by a router to all routers successfully receiving the message.
- This mini project involved using simpy and scipy libraries to run the simulations and do statistical analysis.
- Reverse Path forwarding algorithm was implemented to run this simulation based on a static network configuration (Network.JPG in repository)
- Experiments were conducted to determine factors that affect over performance. some factors identified included Bandwidth, transmission rate, number of routers, cost of each connection, among others.

## 3. Check-out simulation (Event-Driven sim.cpp)

- In this simulation, the goal was to use Object-Oriented programming and its principles to simulate a check-out system at a business.
- The simulation was primarily an event based system, where events that occured included arrival, wait and departure events.
- factors such as number of lanes, number of customers, size of shopping cart, average scan times were adjusted to view the impact of individual or correlated factors on average checkout time for a customer.
