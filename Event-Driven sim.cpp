//-----------------------------------------
// NAME	: SWETUL PATEL
//
// REMARKS: CONDUCT AN EVENT DRIVEN SIMULATION
//
//
//-----------------------------------------

#include <iostream>
#include <cstring>
#include <fstream>
#include <stdlib.h>
#include <string>
using namespace std;

//------------------
//	INTERFACES
//__________________

//CLASS NODE
class Node{
	private:
		int CustID;
		int arrivalTime;
		int smallItems;
		int bigItems;
		int Forv;
		int Coupons;
		Node* next;

	public:
		//MUTATOR METHODS
		void setNext(Node* next);
		void setSmall(int small);
		void setBig(int big);
		void setForv(int amount);
		void setCoupons(int num);
		//Accessors
		Node* getNext();
		int getTotalTime();
		int getTotalItems();
		int getSmall();
		int getCoupons();
		int getBig();
		int getForv();
		int getArrTime();

		Node(int ID, int ArrTime);
		Node(const Node& a);
		Node();
		//Destructor
		virtual ~Node();
};
//CLASS CUTSOMER
class Customer{
	private:
		int CustID;
		int time;
		string type;
		Node* info;
		string Lane;
		int wait;
		Customer* next;
	public:
		//Accessors
		void print();
		int getCustID();
		int getTime();
		string getType();
		Customer* getNext();
		//MUTATOR METHODS
		void setNext(Customer* next);
		//CONSTRUCTORS
		Customer();
		Customer(int time, int ID, string type, Node* info, string Lane, int wait);
		//Destructor
		virtual ~Customer();
};
//CLASS EVENTQUEUE
class EventQueue{
	private:
		Customer* first;
		int totalServ;
		int totalWait;
	public:
		void insert(Customer* newCust);
		//Accessors
		int getServiceTime();
		int getWaitTime();
		//MUTATOR METHODS
		void incrService(int amount);
		void incrTime(int amount);
		void print();
		//CONSTRUCTORS
		EventQueue();
		//Destructor
		virtual ~EventQueue();

};
//CLASS PRIOROTYQUEUE
class PriorityQueue{
	private:
		Node* first;

	public:
		void insert(Node* newNode);
		//Accessors
		void removeNextCust();
		Node* getFirst();
		void print();
		//CONSTRUCTORS
		PriorityQueue();	//Constructor
		//Destructor
		virtual ~PriorityQueue();
};
//CLASS CHECKOUTS
class CheckOuts{
	public:
		//Accessors
		virtual void insert(Node* newNode);
		virtual bool simEvent();
		virtual void setLaneTime(int time, string lane);
		virtual int getLaneEndTime(string Lane);
		virtual void remove(string Lane);
		//Destructor
		~CheckOuts();


};
//CLASS EXPLANE
class ExpLane: public CheckOuts{
	private:
		PriorityQueue express;
		PriorityQueue regular;
		int expEndTime;
		int regEndTIme;

	public:
		void insert(Node* newNode);
		bool simEvent();
		//Accessors
		int getExpEndTime();
		int getRegEndTime();
		int getLaneEndTime(string Lane);
		//MUTATOR METHODS
		void setExpEndTime(int time);
		void setRegEndTime(int time);
		void setLaneTime(int time, string Lane);
		void remove(string Lane);
		//CONSTRUCTORS
		ExpLane();
		//Destructor
		virtual ~ExpLane();
};
//CLASS WAITLANE
class WaitLane: public CheckOuts{
	private:
		PriorityQueue regular;
		int laneOneTime;
		int laneTwoTime;

	public:
		void insert(Node* NewNode);
		//Accessors
		bool simEvent();
		bool getLaneOneTime();
		bool getLaneTwoTime();
		//MUTATOR METHODS
		void setLaneOneTime(int state);
		void setLaneTwoTime(int state);
		void setLaneTime(int time, string Lane);
		void remove(string lane);
		//CONSTRUCTORS
		WaitLane();
		//Destructor
		virtual ~WaitLane();
};




//=-------------------------------------------------
//
//
//--------------------------------------------------

//##	CLASS NODE 	##
//CONSTRUCTORS
Node::Node(int ID, int ArrTime)
{
	this->CustID = ID;
	this->arrivalTime = ArrTime;
	this->next = NULL;
	this->Coupons = 0;
	this->Forv = 0;
	this->smallItems = 0;
	this->bigItems = 0;
}
Node::Node(){}
Node::Node(const Node& a)
{
	CustID = a.CustID;
	arrivalTime = a.arrivalTime;
	next = a.next;
	Coupons = a.Coupons;
	Forv = a.Forv;
	smallItems = a.smallItems;
	bigItems = a.bigItems;
}

