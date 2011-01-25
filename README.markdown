# pyAgileTaskAPI

A python wrapper for the AgileTask API

## API's that are working

* http://doc.agiletask.me/get_tasks.html
	* .GetAll()
* http://doc.agiletask.me/get_today.html
	* .GetToday()
* http://doc.agiletask.me/get_icebox.html
	* .GetIcebox()
* http://doc.agiletask.me/get_single.html
	* .GetSingle( *&lt;Task ID&gt;* )

## API's that are being worked on

* http://doc.agiletask.me/get_completed.html
	* .GetCompleted()
* http://doc.agiletask.me/get_achievements.html
	* .GetRecentAchievements()
* http://doc.agiletask.me/get_new_achievements.html
	* .GetAllAchievements()

## API's that are not implemented

* http://doc.agiletask.me/new_tasks.html
	* .AddTask()
* http://doc.agiletask.me/update_tasks.html
	* .UpdateTask()
* http://doc.agiletask.me/delete_tasks.html
	* .DeleteTask( *&lt;Task ID&gt;* )

## Usage
	from AgileTaskAPI import AgileTaskAPI

	patapi = AgileTaskAPI( '<Your Agile Task API Key>' )
	
	for task in patapi.GetToday():
		print task['task']['name']

Would print each task in your Today Task List one per line

### Python Path

You can add the path to pyAgileTaskAPI like this before you import the module

	import sys
	sys.path.append( '<Path to pyAgileTaskAPI folder>' )

