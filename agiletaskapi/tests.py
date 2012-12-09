#!/usr/bin/env python

import unittest
from agiletaskapi.AgileTaskAPI import AgileTaskAPI
import sys
import time

class BaseTests( unittest.TestCase ):
	def setUp( self ):
		self.api = AgileTaskAPI( 'CLOrJlYa5Ny02fs-F8Zz' );

	def _isList( self, item ):
		return type( [] ) == type( item )

	def test_json_decode( self ):
		""" Tests a simple json string to make sure it decodes correctly """
		jsonString = '[{"hello":1}]'
		json = self.api._decodeJson( jsonString )
		self.assertTrue( len( json ) == 1 )

class GetTestCases( BaseTests ):
	"""
		Tests to make sure getting tasks works
		Assumes that AddTask works
	"""
	def setUp( self, *args, **kwargs ):
		super( GetTestCases, self ).setUp( *args, **kwargs )
		self.alltasks = []
		self.fixtureTasks = []
		self.fixtureTasks.append( self.api.AddTask( name = "Get This Task Today", icebox = 'false', complete = 'false' ) )
		self.fixtureTasks.append( self.api.AddTask( name = "Get This Task Icebox", icebox = 'true', complete = 'false' ) )
		self.fixtureTasks.append( self.api.AddTask( name = "Get This Task Complete", icebox = 'false', complete = 'true' ) )

	def tearDown( self ):
		# Remove the tasks we created in setUP
		for task in self.fixtureTasks:
			self.api.DeleteTask( task['task']['id'] )

	def test_getalltasks_good( self ):
		""" Should return all tasks as a list """
		# Actually save this result set for later
		self.alltasks = self.api.GetAllTasks()

		# Should be a list
		self.assertTrue( self._isList( self.alltasks ) )

		# The list should be larger than 0
		self.assertTrue( len( self.alltasks ) >= 3 )

	def test_getcompleted_good( self ):
		""" Should return all tasks as a list """
		tasks = self.api.GetCompleted()
		# Should be a list
		self.assertTrue( self._isList( tasks ) )
		
		# Should be at least 1 task in the completed list
		self.assertTrue( len( tasks ) >= 1 )

	def test_geticebox_good( self ):
		""" Should return all tasks as a list """
		tasks = self.api.GetIcebox()
		# Should be a list
		self.assertTrue( self._isList( tasks ) )

		# Should be at least one item in the icebox
		self.assertTrue( len( tasks ) >= 1 )

	def test_gettoday_good( self ):
		""" Should return all tasks as a list """
		tasks = self.api.GetToday()
		# Should be a list
		self.assertTrue( self._isList( tasks ) )

		# Should be at least one item in today list
		self.assertTrue( len( tasks ) >= 1 )

	def test_getachievements_good( self ):
		""" Should return all tasks as a list """
		# Should be a list
		self.assertTrue( self._isList( self.api.GetAllAchievements() ) )

	def test_getrecentachievements_good( self ):
		""" Should return all tasks as a list """
		# Should be a list
		self.assertTrue( self._isList( self.api.GetRecentAchievements() ) )

	def test_getsingle_bad_id_given( self ):
		""" GetSingle raises exception on bad input """
		self.failUnlessRaises( ValueError, self.api.GetSingle, "henry" )

	def test_getsingle_no_task_for_id( self ):
		""" Should return empty list when there is no task for an id """
		import random

		# Make sure that we have all the tasks in the variable in case the all tasks test has not been run
		if not self.alltasks:
			self.alltasks = self.api.GetAllTasks()

		# Build a list of all id's of tasks we own
		ids = [task['task']['id'] for task in self.alltasks]

		# Get an id that is not in the list of id's we own
		id = random.randint( 1, 100000 )
		while id in ids:
			id = random.randint( 1, 100000 )

		self.assertEqual( self.api.GetSingle( id ), [] )

	def test_getsingle_good_id_given( self ):
		""" Should return a list representation of the task's json object """
		# Fetch the first task we created in setUp
		task = self.api.GetSingle( self.fixtureTasks[0]['task']['id'] )

		self.assertTrue( type( task ) == type( {} ), "The task has to be a dict" )
		self.assertTrue( len( task ) == 1, "The task has to be length 1" )

