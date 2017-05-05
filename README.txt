for UNIX/LINUX environment:

Execution steps:

1. First resolve the dependencies by running the 'requirements.txt' through a packaging solution like pip.
Command is 'pip install -r requirements.txt'

2. Move to the tradediff folder.

3. Run the trade_diff.py from the console.
Command is 'python trade_diff.py'

4. The packaged solution can be privately shared which is available in the dist folder.

5. To make the package publicly available, follow following steps.
	5.1. Run the command from console, 'python setup.py register'
	5.2. You will be given the following options.
		 1. use your existing login,
		 2. register as a new user,
		 3. have the server generate a new password for you (and email it to you), or
		 4. quit
		Select any one of them.

6. You can also create a windows installable file using the setup.py. Run the below command to create a installable by the name 'bdist_wininst'.
	'python setup.py sdist bdist_wininst upload'


