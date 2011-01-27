import urllib2
import urllib
from urllib2 import URLError, HTTPError
import json

__author__ = "vallardt@gmail.com (Tyghe Vallard)"
VERSION = "0.0.1"

class RequestWithMethod(urllib2.Request):
	"""
		http://benjamin.smedbergs.us/blog/2008-10-21/putting-and-deleteing-in-python-urllib2/
		Allows you to change the request method to anything you wish
	"""
	def __init__(self, method, *args, **kwargs):
		self._method = method
		urllib2.Request.__init__(self, *args, **kwargs)

	def get_method(self):
		return self._method

class AgileTaskAPI:
	""" Agile Task API wrapper in python """

	# The base url for AgileTaks's api
	api_base_url = 'https://agiletask.me'

	def __init__( self, api_key ):
		""" Setup the class """

		# Set the api key for the user
		self.api_key = api_key

	def _send_request( self, url, data, method = 'GET' ):
		""" Sends a request to a url with the given data and using the given method """

		# Build the url to send to
		api_url = self.api_base_url + url

		# Setup the GET/POST/DELETE/UPDATE params
		params = urllib.urlencode( data )

		# Initialize our request using our custom Request Class
		req = RequestWithMethod( method, api_url, data = params )

		try:
			# Open the url
			response = urllib2.urlopen(req)
		except URLError, e:
			if hasattr(e, 'reason'):
				print 'We failed to reach a server.'
				print 'Reason: ', e.reason
			elif hasattr(e, 'code') and e.code != 404:
				print 'The server couldn\'t fulfill the request.'
				print "URL: %s" % api_url
				print 'Error code: ', e.code
		else:
			# Return our raw response as there were no errors
			if response.geturl() != api_url:
				print "Warning: Redirect detected could cause problems in the output"
			return response.read()

	def _decodeJson( self, jsonString ):
		""" Returns the json encoded string as a series of lists and dictionaries """
		try:
			return json.loads( jsonString )
		except ValueError, e:
			print "Invalid json string returned from server"
			return []

	def _get( self, url, params = {} ):
		""" Get data from a url and return the list/dict representation of the json returned """

		# The only data we send is the api_key
		if params:
			data = params
		else:
			data = { 'api_key' : self.api_key }

		# Return the request object
		# Catch the bad requests because they are probably valid requests just no data for them
		# I.E. GetSingle( 53) when the user does not have a task with id of 53 which returns a 404 page that is
		# not parseable by json
		try:
			return self._decodeJson( self._send_request( url, data, 'GET' ) )
		except:
			return []

	def _is_id( self, number ):
		if type( number ) == type( 1 ):
			return True
		else:
			return False

	# Tests written
	def GetSingle( self, id ):
		"""
			http://doc.agiletask.me/get_single.html
			Returns a single task by its id
			HTTP Method: GET
		"""
		if not self._is_id( id ) and id > 0:
			raise ValueError( 'ID must be an integer value > 0' )

		# API URL
		api_url = "/tasks/" + str( id ) + ".json"

		# Return the request object
		return self._get( api_url )

	def GetCompleted( self ):
		"""
			http://doc.agiletask.me/get_completed.html
			Returns all tasks completed
			HTTP Method: GET
		"""
		# API URL
		api_url = '/tasks/completed.json'

		# Return the request object
		return self._get( api_url )

	def GetIcebox( self ):
		"""
			http://doc.agiletask.me/get_icebox.html
			Returns all tasks in icebox
			HTTP Method: GET
		"""
		# API URL
		api_url = '/tasks/icebox.json'

		# Return the request object
		return self._get( api_url )

	def GetAllTasks( self ):
		"""
			http://doc.agiletask.me/get_tasks.html
			Returns all tasks
			HTTP Method: GET
		"""
		# API URL
		api_url = '/tasks.json'

		# Return the request object
		return self._get( api_url )

	def GetToday( self ):
		"""
			http://doc.agiletask.me/get_today.html
			Returns today's tasks
			HTTP Method: GET
		"""
		# API URL
		api_url = '/tasks/today.json'

		# Return the request object
		return self._get( api_url )

	def GetRecentAchievements( self ):
		"""
			http://doc.agiletask.me/get_new_achievements.html
			Returns all recently aquired achievments
			HTTP Method: GET
		"""
		# API URL
		api_url = '/achievements/newly_received.json'

		# Return the request object
		return self._get( api_url )

	def GetAllAchievements( self ):
		"""
			http://doc.agiletask.me/get_achievements.html
			Returns all achievments
			HTTP Method: GET
		"""
		# API URL
		api_url = '/achievements.json'

		# Return the request object
		return self._get( api_url )

	def AddTask( self ):
		"""
			http://doc.agiletask.me/new_tasks.html
			Adds a new task
			HTTP Method: POST
		"""

		# API URL
		api_url = '/tasks/tasks.json'

	def UpdateTask( self, id ):
		"""
			http://doc.agiletask.me/update_tasks.html
			Updates a task
			HTTP Method: PUT
		"""

		# API URL
		api_url = '/tasks/' + str( id ) + '.json'

	def DeleteTask( self, id ):
		"""
			http://doc.agiletask.me/delete_tasks.html
			Deletes a task
			HTTP Method: DELETE
		"""

		# API URL
		api_url = '/tasks/' + str( id ) + '.json'

if __name__ == "__main__":
    import doctest
    doctest.testmod()
