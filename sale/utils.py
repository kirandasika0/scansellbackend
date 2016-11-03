import bmemcached
from datetime import datetime
from json import dumps, loads
from hashlib import sha224
# this file will never connect to the memcache server directly
# rather it will be passed an instance of the memcache client object

# CLASS CONSTANTS
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'

class MemcacheWrapper():
	def __init__(self, mc):
		self.client = mc
		self.now = datetime.now()

	def set_key_value(self, key, value):
		#creating the data structure for the insert
		created_at = datetime.now()
		memcache_structure = {
			'created_at': created_at.strftime(DATETIME_FORMAT),
			'updated_at': created_at.strftime(DATETIME_FORMAT),
			'last_access_at': created_at.strftime(DATETIME_FORMAT),
			'data': value
		}
		# insert the value into the memcached server
		return self.client.set(key, dumps(memcache_structure, indent=4))


	def get_val(self, key):
		if self.client.get(key):
			response = loads(self.client.get(key))
		else:
			response = False
		return response

	def update_last_access(self, key):
		#updating the last access for given memcache
		response = loads(self.client.get(key))
		#update the last access
		now = datetime.now()
		response['last_access_at'] = now.strftime(DATETIME_FORMAT)
		#update the memcache server with the response
		return self.client.set(key, dumps(response))

	def append_data_to_key(self, key, value):
		# get data from memcaches server
		response = loads(self.client.get(key))
		if type(response['data']) is not list:
			# looks like we have to create a new list and append it
			temp_response = response['data']
			response['data'] = list()
			response['data'].append(temp_response)
			response['data'].append(value)
		else:
			response['data'].append(value)

		# update the updated_at key in the memcahed structure
		response['updated_at'] = self.now.strftime(DATETIME_FORMAT)

		# updating memcahed
		return self.client.set(key, dumps(response))

	def delete(self, key):
		return self.client.delete(key)






''' ======================================================================== '''
''' CODE FOR FINDING BEST DEALS '''
class MinPQ():
    def __init__(self, mini=None, maxi=None, size=0):
        self.mini = mini
        self.maxi = maxi
        self.size = size
        self.current = None

    def getSize(self):
        return self.size

    def isEmpty(self):
        return self.size is 0

    def enqueue(self, e=None):
        # place element in the sorted postion of natural order
        if e is None:
            return False

        # element to be added in PQ
        x = LinkedNode(e)

        if self.isEmpty():
            self.mini = x
            self.maxi = x
            self.size += 1
            return True

        n = self.mini
        while n is not None:
            if e.comparePriceTo(n.element) < 0 and n is self.mini:
                x.next = n
                n.prev = x
                self.mini = x
                self.size += 1
                return True

            elif e.comparePriceTo(n.element) > 0 and n is self.maxi:
                n.next = x
                x.prev = n
                self.maxi = x
                self.size += 1
                return True

            elif e.comparePriceTo(n.element) < 0:
                n.prev.next = x
                x.prev = n.prev
                x.next = n
                n.prev = x
                self.size += 1
                return True

            # elif e.comparePriceTo(n.element) == 0:
            #     n.next.prev = x
            #     x.next = n.next
            #     n.next = x
            #     x.prev = n
            #     self.size += 1
            #     return True

            n = n.next
        return False

    def dequeue(self):
        if self.size == 0:
            return None

        if self.size == 1:
            n = self.maxi.element
            self.mini = None
            self.maxi = None
            return n

        n = self.mini.element
        self.mini = self.mini.next
        self.mini.prev = None
        self.size -= 1
        return n

    def peek(self):
        if self.mini == None:
            return None
        return self.mini.element
    
    def serialize(self, key, mc):
        """
        Method serializes a queue and saves it to memecache
        :return: boolean
        """
        if self.size == 0:
            return False
        
        queue = []
        n = self.mini
        while n is not None:
            queue.append(n.element.pk)
            n = n.next
        
        return mc.set_key_value(key, queue)
        
    
    
    def deserialize(self, key, mc):
        """
        :return: MinPQ
        """
        if key is None:
            return None
        
        value = mc.get_val(key)
        
        if value is None:
            return None
        
        return None
        
class LinkedNode():
    def __init__(self, element, next=None, prev=None):
        self.element = element
        self.next = next
        self.prev = prev

    def __str__(self):
        return self.element

class TestClass(object):
    def __init__(self, x):
        self.x = x


    def comparePriceTo(self, y):
        if self.x > y.x:
            return 1
        elif self.x < y.x:
            return -1
        else:
            return 0

    def __str__(self):
        return self.x
        
    def __repr__(self):
        return self.x