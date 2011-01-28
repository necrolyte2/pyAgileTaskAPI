#!/usr/bin/env python

import unittest
from AgileTaskAPI import AgileTaskAPI
import sys

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
	""" Tests all Get Methods """
	def setUp( self, *args, **kwargs ):
		super( GetTestCases, self ).setUp( *args, **kwargs )
		self.alltasks = self.api.GetAllTasks()
		self.singleID = self.alltasks[0]['task']['id']

	### Tests for GetAllTasks

	def test_getalltasks_good( self ):
		""" Should return all tasks as a list """
		# Should be a list
		self.assertTrue( self._isList( self.alltasks ) )

	### Tests for GetCompleted

	def test_getcompleted_good( self ):
		""" Should return all tasks as a list """
		# Should be a list
		self.assertTrue( self._isList( self.api.GetCompleted() ) )

	### Tests for GetIcebox

	def test_geticebox_good( self ):
		""" Should return all tasks as a list """
		# Should be a list
		self.assertTrue( self._isList( self.api.GetIcebox() ) )

	### Tests for GetToday

	def test_gettoday_good( self ):
		""" Should return all tasks as a list """
		# Should be a list
		self.assertTrue( self._isList( self.api.GetToday() ) )

	### Tests for GetAchievements

	def test_getachievements_good( self ):
		""" Should return all tasks as a list """
		# Should be a list
		self.assertTrue( self._isList( self.api.GetAllAchievements() ) )

	### Tests for GetRecentAchievements

	def test_getrecentachievements_good( self ):
		""" Should return all tasks as a list """
		# Should be a list
		self.assertTrue( self._isList( self.api.GetRecentAchievements() ) )

	### Tests for GetSingle

	def test_getsingle_bad_id_given( self ):
		""" GetSingle raises exception on bad input """
		self.failUnlessRaises( ValueError, self.api.GetSingle, "henry" )

	def test_getsingle_no_task_for_id( self ):
		""" Should return empty list when there is no task for an id """
		self.assertEqual( self.api.GetSingle( 0 ), [] )

	def test_getsingle_good_id_given( self ):
		""" Should return a list representation of the task's json object """
		task = self.api.GetSingle( self.singleID )
		self.assertTrue( type( task ) == type( {} ), "The task has to be a dict" )
		self.assertTrue( len( task ) == 1, "The task has to be length 1" )

class AddTestCases( BaseTests ):
	### Tests for AddTask
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

	def test_addtask_complete_good( self ):
		""" Should add a task to the icebox list """
		task = self.api.AddTask( "This task should go into completed", complete = 'true' )
		# Make sure we are getting a dict back
		self.assertTrue( type( task ) == type( {} ), str( task ) )
		# Length has to be 1
		self.assertEqual( len( task ), 1, str( task ) )
		# complete is false
		self.assertTrue( ( task['task']['complete'] ) )

	def test_addtask_bad_id( self ):
		""" Should raise an exception from bad position value """
		self.failUnlessRaises( ValueError, self.api.AddTask, name = "This should not be added", position = 'henry' )

	def test_addtask_bad_icebox( self ):
		""" Should raise an exception from bad value for icebox """
		self.failUnlessRaises( ValueError, self.api.AddTask, name = "This should not be added", icebox = 'BadValue' )

	def test_addtask_bad_completed( self ):
		""" Should raise an exception from bad value for completed """
		self.failUnlessRaises( ValueError, self.api.AddTask, name = "This should not be added", complete = 'BadValue' )

	def test_addtask_bad_name( self ):
		""" Should raise an exception if bad things are given in the name """
		pass

class UpdateTestCases( BaseTests ):
	### Tests for UpdateTask
	pass

class DeleteTestCases( BaseTests ):
	### Tests for DeleteTask
	
	def test_deletetask_bad_id_given( self ):
		""" Raises exception on bad input """
		self.failUnlessRaises( ValueError, self.api.DeleteTask, "henry" )

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
	else:
		print "Valid Tests are %s" % validTests
		sys.exit( -1 )
	unittest.TextTestRunner().run( suite )
