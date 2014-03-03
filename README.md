Initial Setup
-------------------------
1. Install the project requirements using pip
	
	```pip install -p -r requirements.txt```

	Note: Make sure you are in the project directory

2. Install other requirements from the appropriate sources
	* MySQL
	* Gitflow	
3. Login as the root user into MySQL client. (Use the password specified during setup)

	```mysql -u root -p```

4. Create a database named 'newstrolley' and user named 'django'

	```
	CREATE DATABASE newstrolley;
	GRANT ALL ON newstrolley.* TO django@localhost IDENTIFIED BY 'newpassword';
	```

5. Create a file called 'localsettings.py' in the same directory as 'settings.py' and add the following:
	
	```
	import sys

	#Change the following variables to your requirements
	PROJECT_ROOT_DIR = 'main/project/dir' #The directory that contains manage.py

	if 'test' in sys.argv or 'nt_test.py' in sys.argv:
		DB_NAME = PROJECT_ROOT_DIR + 'nt.db'
		DB_USER = ''
		DB_PASSWORD = ''
		DB_ENGINE = 'sqlite3'
	else:
		DB_NAME = 'newstrolley'
		DB_USER = 'django'
		DB_PASSWORD = 'newpassword'
		DB_ENGINE = 'mysql'

	#Leave as-is during development. Only used while deploying to server. DO NOT CHANGE THE FOLLOWING
	DEBUG = True
	DB_HOST = ''
	STATIC_ROOT = ''
	ALLOWED_HOSTS = []
	EMAIL_HOST = 'localhost'
	EMAIL_HOST_USER = ''
	```
	Note: Do not make any changes to settings.py. These are the only settings you must change

6. Sync the database

	```python manage.py syncdb```

7. Load the database with sources

	```python load_db.py```

8. Test to see if the project is working properly

	```python nt_test.py```

	Note: Always use this to test the app. It tests the apps in a specified order. 

Workflow
--------
The following will be our basic workflow:

1. Create a new feature

	```git flow feature start my-feature```

	-- Work on the feature --

	NOTE: While working on the feature, follow normal git workflow like:
	
	```
	git add .
	git commit -m "My commit message"
	```

2. Share it if collaboration is required (This will push the feature to Github)

	```git flow feature publish my-feature```

3. Finish the feature if successful, or discard if unsuccessful

	```git flow feature finish my-feature (Merges the feature branch with develop)```

	or
	
	```
	git checkout develop
	git branch -D feature/my-feature (Deletes the feature branch)
	```

4. Push the changes to Github (This will be done only after you have finished the feature. Otherwise, just share the feature as in step 2)

	```git push -u origin develop```

5. Repeat 1-4 until desired features are done

6. Release the updates

	```git flow release start release-name```

	-- Make minor tweaks and changes --

	```git flow release finish release-name```

Please note that all work will be done on 'develop' branch. So, push the changes as follows: 
	```git push -u origin develop```
or pull the changes as follows:
	```git pull origin develop```

'master' branch will only change during release. During all other times we are only working on the 'develop' branch.

NOTE: Please make sure you adhere to the above workflow.
