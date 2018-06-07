from django.shortcuts import render,redirect
from django.urls import reverse 
from .models import Request,Elavator,Passenger
from queue import Queue
from threading import Thread

# Create your views here.
exchange_queue=Queue()
elavator1=Elavator()
t1=Thread(target=elavator1.run,args=(exchange_queue,))
elavator2=Elavator()
t2=Thread(target=elavator2.run,args=(exchange_queue,))
elavator3=Elavator()
t3=Thread(target=elavator3.run,args=(exchange_queue,))
elavator4=Elavator()
t4=Thread(target=elavator4.run,args=(exchange_queue,))
elavator5=Elavator()
t5=Thread(target=elavator5.run,args=(exchange_queue,))
arg_dict={
        'elavator1':elavator1,
        'elavator2':elavator2,
        'elavator3':elavator3,
        'elavator4':elavator4,
        'elavator5':elavator5,
        'num_list':range(1,21),
    }
def start(request):
    
    t1.start()
    t2.start()
    t3.start()
    t4.start()
    t5.start()
    print('init')
    return redirect("/index/")

def index(request):
    #print(elavator1)
    return render(request,'elevator/awesome.html',arg_dict)

def request_up(request,stair_num):
    stair_num=int(stair_num)
    print("**REQUEST**: "+str(stair_num)+' up')
    #print(exchange_queue)
    new_request=Request(stair_num,1)
    exchange_queue.put(new_request)
    return render(request,'elevator/empty.html')

def request_down(request,stair_num):
    stair_num=int(stair_num)
    print("**REQUEST**: "+str(stair_num)+' down')
    new_request=Request(stair_num,-1)
    exchange_queue.put(new_request)
    return render(request,'elevator/empty.html')

def ask_for_destination(request,elevator_num,stair_num):
    elevator_num=int(elevator_num)
    stair_num=int(stair_num)
    elevator_name='elavator'+str(elevator_num)
    elevator_instance=arg_dict[elevator_name]
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
    return render(request,'elevator/empty.html')