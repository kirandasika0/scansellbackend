import bmemcached
from datetime import datetime
from json import dumps, loads
from hashlib import sha224
from .models import Sale
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
			response = loads(self.client.get(key))['data']
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

        queueList = []

        n = self.mini
        while n is not None:
            queueList.append(n.element.pk)
            n = n.next

        return mc.set_key_value(key, queueList)




    def deserialize(self, key, mc):
        """
        This method deserializes and creates an entire PriorityQueue from a
        provided key and the memcache object.
        For the deserialize to work the size of the queue must be equal to 0.
        :return: MinPQ
        """
        if self.size is not 0:
            return None

        savedData = mc.get_val(key)
        if savedData is False:
            return None

        for pk in savedData:
            self.enqueue(Sale.objects.get(pk=pk))

        return self

""" ============================== """
class MaxPQ():
    def __init__(self):
        self.max = None
        self.min = None
        self.size = 0

    def getSize(self):
        return self.size

    def isEmpty(self):
        return self.size == 0

    def enqueue(self, e=None):
        if e is None:
            return False

        x = LinkedNode(e)

        if self.isEmpty():
            self.max = x
            self.min = x
            self.size += 1
            return True

        n = self.max
        while n is not None:
            if e.comparePriceTo(n.element) > 0 and n is self.max:
                x.next = n
                n.prev = x
                self.max = x
                self.size += 1
                return True

            elif e.comparePriceTo(n.element) < 0 and n is self.min:
                n.next = x
                x.prev = n
                self.min = x
                self.size += 1
                return True

            elif e.comparePriceTo(n.element) > 0:
                n.prev.next = x
                x.prev = n.prev
                x.next = n
                n.prev = x
                self.size += 1
                return True

            n = n.next


    def dequeue(self):
        result = self.max.element
        self.max = self.max.next
        return result

    def peek(self):
        return self.max.element

    def serialize(self, key, mc):
        """
        Method serializes a Max PriorityQueue and saves it in memcache

        :return: bool
        """
        if self.size == 0:
            return False

        queueList = []
        n = self.max

        while n is not None:
            queueList.append(n.element.pk)

        return mc.set_key_value(key, queueList)


    def deserialize(self, key, mc):
        """
        Method Deserializes a MaxPriorityQueue from disk and gives it

        :return: MaxPQ
        """
        if self.size is not 0:
            return None

        savedData = mc.get_val(key)
        if savedData is False:
            return None

        for pk in savedData:
            self.enqueue(Sale.objects.get(pk=pk))

        return self


""" ============================ """
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



def binary_search(a, target, comparator):
    lo = 0
    hi = len(a) - 1
    i = 0
    mid = (lo + hi) / 2
    while lo <= hi:
        if a[lo].comparator(a[mid]) < 0:
            hi = mid - 1
        elif a[lo].comparator(a[mid]) > 0:
            lo = mid + 1
        else:
            return mid
