import urllib2
import urllib
from urllib2 import URLError
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
			print e
			if hasattr(e, 'reason'):
				print 'We failed to reach a server.'
				print 'Reason: ', e.reason
			elif hasattr(e, 'code'):
				print 'The server couldn\'t fulfill the request.'
				print 'Error code: ', e.code
		else:
			# Return our raw response as there were no errors
			return response.read()

	def _decodeJson( self, jsonString ):
		""" Returns the json encoded string as a series of lists and dictionaries """
		return json.loads( jsonString )


	def GetToday( self ):
		"""
			http://doc.agiletask.me/get_today.html
			Returns today's tasks
		"""
		# The only data we send is the api_key
		data = { 'api_key' : self.api_key }

		# The url for today's taks in json
		api_url = '/tasks/today.json'

		# Return the request object
		return self._decodeJson( self._send_request( api_url, data, 'GET' ) )