class AddTestCases( BaseTests ):
	"""
		Tests to make sure that Adding a task works
		Depends on DeleteTask working which makes a vicious cycle of testing
	"""
	def test_addtask_today_good( self ):
		""" Should add a task to the today list """
		task = self.api.AddTask( "This task should go into Today", icebox = 'false', complete = 'false' )
		# Make sure we are getting a dict back
		self.assertTrue( type( task ) == type( {} ), str( task ) )
		# Length has to be 1
		self.assertEqual( len( task ), 1, str( task ) )
		# icebox is false
		self.assertFalse( ( task['task']['icebox'] ) )
		# complete is false
		self.assertFalse( ( task['task']['complete'] ) )

		# Delete the task
		self.api.DeleteTask( task['task']['id'] )

	def test_addtask_icebox_good( self ):
		""" Should add a task to the icebox list """
		task = self.api.AddTask( "This task should go into Icebox", icebox = 'true', complete = 'false' )
		# Make sure we are getting a dict back
		self.assertTrue( type( task ) == type( {} ), str( task ) )
		# Length has to be 1
		self.assertEqual( len( task ), 1, str( task ) )
		# icebox is false
		self.assertTrue( ( task['task']['icebox'] ) )
		# complete is false
		self.assertFalse( ( task['task']['complete'] ) )

		# Delete the task
		self.api.DeleteTask( task['task']['id'] )

	def test_addtask_complete_good( self ):
		""" Should add a task to the icebox list """
		task = self.api.AddTask( "This task should go into completed", complete = 'true' )
		# Make sure we are getting a dict back
		self.assertTrue( type( task ) == type( {} ), str( task ) )
		# Length has to be 1
		self.assertEqual( len( task ), 1, str( task ) )
		# complete is false
		self.assertTrue( ( task['task']['complete'] ) )

		# Delete the task
		self.api.DeleteTask( task['task']['id'] )

	def test_addtask_bad_id( self ):
		""" Should raise an exception from bad position value """
		self.failUnlessRaises( ValueError, self.api.AddTask, name = "This should not be added", position = 'henry' )

	def test_addtask_bad_icebox( self ):
		""" Should raise an exception from bad value for icebox """
		self.failUnlessRaises( ValueError, self.api.AddTask, name = "This should not be added", icebox = 'BadValue' )

	def test_addtask_bad_completed( self ):
		""" Should raise an exception from bad value for completed """
		self.failUnlessRaises( ValueError, self.api.AddTask, name = "This should not be added", complete = 'BadValue' )

	def test_addtask_with_tag( self ):
		""" Should add a task that has tags in the name """
		task = self.api.AddTask( "This task should go into Today #TestTag", icebox = 'false', complete = 'false' )
		# Make sure we are getting a dict back
		self.assertTrue( type( task ) == type( {} ), str( task ) )
		# Length has to be 1
		self.assertEqual( len( task ), 1, str( task ) )

		# Delete the task
		self.api.DeleteTask( task['task']['id'] )
		
	def test_addtask_bad_name( self ):
		""" Should raise an exception if bad things are given in the name """
		pass

class UpdateTestCases( BaseTests ):
	"""
		Tests to make sure that Updating a task works.
		Assumes that both Adding and Deleting tests have passed
	"""

	def setUp( self, *args, **kwargs ):
		""" Create a task to work with """
		super( UpdateTestCases, self ).setUp( *args, **kwargs )
		self.task = self.api.AddTask( name = "Update Me", icebox = 'false', complete = 'false' )
		self.taskID = self.task['task']['id']

	def tearDown( self ):
		""" Remove the task created """
		self.api.DeleteTask( self.taskID )

	def test_updatetask_name( self ):
		""" Should update a task in today list """
		# Update the task and store the old task's value for comparison
		updatedTask = self.api.UpdateTask( self.taskID, name = "I have updated #Test" )

		# The original task's name and the updatedTask's name should be different after the update
		self.assertNotEqual( self.task['task']['name'], updatedTask['task']['name'] )

		# The updated_at should now be different as well
		self.assertNotEqual( self.task['task']['updated_at'], updatedTask['task']['updated_at'] )

		# Now set the task to our updated task for later comparisons
		self.task = updatedTask

	def test_updatetask_today_does_not_exist( self ):
		""" Should raise exception that task does not exist """
		# Update a task that doesn't exist(Shouldn't have a task with id of 0)
		self.assertEqual( self.api.UpdateTask( 0, name = "Update non-existing task" ), [] )

	def test_updatetask_move_to_today( self ):
		""" Should move a task from icebox to today """
		# Move to icebox so we can move to today
		updatedTask = self.api.UpdateTask( self.taskID, icebox = 'true', complete = 'false' )

		# Move the task to today
		updatedTask = self.api.UpdateTask( self.taskID, icebox = 'false' )

		# Task should not be in the icebox
		self.assertFalse( updatedTask['task']['icebox'] )

		# Now set the task to our updated task for later comparisons
		self.task = updatedTask
	
	def test_updatetask_move_to_icebox( self ):
		""" Should move a task from today to icebox """
		# Move to today so we can move to icebox
		updatedTask = self.api.UpdateTask( self.taskID, icebox = 'false', complete = 'false' )
		
		# Move to icebox so we can move to today
		updatedTask = self.api.UpdateTask( self.taskID, icebox = 'true', complete = 'false' )

		# Task should be in the icebox
		self.assertTrue( updatedTask['task']['icebox'] )

		# Now set the task to our updated task for later comparisons
		self.task = updatedTask

	def test_updatetask_move_to_complete( self ):
		""" Should move a task to the complete list """
		# Move out of complete
		updatedTask = self.api.UpdateTask( self.taskID, icebox = 'false', complete = 'false' )

		# Move the task to the complete
		updatedTask = self.api.UpdateTask( self.taskID, complete = 'true' )

		# Task should now be in the complete
		self.assertTrue( updatedTask['task']['complete'] )

		# Now set the task to our updated task for later comparisons
		self.task = updatedTask

	def test_updatetask_use_task_param( self ):
		""" Should update a task given just a modified task returned from an update or get """
		# Set a new name
		self.task['task']['name'] = "Here is my new name #Update Test"

        # Make sure we sleep at least 1 second so the update has a different time
		time.sleep( 1 )

		# Update our task using a previously returned task
		updatedTask = self.api.UpdateTask( self.taskID, task = self.task )
		
		# Make sure our 
		self.assertNotEqual( self.task['task']['updated_at'], updatedTask['task']['updated_at'] )

		# Now set our original task to updated task for later comparisons
		self.task = updatedTask

	def test_updatetask_bad_id( self ):
		""" Should raise an ValueError exception from the bad id given """
		self.failUnlessRaises( ValueError, self.api.UpdateTask, id = 'henry', name = "Update Me" )

	def test_updatetask_bad_position( self ):
		""" Should raise an ValueError exception from the bad position given """
		self.failUnlessRaises( ValueError, self.api.UpdateTask, id = self.taskID, position = "henry" )

	def test_updatetask_bad_icebox( self ):
		""" Should raise an ValueError exception from the bad icebox value given """
		self.failUnlessRaises( ValueError, self.api.UpdateTask, id = self.taskID, icebox = "henry" )

	def test_updatetask_bad_complete( self ):
		""" Should raise an ValueError exception from the bad complete value given """
		self.failUnlessRaises( ValueError, self.api.UpdateTask, id = self.taskID, complete = "henry" )

