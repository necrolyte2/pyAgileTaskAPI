# pyAgileTaskAPI

A python wrapper for the AgileTask API

## API

* http://doc.agiletask.me/get_tasks.html
	* .GetAll()
* http://doc.agiletask.me/get_today.html
	* .GetToday()
* http://doc.agiletask.me/get_icebox.html
	* .GetIcebox()
* http://doc.agiletask.me/get_single.html
	* .GetSingle( *&lt;Task ID&gt;* )
* http://doc.agiletask.me/get_completed.html
	* .GetCompleted()
* http://doc.agiletask.me/get_achievements.html
	* .GetRecentAchievements()
* http://doc.agiletask.me/get_new_achievements.html
	* .GetAllAchievements()
* http://doc.agiletask.me/new_tasks.html
	* .AddTask( *&lt;name&gt;*, *icebox* = *'true|false'*, *&lt;position&gt;*, *complete* = *'true|false'* )
* http://doc.agiletask.me/delete_tasks.html
	* .DeleteTask( *&lt;Task ID&gt;* )
* http://doc.agiletask.me/update_tasks.html
	* .UpdateTask( *&lt;Task ID&gt;*[, *&lt;name&gt;* [, *&lt;icebox&gt;*[*&lt;position&gt;*[, *&lt;complete&gt;*]]]], *task* = *&lt;Task Object&gt;* )  
		* __Note__: You have to provide either the task object or some combination of name, icebox, position and complete
		* __Note__: *&lt;Task Object&gt;* is a python dictionary representation of a simple task.  
{ 'task' : { 'name' : *&lt;name&gt;*, 'icebox' : *&lt;icebox&gt;*, 'position' : *&lt;position&gt;*, 'complete' : *&lt;complete&gt;* } }

## ToDo

* .MoveTaskToIcebox( *&lt;Task ID&gt;* )
* .MoveTaskToToday( *&lt;Task ID&gt;* )
* .CompleteTask( *&lt;Task ID&gt;* )

## Examples

### Initialize the API

	from AgileTaskAPI import AgileTaskAPI

	patapi = AgileTaskAPI( '<Your Agile Task API Key>' )

### Print Today's Tasks
	
	for task in patapi.GetToday():
		print task['task']['name']

### Add New Task to Top of Today's Tasks

	newTask = patapi.AddTask( 'Super cool awesome task text goes here!', icebox = 'false )

### Update added task's name and move it to the icebox

	newTask['task']['name'] = "Cool task #tyghe is #awesome"
	newTask['task']['icebox'] = 'true'
	oldTask = patapi.UpdateTask( newTask['task']['id'], task = newTask )

#### You can also make an entirely new task with changed values like this

	updatedTaskDef = { 'task' : { 'name' : "Cool task #tyghe is #awesome", 'icebox' : 'false', 'complete' : 'false', 'position' : 0 } }
	oldTask = patapi.UpdateTask( newTask['task']['id'], task = updatedTaskDef )
__Note__: that you have to provide all 4 task keys if you make a task from scratch and update that way

### Delete a task

	deletedTask = patapi.DeleteTask( oldTask['task']['id'] )

## Tips

### Python Path

You can add the path to pyAgileTaskAPI like this before you import the module

	import sys
	sys.path.append( '<Path to pyAgileTaskAPI folder>' )
