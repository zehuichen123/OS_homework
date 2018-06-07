from django.shortcuts import render
from .algorithm import stimulate
import random
import os

# Create your views here.
def parse_address_list():
	address_num=random.randint(0,5)
	curr_dir=os.path.abspath('.')
	address_file_dir=os.path.join(curr_dir,'random_address.txt')
	with open(address_file_dir,'r') as f:
		all_address=f.readlines()
	address_list_str=all_address[address_num]
	address_list_str=address_list_str.strip('\n')
	address_list_str=address_list_str.split(',')
	address_list=[]
	for each_address in address_list_str:
		address_list.append(int(each_address))
	return address_list

def index(request):
	return render(request,'simulator/index.html',locals())

def lru(request):
	address_list=parse_address_list()
	lru_address_list,lru_hit_count=stimulate(address_list,1)
	lru_hit_ratio=str((lru_hit_count/320*100))[:4]
	return render(request,'simulator/lru.html',locals())

def readme(request):
	home=1
	return render(request,'simulator/readme.html',locals())

def fifo(request):
	address_list=parse_address_list()
	fifo_address_list,fifo_hit_count=stimulate(address_list,2)
	fifo_hit_ratio=str((fifo_hit_count/320*100))[:4]
	return render(request,'simulator/fifo.html',locals())

