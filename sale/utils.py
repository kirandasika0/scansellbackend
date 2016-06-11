import bmemcached
from datetime import datetime
from json import dumps, loads
from sale.feed import generate_feed
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