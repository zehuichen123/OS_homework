from django.db import models
import time
# Create your models here.

class Request(object):
    def __init__(self, request_stair,direction):
        # the request stair number
        self.request_stair = request_stair
        # -1 down 1 up
        self.direction = direction

class Passenger(object):
    def __init__(self,destination):
        # passenger's 
        self.destination=destination

class Elavator(object):
    def __init__(self):
        self.curr_stair=1
        # elavator current state 0 idle, 1 up, -1 down
        self.curr_direction=0
        # elavator now task
        self.curr_getting=None
        # the furtherest destination of passenger in this elevator
        self.further_passenger=None
        # all passengers currently in this elevator
        self.passenger_list=[]
        # new passenger request for his destination
        self.new_passenger_destination=1
        # current request that elevator is processing
        self.curr_process_req=None
        self.door_open=0

    # get the current direction of elevator based on 
    # the curr_getting or passenger in the elevator
    def get_direction(self,task_destination):
        if task_destination>self.curr_stair:
            self.curr_direction=1
            
        elif task_destination==self.curr_stair:
            self.curr_direction=0

        else:
            self.curr_direction=-1


    def check_passenger_down(self):
        # if further_passenger in the elevator reach its destination
        if self.further_passenger.destination==self.curr_stair:
            # let this passenger down
            self.further_passenger=None
            self.new_passenger_destination=1
            return
        # tranverse the whole passenger_list to check if there is 
        # any passenger reach its destination
        for each_passenger in self.passenger_list:
            if each_passenger.destination==self.curr_stair:
                self.passenger_list.remove(each_passenger)
        return

    def recheck_direction(self):
        # redirect the elevator direction
        if self.further_passenger!=None:
            if self.further_passenger.destination>self.curr_stair:
                self.curr_direction=1
                print('recheck direction to 1')
            elif self.further_passenger.destination<self.curr_stair:
                self.curr_direction=-1
                print('recheck direction to -1')
            else:
                self.curr_direction=0
                print('recheck direction to 0')

    def check_passenger_up(self,request_queue):
        queue_list=[]
        # check if getting someone up
        #print('-------')
        #print("check passenger up at stair "+str(self.curr_stair))
        #print(request_queue.empty())
        if self.curr_getting!=None:
            if self.curr_getting.request_stair==self.curr_stair:
                self.curr_process_req=self.curr_getting
                self.door_open=1
                time.sleep(3)
                self.door_open=0
                self.curr_getting=None
                new_passenger_destination=self.new_passenger_destination
                new_passenger=Passenger(new_passenger_destination)
                # if there's no passenger before,
                # just add new passenger to further_passenger
                if self.further_passenger==None:
                    self.further_passenger=new_passenger
                # if new passenger destination > curr passenger destination, 
                # update further_passenger state
                elif abs(new_passenger_destination-self.curr_direction)\
                    >abs(self.further_passenger.destination-self.curr_direction):
                    self.passenger_list.append(self.further_passenger)
                    self.further_passenger=new_passenger
                # if new passenger destination < curr passenger destination,
                # add it to passenger_list
                elif abs(new_passenger_destination-self.curr_direction)\
                    <abs(self.further_passenger.destination-self.curr_direction):
                    self.passenger_list.append(new_passenger)
                # if new passenger's destination is same as another
                # passenger before, just merge them(do nothing).
                else:
                    pass

                self.recheck_direction()
                return

        # check all requests in the request_list
        while(not request_queue.empty()):
            request_item=request_queue.get()
            print("GET REQUEST:  "+str(request_item.request_stair))
            # if the request meets the requirement of curr 
            # elavator state, get it into elavator.
            if request_item.request_stair==self.curr_stair\
                and request_item.direction==self.curr_direction:
                # passenger can be picked up
                self.curr_process_req=request_item
                self.door_open=1
                time.sleep(3)
                self.door_open=0
                new_passenger_destination=self.new_passenger_destination
                new_passenger=Passenger(new_passenger_destination)
                # if there's no passenger before,
                # just add new passenger to further_passenger
                if self.further_passenger==None:
                    self.further_passenger=new_passenger
                # if new passenger destination > curr passenger destination, 
                # update further_passenger state
                elif abs(new_passenger_destination-self.curr_direction)\
                    >abs(self.further_passenger.destination-self.curr_direction):
                    self.passenger_list.append(self.further_passenger)
                    self.further_passenger=new_passenger
                # if new passenger destination < curr passenger destination,
                # add it to passenger_list
                elif abs(new_passenger_destination-self.curr_direction)\
                    <abs(self.further_passenger.destination-self.curr_direction):
                    self.passenger_list.append(new_passenger)
                # if new passenger's destination is same as another
                # passenger before, just merge them(do nothing).
                else:
                    pass
            else:
                queue_list.append(request_item)
        # for those requests not be accepted
        # put them back to request_queue
        self.recheck_direction()
        for remain_request in queue_list:
            request_queue.put(remain_request)
        #print("End checking passenger up at stair "+str(self.curr_stair))
        #print('------')

    def update_getting(self,request_queue):
        # update elevator curr_getting based on Request from exchange_queue
        queue_list=[]
        # if there's no curr_getting with this elevator
        if self.curr_getting==None:
            self.curr_getting=request_queue.get()
            task_destination=self.curr_getting.request_stair
            self.get_direction(task_destination)
        # tranverse the whole requests in the Queue
        while(not request_queue.empty()):
            request_item=request_queue.get()
            # if the curr_direction of the elevator is same as 
            # request by users, add it to elevator passenger_list
            if self.curr_direction*request_item.request_stair\
                >self.curr_direction*self.curr_getting.request_stair:
                queue_list.append(self.curr_getting)
                self.curr_getting=request_item
            # if the curr_direction is not the same as the request, just ignore it.
            elif self.curr_direction*request_item.request_stair\
                <self.curr_direction*self.curr_getting.request_stair:
                queue_list.append(request_item)
            else:
                pass
        # put all requests that has not been receieved by elevator
        for remain_request in queue_list:
            request_queue.put(remain_request)

    # debug function to check current elevator state
    def state_check(self):
        
        print("*************")
        print("STATE CHECK")
        
        if self.further_passenger!=None:
            print('further passenger: '+str(self.further_passenger.destination))
        else:
            print("no further passenger")
        print("passenger list:")
        for i in self.passenger_list:
            print(i.destination)
        print("*************")
       
        pass

    def run(self,request_queue):
        while(True):
            self.state_check()
            if self.curr_direction!=0:
                print('current at '+str(self.curr_stair))
            # if the elevator needs to deliver any passenger
            if self.further_passenger!=None:
                task_destination=self.further_passenger.destination
                self.get_direction(task_destination)
                self.check_passenger_down()
                self.check_passenger_up(request_queue)
                self.curr_stair+=self.curr_direction
                #curr_percent=(self.curr_stair*18-9)/358
                time.sleep(1)
            else:
                # the elavator has someone to pickup
                if self.curr_getting!=None:
                    #print('has someone to pick up?')
                    task_destination=self.curr_getting.request_stair
                    self.get_direction(task_destination)
                    self.check_passenger_up(request_queue)
                    if self.further_passenger==None:
                        self.update_getting(request_queue)
                    self.curr_stair+=self.curr_direction
                    curr_percent=(self.curr_stair*18-9)/358
                    #progressbar.set_fraction(curr_percent)
                # if the elavator is idling now
                else:
                    #print('find someone to pick up')
                    self.update_getting(request_queue)
                    self.curr_stair+=self.curr_direction
                    curr_percent=(self.curr_stair*18-9)/358
                    #progressbar.set_fraction(curr_percent)
                time.sleep(1)