//MUTATOR METHODS
void Node::setNext(Node* next){this->next = next;}
void Node::setSmall(int small){this->smallItems = small;}
void Node::setBig(int big){this->bigItems = big;}
void Node::setForv(int amount){this->Forv = amount;}
void Node::setCoupons(int num){this->Coupons = num;}
//Accessors
Node* Node::getNext(){return next;}
int Node::getSmall(){return smallItems;}
int Node::getBig(){return bigItems;}
int Node::getForv(){return Forv;}
int Node::getCoupons(){return Coupons;}
int Node::getTotalTime()
{
	return (smallItems) + (bigItems*2) + (Forv * 4) + (Coupons*5);
}
int Node::getArrTime(){return arrivalTime;}
int Node::getTotalItems()
{
	return (smallItems + bigItems + Forv);
}
//Destructor
Node::~Node(){}

//##	CLASS CUSTOMER 	##
//CONSTRUCTORS
Customer::Customer()
{
	time=0;
	CustID = 0;
	type = "UNKNOWN";
	Lane = "UNKNOWN";
	wait = 0;
}

Customer::Customer(int time, int ID, string type, Node* info, string Lane, int wait)
{
	this->time = time;
	this->CustID = ID;
	this->type = type;
	this->info = info;
	this->Lane = Lane;
	this->wait = wait;
	this->next = NULL;
}
//Accessors
int Customer::getCustID(){return CustID;}
string Customer::getType(){return type;}
int Customer::getTime(){return time;}
Customer* Customer::getNext(){return next;}
//MUTATOR METHODS
void Customer::setNext(Customer* next){this->next = next;}

void Customer::print()
{

	cout << "Time " << time <<" Customer " << CustID;
	if(type == "arrive")
	{
		cout <<" arrives: ";
		if(info->getSmall() != 0)
		{
			cout << " SMALL "<< (info->getSmall)();
		}
		if(info->getBig() != 0)
		{
			cout << " BIG "<< info->getBig();
		}
		if(info->getForv() != 0)
		{
			cout << " Forv " << info->getForv();
		}
		if(info->getCoupons() != 0)
		{
			cout << " Coupons " << info->getCoupons();
		}

		cout <<" Service time: ";
		cout << info->getTotalTime() <<endl;
	}
	else if(type == "begin")
	{
		cout << " begins Service in " <<Lane << " lane"<<endl;
	}
	else
	{
		cout << " completes service in " << Lane << " lane. Arrival: "<< info->getArrTime() << "complete: "<< time <<" wait: "<< wait <<endl;
	}
}
//Destructor
Customer::~Customer(){}

//##	CLASS EVENTQUEUE 	##
//CONSTRUCTORS
EventQueue::EventQueue(){this->first = NULL; this->totalServ = 0; this->totalWait = 0;}
//MUTATOR METHODS
void EventQueue::incrService(int amount){totalServ += amount;}
void EventQueue::incrTime(int amount){totalWait += amount;}
void EventQueue::insert(Customer* newCust)
{
	Customer* current = first;
	if(current == NULL)
	{
		first = newCust;
	}
	else
	{
		while(current != NULL)
		{
			if(current->getNext() == NULL)
			{
				current->setNext(newCust);
				break;
			}
			else
			{
				int tempTime = current->getNext()->getTime();
				if(tempTime > newCust->getTime())
				{
					newCust->setNext(current->getNext());
					current->setNext(newCust);
					break;
				}
				else if(tempTime == newCust->getTime())
				{
					int tempID = current->getNext()->getCustID();
					if(tempID > newCust->getCustID())
					{
						newCust->setNext(current->getNext());
						current->setNext(newCust);
						break;
					}
				}
			}
			current = current->getNext();
		}
	}
}
//Accessors
int EventQueue::getServiceTime(){return totalServ;}
int EventQueue::getWaitTime(){return totalWait;}
void EventQueue::print()
{
	Customer* current = first;
	while(current != NULL)
	{
		current->print();
		current = current->getNext();
	}
}
//Destructor
EventQueue::~EventQueue(){}


//##	CLASS CHECKOUTS 	##
int CheckOuts::getLaneEndTime(string Lane){ return 0;}
void CheckOuts::setLaneTime(int time, string lane){}
void CheckOuts::insert(Node* newNode){}
void CheckOuts::remove(string Lane){}
bool CheckOuts::simEvent(){return true;}
//Destructor
CheckOuts::~CheckOuts(){}


