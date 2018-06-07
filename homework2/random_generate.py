#!/usr/bin/env python3
# -*- coding:utf-8 -*-

import random

curr_addr=random.randint(1,320)
seq_count=160
back_count=80
front_count=80

def get_random_list():
	random_list=[]
	random_list.append(curr_addr)
	while (seq_count>=0 or back_count>=0 or front_count>=0):
		random_num=random.random()
		if random_num < 1/3:
			if seq_count>0 and curr_addr<320:
				seq_count-=1
				curr_addr+=1
				random_list.append(curr_addr)
			else:
				continue
		if random_num >= 1/3 and random <2/3:
			if back_count>0 and curr_addr>1:
				back_count-=1
				curr_addr=random.randint(1,curr_addr)
				random_list.append(curr_addr)
			else:
				continue
		else:
			if front_count>0 and curr_addr<319:
				front_count-=1
				curr_addr=random.randint(curr_addr+1,320)
				random_list.append(curr_addr)
	return 
