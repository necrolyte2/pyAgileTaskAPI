import urllib2
import urllib
from urllib2 import URLError, HTTPError
import json

__author__ = "vallardt@gmail.com (Tyghe Vallard)"
VERSION = "1.0.0"

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

class BadHttpMethodException( Exception ):
	"""
		Exception class raised when request methods are used that are not allowed on the server for a given url
	"""
	def __init__( self, url, requested_method, allowed_methods ):
		"""
			Initialize the variables

			url(str) - The url that was used in the request
			requested_method(str) - Any of the 4 HTTP methods. PUT, DELETE, GET, POST
			allowed_methods(str) - The methods allowed for the given url
		"""
		self.url = url
		self.requested_method = requested_method
		self.allowed_methods = allowed_methods

	def __str__( self ):
		return "URL(%s) only accepts Http method's %s. You supplied %s" % (self.url, self.allowed_methods, self.requested_method)

class AgileTaskAPI:
	""" Agile Task API wrapper in python """

	# The base url for AgileTaks's api
	api_base_url = 'https://agiletask.me'
	#api_base_url = 'http://tygertown.us'

	def __init__( self, api_key ):
		"""
			Set the api_key for the user for this class instance
			
			Params:
				api_key(str) - The api key from your user account
		"""

		# Set the api key for the user
		self.api_key = api_key

		# Valid True False values for AgileTask
		self.tf = [ 'true', 'false' ]

	def _send_request( self, url, data, method = 'GET' ):
		"""
			Sends a request to a url with the given data and using the given method

			Params:
				url(str) - The url to send the request to
				data(dict) - Dictionary of key/value pairs to be urlencoded and sent with the request
				method('GET'|'POST'|'DELETE'|'PUT') - Http method to use.

			Return:
				The raw output of the url

			Raises:
				ValueError - If the url returns a 404
				BadHttpMethod - If the method used for url is incorrect
				HTTPError - If there was an error with the request
		"""

		# Build the url to send to
		api_url = self.api_base_url + url

		# Setup the GET/POST/DELETE/UPDATE params
		params = urllib.urlencode( data )

		# Initialize our request using our custom Request Class
		req = RequestWithMethod( method, api_url, data = params )

		try:
			# Open the url
			response = urllib2.urlopen(req)
		except HTTPError, e:
			if hasattr( e, 'code' ) and e.code == 404:
				raise ValueError( "Bad URL. Most probable cause is an ID given that does not exist" )
			elif hasattr( e, 'code') and e.code == 405:
				raise BadHttpMethod( api_url, req.get_method(), e.info()['Allow'] )
		# Return our raw response as there were no errors
		if response.geturl() != api_url:
			print "Warning: Redirect detected could cause problems in the output"
		return response.read()

	def _decodeJson( self, jsonString ):
		"""
			Returns the json encoded string as a series of lists and dictionaries
			
			Params:
				jsonString(str) - The json string to convert to a Python list/dict

			Return:
				Python list/dict parsed from the jsonString
				or an empty list on error
		"""
		try:
			return json.loads( jsonString )
		except ValueError, e:
			print "Invalid json string returned from server"
			return []

	def _delete( self, url, params = {} ):
		"""
			Send data to a URL as DELETE and return the task that was deleted or 
			 [] if no task exists for that ID

			Params:
				url(str) - The url to send the DELETE to
				params(dict) - key/value pair to be urlencoded and sent with the request


			Return:
				Python list/dict from the json returned from the url
		"""
		# Need to append api_key to data if it isn't included
		url += '?' + urllib.urlencode( { "api_key" : self.api_key } )

		try:
			task = self._send_request( url, params, 'DELETE' )
		except ValueError, e:
			# If there was no task for the id we are trying to delete return []
			return []

		# Return the task we just deleted
		return self._decodeJson( task )

	def _post( self, url, data = {} ):
		"""
			Send data to a URL as POST and return the returned output from that page

			Params:
				url(str) - The url to send the POST to
				params(dict) - key/value pair to be urlencoded and sent with the request


			Return:
				Python list/dict from the json returned from the url
		"""
		# Need to append api_key to data if it isn't included
		url += '?' + urllib.urlencode( { "api_key" : self.api_key } )

		try:
			return self._decodeJson( self._send_request( url, data, 'POST' ) )
		except:
			return []

	def _put( self, url, data = {} ):
		"""
			Send data to a URL as PUT and return the output from the page as json

			Params:
				url(str) - The url to send the PUT to
				params(dict) - key/value pair to be urlencoded and sent with the request


			Return:
				Python list/dict from the json returned from the url
		"""
		# Need to append api_key to data if it isn't included
		url += '?' + urllib.urlencode( { "api_key" : self.api_key } )

		try:
			task = self._send_request( url, data, 'PUT' )
		except ValueError, e:
			# If there was no task for the id send return []
			return []

		# Return the task that was updated
		return self._decodeJson( task )

	def _get( self, url, params = {} ):
		"""
			Get data from a url and return the list/dict representation of the json returned

			Params:
				url(str) - The url to send the GET to
				params(dict) - key/value pair to be urlencoded and sent with the request


			Return:
				Python list/dict from the json returned from the url
		"""

		# The only data we send is the api_key
		if params:
			data = params
		else:
			data = { 'api_key' : self.api_key }

		# Return the request object
		# Catch the bad requests because they are probably valid requests just no data for them
		# I.E. GetSingle( 53 ) when the user does not have a task with id of 53 which returns a 404 page that is
		# not parseable by json
		try:
			task = self._send_request( url, data, 'GET' )
		except ValueError, e:
			return []

		return self._decodeJson( task )

	def _is_digit( self, number ):
		"""
			Returns True if number is a digit. False otherwise

			Params:
				number - The object to check

			Return:
				True if the object is a digit or False otherwise
		"""
		if type( number ) == type( 1 ):
			return True
		else:
			return False

	def _check_values( self, id = 1, name = "Some String", icebox = 'true', position = 0, complete = 'true' ):
		"""
			Make sure every value has a valid value and raise correct exception for it
			Every task has these values and they are the core of the task so they have to be correct

			Params:
				id(int) - The id of a task
				name(str) - The name of a task
				icebox('true'|'false') - Is the task in the icebox or not
				position(int) - The rank or position of a task in it's current list
				complete('true'|'false') - Is the task completed(in the complete list)

			Raises:
				ValueError if any of the values are invalid
		"""
		# Make sure the id is a digit
		if not self._is_digit( id ):
			raise ValueError( "ID has to be an integer value > 0" )

		# Make sure the position is a digit
		if not self._is_digit( position ):
			raise ValueError( "Position has to be an integer value > 0" )

		# Make sure icebox is valid
		if not icebox in self.tf:
			raise ValueError( "icebox value given is incorrect" )

		# Make sure complete is valid
		if not complete in self.tf:
			raise ValueError( "complete value given is incorrect" )

	def GetSingle( self, id ):
		"""
			http://doc.agiletask.me/get_single.html
			Returns a single task by its id

			Params:
				id(int) - The id of a task

			Return:
				Python list/dict object representing a task.
				See the link above for object definition
		"""
		# Check id
		self._check_values( id = id )

		# API URL
		api_url = "/tasks/" + str( id ) + ".json"

		# Return the request object
		return self._get( api_url )

	def GetCompleted( self ):
		"""
			http://doc.agiletask.me/get_completed.html
			Returns all tasks completed

			Return:
				Python list/dict object representing all completed tasks.
				See the link above for object definition
		"""
		# API URL
		api_url = '/tasks/completed.json'

		# Return the request object
		return self._get( api_url )

	def GetIcebox( self ):
		"""
			http://doc.agiletask.me/get_icebox.html
			Returns all tasks in icebox

			Return:
				Python list/dict object representing all tasks in the icebox.
				See the link above for object definition
		"""
		# API URL
		api_url = '/tasks/icebox.json'

		# Return the request object
		return self._get( api_url )

	def GetAllTasks( self ):
		"""
			http://doc.agiletask.me/get_tasks.html
			Returns all tasks

			Return:
				Python list/dict object representing all tasks.
				See the link above for object definition
		"""
		# API URL
		api_url = '/tasks.json'

		# Return the request object
		return self._get( api_url )

	def GetToday( self ):
		"""
			http://doc.agiletask.me/get_today.html
			Returns today's tasks

			Return:
				Python list/dict object representing a all tasks in Todayask.
				See the link above for object definition
		"""
		# API URL
		api_url = '/tasks/today.json'

		# Return the request object
		return self._get( api_url )

	def GetRecentAchievements( self ):
		"""
			http://doc.agiletask.me/get_new_achievements.html
			Returns all recently aquired achievments

			Return:
				Python list/dict object representing all recent achievements.
				See the link above for object definition
		"""
		# API URL
		api_url = '/achievements/newly_received.json'

		# Return the request object
		return self._get( api_url )

	def GetAllAchievements( self ):
		"""
			http://doc.agiletask.me/get_achievements.html
			Returns all achievments

			Return:
				Python list/dict object representing all achievements.
				See the link above for object definition
		"""
		# API URL
		api_url = '/achievements.json'

		# Return the request object
		return self._get( api_url )

	def AddTask( self, name, icebox = 'true', position = 0, complete = 'false' ):
		"""
			http://doc.agiletask.me/new_tasks.html
			Adds a new task given task info

			Params:
				name(str) - The name of the task to be added
				icebox('true'|'false') - If the task should be added to the icebox or not. Valid values are 'true' | 'false'.
				position(int) - Priority or position of the task in the list you are adding it too. Lower is higher priority.
				complete('true'|'false') - If the task should be in the completed list or the today/icebox page

			Return:
				Python list/dict object representing a task. See the link above for object definition
		"""
		# API URL
		api_url = '/tasks.json'
		#api_url = '/testpost.php'

		# Check all values given
		self._check_values( 1, name, icebox, position, complete )

		# The Data to send
		task = { 
			 "task[position]" : position, \
			 "task[name]" : name, \
			 "task[icebox]" : icebox, 
			 "task[complete]" : complete \
		       }
		return self._post( api_url, task )
		
	def UpdateTask( self, id = None, name = None, icebox = None, position = None, complete = None, task = {} ):
		"""
			http://doc.agiletask.me/update_tasks.html
			Updates a task

			Params:
				id(int) - The id of a task
				name(str) - The new name of the task
				icebox('true'|'false') - New value for the icebox
				position(int) - New value for the position
				complete('true'|'false') - New value for complete
				task(dict) - { 'task' : { 
								'name' : <new name>, 
								'icebox' : <new icebox>, 
								'complete' : <new complete>, 
								'position' : <new position> 
							}
						   }

				Note: id is required and also either any combination of (name, icebox, position, complete) or (a task dictionary representation)


			Return:
				Python list/dict object representing the old task.
				See the link above for object definition

			Raises:
				KeyError - If you supply task as the parameter and do not supply all 4 keys for the task
					    This is a poor implementation but it works for now
		"""
		
		# If task was given as a convienence we will use the values from that dictionary
		if task:
			name = task['task']['name']
			icebox = task['task']['icebox']
			complete = task['task']['complete']
			position = task['task']['position']

		# Build our data dictionary to send to server using only values that are given
		data = {}
		if not name:
			name = ''
		else:
			data['task[name]'] = name
		if not icebox:
			icebox = 'false'
		else:
			data['task[icebox]'] = icebox
		if not position:
			position = 0
		else:
			data['task[position]'] = position
		if not complete:
			complete = 'false'
		else:
			data['task[complete]'] = complete

		# Check the values given
		self._check_values( id = id, name = name, icebox = icebox, position = position, complete = complete )

		# API URL
		api_url = '/tasks/' + str( id ) + '.json'

		return self._put( api_url, data )

	def DeleteTask( self, id ):
		"""
			http://doc.agiletask.me/delete_tasks.html
			Deletes a task

			Params:
				id(int) - The id of a task

			Return:
				Python list/dict object representing the task just deleted.
				See the link above for object definition
		"""
		# Make sure the id is correct
		self._check_values( id = id )

		# API URL
		api_url = '/tasks/' + str( id ) + '.json'

		return self._delete( api_url )

if __name__ == "__main__":
	pass