//##	CLASS EXPLANE 	##
//CONSTRUCTORS
ExpLane::ExpLane()
{
	this->express = PriorityQueue();
	this->regular = PriorityQueue();
	this->expEndTime = 0;
	this->regEndTIme = 0;
}
void ExpLane::insert(Node* newNode)
{
	if(newNode->getTotalItems() <= 12)
	{
		express.insert(newNode);
	}
	else
	{
		regular.insert(newNode);
	}
}

bool ExpLane::simEvent()
{
	if(express.getFirst() != NULL){
		return true;
	}
	else if(regular.getFirst() != NULL)
	{
		return true;
	}
	else
		{return false;}
}
//Accessors
int ExpLane::getExpEndTime(){return expEndTime;}
int ExpLane::getRegEndTime(){return regEndTIme;}
int ExpLane::getLaneEndTime(string Lane)
{
	if(Lane == "express")
	{
		return getExpEndTime();
	}
	else
	{
		return getRegEndTime();
	}
}
//MUTATOR METHODS
void ExpLane::setExpEndTime(int time){ expEndTime = time;}
void ExpLane::setRegEndTime(int time){ regEndTIme = time;}
void ExpLane::setLaneTime(int time, string Lane)
{
	if(Lane == "express")
	{
		setExpEndTime(time);
	}
	else
	{
		setRegEndTime(time);
	}
}
void ExpLane::remove(string Lane)
{
	if(Lane == "regular")
	{
		regular.removeNextCust();
	}
	else
	{
		express.removeNextCust();
	}
}
//Destructor
ExpLane::~ExpLane(){}

//##	CLASS WAITLANE 	##
//CONSTRUCTORS
WaitLane::WaitLane(){this->regular = PriorityQueue(); this->laneOneTime = 0; this->laneTwoTime = 0;}

void WaitLane::insert(Node* newNode)
{
	regular.insert(newNode);
}
bool WaitLane::simEvent()
{
	if(regular.getFirst() != NULL)
	{
		return true;
	}
	else
	{
		return false;
	}
}
//Accessors
bool WaitLane::getLaneTwoTime(){return laneTwoTime;}
bool WaitLane::getLaneOneTime(){return laneOneTime;}
//MUTATOR METHODS
void WaitLane::setLaneTwoTime(int state){this->laneOneTime = state;}
void WaitLane::setLaneOneTime(int state){this->laneTwoTime = state;}
void WaitLane::setLaneTime(int time, string Lane)
{
	if(Lane == "1st")
	{
		setLaneOneTime(time);
	}
	else
	{
		setLaneTwoTime(time);
	}
}
void WaitLane::remove(string lane)
{
	regular.removeNextCust();
}
//Destructor
WaitLane::~WaitLane(){}

//##	CLASS PRIORITYQUEUE 	##
//##	CLASS CHECKOUTS 	##
PriorityQueue::PriorityQueue(){first = NULL;}
void PriorityQueue::insert(Node* newNode)
{
	if(first == NULL)
	{
		first = newNode;
	}
	else
	{
		Node* curr = first;
		while(curr != NULL)
		{
			if(curr->getNext() == NULL)
			{
				curr->setNext(newNode);
			}
			curr = curr->getNext();
		}
	}
}
void PriorityQueue::removeNextCust()
{
	Node* temp = first;
	first = first->getNext();
	delete(temp);
}

Node* PriorityQueue::getFirst()
{
	return first;
}
//Destructor
PriorityQueue::~PriorityQueue(){}