class DeleteTestCases( BaseTests ):
	"""
		Tests to make sure that Deleting a task works.
		Assumes that both Adding and Get'ing tests have passed
	"""
	def test_deletetask_today_good( self ):
		""" Should delete a task from today """
		# Add a task to delete it
		task = self.api.AddTask( "Please Delete Me", icebox = 'false', complete = 'false' )
		taskID = task['task']['id']
		self.api.DeleteTask( taskID )
		# The resulting fetch should be an empty list if the task was deleted
		self.assertEqual( self.api.GetSingle( taskID ), [] )

	def test_deletetask_today_does_not_exist( self ):
		""" Should raise exception that task does not exist """
		# Deleting a task that doesn't exist(Shouldn't have a task with id of 0)
		self.assertEqual( self.api.DeleteTask( 0 ), [] )

	def test_deletetask_icebox_good( self ):
		""" Should delete a task from the icebox list """
		# Add a task to delete it
		task = self.api.AddTask( "Please Delete Me", icebox = 'true', complete = 'false' )
		taskID = task['task']['id']
		self.api.DeleteTask( taskID )
		# The resulting fetch should be an empty list if the task was deleted
		self.assertEqual( self.api.GetSingle( taskID ), [] )

	def test_deletetask_complete_good( self ):
		""" Should delete a task from the complete list """
		# Add a task to delete it
		task = self.api.AddTask( "Please Delete Me", complete = 'true' )
		taskID = task['task']['id']
		self.api.DeleteTask( taskID )
		# The resulting fetch should be an empty list if the task was deleted
		self.assertEqual( self.api.GetSingle( taskID ), [] )

	def test_deletetask_bad_id( self ):
		""" Should raise an exception from the bad id given """
		self.failUnlessRaises( ValueError, self.api.DeleteTask, 'henry' )

def GetTestSuite( ):
	return unittest.TestLoader().loadTestsFromTestCase( GetTestCases )

def AddTestSuite( ):
	return unittest.TestLoader().loadTestsFromTestCase( AddTestCases )

def UpdateTestSuite( ):
	return unittest.TestLoader().loadTestsFromTestCase( UpdateTestCases )

def DeleteTestSuite( ):
	return unittest.TestLoader().loadTestsFromTestCase( DeleteTestCases )

def AllTestSuite():
	return unittest.TestSuite( [GetTestSuite(), AddTestSuite(), UpdateTestSuite(), DeleteTestSuite()] )

if __name__ == '__main__':
	validTests = [ 'Get', 'Add', 'Update', 'Delete', 'All' ]
	validTests = "|".join( validTests )
	try:
		suiteName = sys.argv[1]
	except IndexError:
		print "Provide a test to run. %s " % validTests
		sys.exit( -1 )

	if suiteName == 'Get':
		suite = GetTestSuite()
	elif suiteName == 'Add':
		suite = AddTestSuite()
	elif suiteName == 'Update':
		suite = UpdateTestSuite()
	elif suiteName == 'Delete':
		suite = DeleteTestSuite()
	elif suiteName == 'All':
		suite = AllTestSuite()
	else:
		print "Valid Tests are %s" % validTests
		sys.exit( -1 )
	unittest.TextTestRunner().run( suite )
