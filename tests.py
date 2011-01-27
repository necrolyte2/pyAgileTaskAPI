#!/usr/bin/env python

import unittest
from AgileTaskAPI import AgileTaskAPI

class APITests( unittest.TestCase ):
	def setUp( self ):
		self.api = AgileTaskAPI( 'CLOrJlYa5Ny02fs-F8Zz' );
		self.alltasks = self.api.GetAllTasks()
		self.singleID = self.alltasks[0]['task']['id']

	def _isList( self, item ):
		return type( [] ) == type( item )

	def test_json_decode( self ):
		""" Tests a simple json string to make sure it decodes correctly """
		jsonString = '[{"hello":1}]'
		json = self.api._decodeJson( jsonString )
		self.assertTrue( len( json ) == 1 )

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
		try:
			self.api.GetSingle( "henry" )
		except ValueError, e:
			self.assertEqual( e[0], "ID must be an integer value > 0" )

	def test_getsingle_no_task_for_id( self ):
		""" Should return empty list when there is no task for an id """
		self.assertEqual( self.api.GetSingle( 0 ), [] )

	def test_getsingle_good_id_given( self ):
		""" Should return a list representation of the task's json object """
		task = self.api.GetSingle( self.singleID )
		self.assertTrue( type( task ) == type( {} ), "The task has to be a dict" )
		self.assertTrue( len( task ) == 1, "The task has to be length 1" )

	### Tests for AddTask

	### Tests for UpdateTask

	### Tests for DeleteTask

if __name__ == '__main__':
    unittest.main()