//---------------------------------------------------------------------------------
//
//
//---------------------------------------------------------------------------------
static bool eventCheck(CheckOuts* curr){
	return true;
}
static int checkEmptyLane(int amount){
	if(amount <= 12)
	{
		return 1;
	}
	else
	{
		return 0;
	}
}
//
//	MAIN
//
int main(int argc, char** argv)
{
	EventQueue* Simulation = new EventQueue();
	double servTime = 0;
	double wait = 0;
	int custID = 1;
	int simType = atoi(argv[2]);
	ifstream file;
	file.open(argv[1]);
	string inLine;
	cout << "Simulation begins......" << endl;
	CheckOuts* openLane;
	//check event type
	if (simType == 1)
	{
		ExpLane* tempas = new ExpLane();
		openLane = dynamic_cast<CheckOuts*>(tempas);
	}
	else
	{
		WaitLane* tempas = new WaitLane();
		openLane = dynamic_cast<CheckOuts*>(tempas);
	}
	int ln1 = 0;
	int ln2 = 0;
	//read input and process
	while(getline(file, inLine))
	{
		char* current = new char[inLine.length() + 1];
		strcpy(current, inLine.c_str());
		char* temp;
		temp = strtok(current, " ");
		int initTime;
		initTime = atoi(temp);
		Node* newNode = new Node(custID, initTime);
		Node a = *newNode;
		//add corresponding cart items
		while(temp != NULL)
		{
			if(strcmp(temp, "SMALL") == 0)
			{
				temp = strtok(NULL, " ");
				newNode->setSmall(atoi(temp));
			}
			else if(strcmp(temp, "BIG") == 0)
			{
				temp = strtok(NULL, " ");
				newNode->setBig(atoi(temp));
			}
			else if(strcmp(temp, "FORV") == 0)
			{
				temp = strtok(NULL, " ");
				newNode->setForv(atoi(temp));
			}
			else if(strcmp(temp, "COUPON") == 0)
			{
				temp = strtok(NULL, " ");

				newNode->setCoupons(atoi(temp));

			}
			else
			{
				temp = strtok(NULL, " ");
			}

		}
		//event Arrive
		string type = "arrive";
		Customer* newCust = new Customer(initTime, custID, type,newNode, type, 0);
		openLane->insert(newNode);
		Simulation->insert(newCust);
		//check for lane type
		if(eventCheck(openLane))
		{
			if(simType == 1)
			{
				string Lane;
				int beginTime;
				int waitTime;
				if(checkEmptyLane(newNode->getTotalItems()) == 1)
				{
					Lane = "express";
					if(ln1 == 0||initTime > openLane->getLaneEndTime(Lane))
					{
						openLane->setLaneTime(initTime, Lane);
						beginTime = openLane->getLaneEndTime(Lane);
						waitTime = 0;
						ln1++;
					}
					else
					{
						beginTime = openLane->getLaneEndTime(Lane);
						waitTime = beginTime - initTime;
					}
				}
				else
				{
					Lane = "regular";
					if(ln2 == 0||initTime > openLane->getLaneEndTime(Lane))
					{
						openLane->setLaneTime(initTime, Lane);
						beginTime = openLane->getLaneEndTime(Lane);
						waitTime = 0;
						ln2++;
					}
					else
					{
						beginTime = openLane->getLaneEndTime(Lane);
						waitTime = beginTime - initTime;
					}

				}

				//begin event
				type = "begin";
				Customer* beginCust = new Customer(beginTime, custID, type, newNode, Lane, waitTime);
				Simulation->insert(beginCust);
				int endTime;
				endTime = beginTime + newNode->getTotalTime();

				//end event
				type = "end";
				openLane->setLaneTime(endTime, Lane);
				Customer* endCust = new Customer(endTime, custID, type, newNode, Lane, waitTime);
				servTime += (endTime - beginTime);
				wait += waitTime;
				Simulation->insert(endCust);
				openLane->remove(Lane);
			}
			else
			{
				//simulation type 2
				string Lane;
				string str1 = "1st";
				string str2 = "2nd";

				int lane1 = openLane->getLaneEndTime(str1);
				int lane2 = openLane->getLaneEndTime(str2);
				if(lane1 <= initTime)
				{
					Lane = "1st";
				}
				else if(lane2 <= initTime)
				{
					Lane = "2nd";
				}
				else if(lane1 > lane2)
				{
					Lane = "2nd";
				}
				else
				{
					Lane = "1st";
				}
				if(custID == 1)
				{
					openLane->setLaneTime(initTime, Lane);
				}

				int beginTime = openLane->getLaneEndTime(Lane);
				int waitTime;
				if(beginTime > initTime)
				{
					waitTime = beginTime - initTime;
				}
				else
				{
					waitTime = 0;
				}

				Simulation->incrTime(waitTime);
				Customer* beginCust = new Customer(beginTime, custID, "begin", newNode, Lane, waitTime);
				Simulation->insert(beginCust);
				Simulation->incrService(newNode->getTotalTime());
				int endTime = beginTime + newNode->getTotalTime();
				Customer* endCust = new Customer(endTime, custID, "end", newNode, Lane, waitTime);
				Simulation->insert(endCust);
				openLane->setLaneTime(endTime, Lane);
				openLane->remove(Lane);
				servTime += (endTime - beginTime);
				wait += waitTime;
			}
		}
		custID++;
	}

	file.close();
	Simulation->print();
	cout << "Simulation Ended." <<endl;
	cout << "###### SUMMARY ######" <<endl;
	cout << "- Total Number of customers : "<< custID-1 <<endl;

	cout << "- Service time: total = "<< servTime << ", average = " << (servTime /(custID-1)) << endl;

	cout << "- Waiting time: total = "<< wait << ", average = " << (wait/(custID-1)) <<endl;
	return 0;
}
