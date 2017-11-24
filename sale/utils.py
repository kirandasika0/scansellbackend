import pdb
import time
import pprint
from hashlib import sha224
from random import randint
from json import dumps, loads
from datetime import datetime
from collections import defaultdict

import bmemcached
from firebase import firebase

from .models import Sale
from .location import Location
from .models import Sale
from .haversine_km import haversine_km

# this file will never connect to the memcache server directly
# rather it will be passed an instance of the memcache client object

# CLASS CONSTANTS
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'
FIREBASE_BUCKET = "https://switch-1376.firebaseio.com"
FB = firebase.FirebaseApplication(FIREBASE_BUCKET)


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




def make_graph_sales_connections(uLoc, sales):
	# connections will be list of tuples
	connections = []
	#first filter - distance filter
	nearby = []
	for sale in sales:
		sLat, sLong = sale.geo_point.split(',')
		sLoc = Location(sLat, sLong)
		distance = haversine_km(uLoc, sLoc)
		if distance <= 10000000:
			nearby.append(sale)

	for sale in nearby:
		#sCategories - a list of categories
		sCategories = loads(sale.categories)
		temp = list(nearby)
		temp.remove(sale)
		sConnections = get_connection(sCategories, temp, connections=[])
		if sConnections is not None:
			for connection in sConnections:
				if sale is not connection:
					connections.append((sale, connection))
	return connections



def get_connection(sCategories, sales, connections=[]):
	if sCategories is None or len(sCategories) is 0:
		return connections
	category = sCategories[len(sCategories) - 1]
	for sale in sales:
		sCategories2 = loads(sale.categories)
		if category in sCategories2:
			connections.append(sale)
	sCategories.pop()
	return get_connection(sCategories, sales, connections=connections)

def test_connections():
	sales = Sale.objects.all()
	uLat, uLong = sales[0].geo_point.split(',')
	uLoc = Location(uLat, uLong)
	connections = make_graph_sales_connections(uLoc, sales)
	# for a,b in connections:
	# 	print (a.book.uniform_title , b.book.uniform_title)
	g = Graph(connections)
	randomSale1 = sales[randint(0, len(sales) - 1)]
	randomSale2 = sales[randint(0, len(sales) - 1)]
	print(randomSale1.seller_username + " " + randomSale1.book.uniform_title)
	print(randomSale2.seller_username + " " + randomSale2.book.uniform_title)
	path = g.find_path(randomSale1, randomSale2)
	if path == None:
		return
	for a in path:
		print (a.seller_username, a.book.full_title)



class Graph():
	def __init__(self, connections, directed=False):
		self._graph = defaultdict(set)
		self._directed = directed
		self.add_connections(connections)

	def add_connections(self, connections):
		for node1, node2 in connections:
			self.add(node1, node2)


	def add(self, node1, node2):
		edge_weight = self.calculate_edge_weight(node1, node2)
		self._graph[node1].add((edge_weight,node2))
		if not self._directed:
			self._graph[node2].add((edge_weight,node1))

	def calculate_edge_weight(self, node1, node2):
		lat1, long1 = node1.geo_point.split(',')
		lat2, long2 = node2.geo_point.split(',')
		l1 = Location(lat1, long1)
		l2 = Location(lat2, long2)
		t1 = time.mktime(node1.created_at.timetuple())
		t2 = time.mktime(node2.created_at.timetuple())
		return haversine_km(l1, l2) * randint(0,200) * (1/t1) * (1/t2)

	def find_path(self, node1, node2, path=[]):
		path = path + [node1]
		if node1 == node2:
			return path
		if node1 not in self._graph:
			return None
		for edge_weight, node in self._graph[node1]:
			if node not in path:
				new_path = self.find_path(node, node2, path)
				if new_path:
					return new_path
		return None



class FirebaseRequest():
    def __init__(self, endpoint, payload=None):
        self.payload = payload
        self.endpoint = endpoint


    def post(self, uid=None):
        if self.payload is None:
            return False

        if FB.get(self.endpoint, uid) is None:
            return FB.post(self.endpoint, self.payload)
        else:
            self.delete(self.endpoint)
            return FB.post(self.endpoint, self.payload)
        return False

    def delete(self, uid=None):
        return FB.delete(self.endpoint, uid)
