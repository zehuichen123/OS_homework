#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import gi
gi.require_version('Gtk','3.0')
from gi.repository import Gtk,GObject
import random
from queue import Queue
from threading import Thread
import time

def ask_for_destination(other,arg_list):
    destination=arg_list[0]
    elevator_instance=arg_list[1]
    # if the elevator is processing elevator instance
    if elevator_instance.curr_process_req!=None:
        # if this request is up
        if elevator_instance.curr_process_req.direction==1:
            # if the passenger ask for destination higher than current stair
            if destination>elevator_instance.curr_stair:
                # receieve this passenger
                elevator_instance.new_passenger_destination=destination
        # same as the former one
        if elevator_instance.curr_process_req.direction==-1:
            if destination<elevator_instance.curr_stair:
                elevator_instance.new_passenger_destination=destination
    return
    

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
        '''
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
        '''
        pass

    def run(self,request_queue,progressbar):
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
                curr_percent=(self.curr_stair*18-9)/358
                progressbar.set_fraction(curr_percent)
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
                    progressbar.set_fraction(curr_percent)
                # if the elavator is idling now
                else:
                    #print('find someone to pick up')
                    self.update_getting(request_queue)
                    self.curr_stair+=self.curr_direction
                    curr_percent=(self.curr_stair*18-9)/358
                    progressbar.set_fraction(curr_percent)
                time.sleep(1)


##################################
####         UI界面           #####
##################################

class RequestWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="Elevator Simulator")
        self.set_border_width(10)
        
        vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        self.add(vbox)
        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        
        exchange_queue=Queue()
        self.queue=exchange_queue
        
        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        for i in range(1,21):
            if i<10:
                num_str="0"+str(i)
            else:
                num_str=str(i)
            label = Gtk.Label(num_str)
            hbox.pack_start(label,True,True,0)
        
        self.progressbar1 = Gtk.ProgressBar()
        self.progressbar1.set_fraction(9/358)
        vbox.pack_start(self.progressbar1, True, True, 0)

        elavator1=Elavator()
        t1=Thread(target=elavator1.run,args=(exchange_queue,self.progressbar1))

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        label = Gtk.Label()
        label.set_text("电梯-1 内部按钮")
        label.set_justify(Gtk.Justification.LEFT)
        hbox.pack_start(label, True, True, 0)


        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        for i in range(1,21):
            if i<10:
                num_str="0"+str(i)
            else:
                num_str=str(i)
            button=Gtk.Button.new_with_label(num_str)
            button.connect("clicked",ask_for_destination,[i,elavator1])
            hbox.pack_start(button,True,True,0)

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        for i in range(1,21):
            if i<10:
                num_str="0"+str(i)
            else:
                num_str=str(i)
            label = Gtk.Label(num_str)
            hbox.pack_start(label,True,True,0)

        self.progressbar2 = Gtk.ProgressBar()
        self.progressbar2.set_fraction(9/358)
        vbox.pack_start(self.progressbar2, True, True, 0)

        elavator2=Elavator()
        t2=Thread(target=elavator2.run,args=(exchange_queue,self.progressbar2))

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        label = Gtk.Label()
        label.set_text("电梯-2 内部按钮")
        label.set_justify(Gtk.Justification.LEFT)
        hbox.pack_start(label, True, True, 0)

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        for i in range(1,21):
            if i<10:
                num_str="0"+str(i)
            else:
                num_str=str(i)
            button=Gtk.Button.new_with_label(num_str)
            button.connect("clicked",ask_for_destination,[i,elavator2])
            hbox.pack_start(button,True,True,0)

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        for i in range(1,21):
            if i<10:
                num_str="0"+str(i)
            else:
                num_str=str(i)
            label = Gtk.Label(num_str)
            hbox.pack_start(label,True,True,0)

        self.progressbar3 = Gtk.ProgressBar()
        self.progressbar3.set_fraction(9/358)
        vbox.pack_start(self.progressbar3, True, True, 0)

        elavator3=Elavator()
        t3=Thread(target=elavator3.run,args=(exchange_queue,self.progressbar3))

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        label = Gtk.Label()
        label.set_text("电梯-3 内部按钮")
        label.set_justify(Gtk.Justification.LEFT)
        hbox.pack_start(label, True, True, 0)

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        for i in range(1,21):
            if i<10:
                num_str="0"+str(i)
            else:
                num_str=str(i)
            button=Gtk.Button.new_with_label(num_str)
            button.connect("clicked",ask_for_destination,[i,elavator3])
            hbox.pack_start(button,True,True,0)

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        for i in range(1,21):
            if i<10:
                num_str="0"+str(i)
            else:
                num_str=str(i)
            label = Gtk.Label(num_str)
            hbox.pack_start(label,True,True,0)

        self.progressbar4 = Gtk.ProgressBar()
        self.progressbar4.set_fraction(9/358)
        vbox.pack_start(self.progressbar4, True, True, 0)

        elavator4=Elavator()
        t4=Thread(target=elavator4.run,args=(exchange_queue,self.progressbar4))

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        label = Gtk.Label()
        label.set_text("电梯-4 内部按钮")
        label.set_justify(Gtk.Justification.LEFT)
        hbox.pack_start(label, True, True, 0)

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        for i in range(1,21):
            if i<10:
                num_str="0"+str(i)
            else:
                num_str=str(i)
            button=Gtk.Button.new_with_label(num_str)
            button.connect("clicked",ask_for_destination,[i,elavator4])
            hbox.pack_start(button,True,True,0)

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        for i in range(1,21):
            if i<10:
                num_str="0"+str(i)
            else:
                num_str=str(i)
            label = Gtk.Label(num_str)
            hbox.pack_start(label,True,True,0)
            
        self.progressbar5 = Gtk.ProgressBar()
        self.progressbar5.set_fraction(9/358)
        vbox.pack_start(self.progressbar5, True, True, 0)

        elavator5=Elavator()
        t5=Thread(target=elavator5.run,args=(exchange_queue,self.progressbar5))

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        label = Gtk.Label()
        label.set_text("电梯-5 内部按钮")
        label.set_justify(Gtk.Justification.LEFT)
        hbox.pack_start(label, True, True, 0)

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        for i in range(1,21):
            if i<10:
                num_str="0"+str(i)
            else:
                num_str=str(i)
            button=Gtk.Button.new_with_label(num_str)
            button.connect("clicked",ask_for_destination,[i,elavator5])
            hbox.pack_start(button,True,True,0)

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        label = Gtk.Label()
        label.set_text("电梯外整楼层按钮")
        label.set_justify(Gtk.Justification.LEFT)
        hbox.pack_start(label, True, True, 0)

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)
        for i in range(1,21):
            if i<10:
                num_str="0"+str(i)
            else:
                num_str=str(i)
            button=Gtk.Button.new_with_label(num_str+" 上")
            button.connect("clicked",self.print_input_up,[i,self.queue])
            hbox.pack_start(button,True,True,0)
        
        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)

        for i in range(1,21):
            if i<10:
                num_str="0"+str(i)
            else:
                num_str=str(i)
            button=Gtk.Button.new_with_label(num_str+" 下")
            button.connect("clicked",self.print_input_down,[i,self.queue])
            hbox.pack_start(button,True,True,0)
            
        t1.start()
        t2.start()
        t3.start()
        t4.start()
        t5.start()
        
    def print_input_up(self,button,args_list):
        stair_num=args_list[0]
        exchange_queue=args_list[1]
        print("**REQUEST**:"+str(stair_num)+' '+"up")
        new_request=Request(stair_num,1)
        exchange_queue.put(new_request)
    def print_input_down(self,button,args_list):
        stair_num=args_list[0]
        exchange_queue=args_list[1]
        print("**REQUEST**:"+str(stair_num)+' '+"down")
        new_request=Request(stair_num,-1)
        exchange_queue.put(new_request)
class InitWindow(Gtk.Window):
    def __init__(self):
        Gtk.Window.__init__(self,title="Welcome")
        self.set_border_width(10)

        vbox=Gtk.Box(orientation=Gtk.Orientation.VERTICAL,spacing=6)
        self.add(vbox)

        hbox=Gtk.Box(spacing=6)
        vbox.pack_start(hbox,True,True,0)

        confirm_button=Gtk.Button.new_with_label("Start!")
        confirm_button.connect("clicked",self.start_window)
        hbox.pack_start(confirm_button,True,True,0)

    def start_window(self,button):
        self.close()
        new_start_window=RequestWindow()
        new_start_window.connect("destroy", Gtk.main_quit)
        new_start_window.show_all()
        Gtk.main()
        

if __name__=='__main__':
    window =InitWindow()        
    window.connect("destroy", Gtk.main_quit)
    window.show_all()
    Gtk.main()