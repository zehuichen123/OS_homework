# class for each pages
class Block(object):
	def __init__(self):
		# block num based on its address
		self.block_num=None
		# block that last been used (For LRU record)
		self.last_used=None
		# block that first been used (For FIFO record)
		self.first_used=None

# class for each instructions
class Address(object):
	def __init__(self,num,is_load):
		# the physical address for each instruction
		self.num=num
		# whether this instruction has an evit
		self.is_load=is_load

# to find if there has a cache hit
# cache hit : return True
# cache miss: return False
def find_block(address,block_list,index):
	address_block_num=int((address-1)/10)
	for each_block in block_list:
		# check if the block has loaded some page
		if each_block.block_num!=None:
			# check if the page has been loaded
			if address_block_num==each_block.block_num:
				each_block.last_used=index
				return True
	else:
		return False

# to find if there is any empty block to load page
# has emtpy block : return True
# no empty block : return False	
def load_block(address,block_list,index):
	address_block_num=int((address-1)/10)
	for each_block in block_list:
		# check if the block has loaded some page
		if each_block.block_num==None:
			# load page into empty block
			each_block.block_num=address_block_num
			each_block.first_used=index
			each_block.last_used=index
			return True
	return False

# to find block to replace for new 
# block containing current instruction
def replace_block(address,block_list,index,replace_strategy):
	address_block_num=int((address-1)/10)
	record_num=index
	record_index=0
	# tranverse the whole block list to find 
	# the last recently used block or
	# the first used block and replace it
	for i,each_block in enumerate(block_list):
		# LRU replace strategy
		if replace_strategy==1:
			if each_block.last_used<record_num:
				record_num=each_block.last_used
				record_index=i
		# FIFO replace strategy
		else:
			if each_block.first_used<record_num:
				record_num=each_block.first_used
				record_index=i
	block_list[record_index].block_num=address_block_num
	block_list[record_index].first_used=index
	block_list[record_index].last_used=index
	return

# start to simulate the page replacement process
# replace_strategy 1: LRU ; 2: FIFO
def stimulate(address_list,replace_strategy):
	cache_list=[Block(),Block(),Block(),Block()]
	all_address_list=[]
	hit_count=0
	# traverse the whole instructions list
	# and simulate the repalce process
	for index,each_address in enumerate(address_list):
		# if cache hit
		if find_block(each_address,cache_list,index):
			hit_count+=1
			all_address_list.append(Address(each_address,0))
		# if cache miss
		else:
			# if there's emtpy block
			if load_block(each_address,cache_list,index):
				all_address_list.append(Address(each_address,1))
			# if need to replace old block (block evit)
			else:
				replace_block(each_address,cache_list,\
									index,replace_strategy)
				all_address_list.append(Address(each_address,1))
	return all_address_list,hit_count