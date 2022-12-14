
REQUIREMENTS
---------------------
You absolutely must have Python 3 installed on your system if you intend to work with the source code. This was begun on a system using Python 3.9.2, however as I learned more about Python I eventually moved to an OS that had Python 3.10 and 3.11 as it's primary interpreter. That means that if you intend on working with the code you will need to have at least Python 3.10 installed on your system. That being said I haven't met a Linux system yet that doesn't come with Python as part of the OS. Linux systems released within the last few years are going to have Python 3 installed on them. So, getting the binary version of this program setup should be a breeze. 

It may run on 3.8 but I haven't tested it. It's likely that I won't. Most modern operating systems are running at least 3.8 if not higher. If you're running Linux just pop open a terminal and check to see if Python is install: "python --version" or "python3 --version". That will give you a return of the version installed on your system. If you don't get a return telling you the version then it's likely it's not installed. Use your distro's package manager to install the latest version of Python. If you're running Windows, you can get Python from the Microsoft store or you can download it from https://www.python.org/downloads/windows/ You will want Python 3 Release. For Windows users make sure if you install Python from python.org that when you're installing it you click the check boxes to place python in your path. THAT IS IMPORTANT. For Linux users python will already be in your path. (Pyhon being in the users PATH is why its best to store the program directory in your home directory. Windows users in C:\Users\%UserName%). When you download the package from Github you're getting all the souce code, but you're also getting a self-contained compiled binary program that has everything it needs compiled into it except the dependent files mentioned below.

The compiled version of the program, whether windows or Linux, does not require Python to be installed on the system. When I compile the program it's compiled as a single file and contains everything it needs to run in one file. There are still dependency files that are program specific, but they are files that the program uses for data storage and the like that are specific to the program's operation. If all you're looking for is the compiled version to run it on your system, then checked the Releases for your platform. There are two program branches. One for Linux and one for Windows.


GRAPHICAL USER INTERFACE or GUI
------------------------------
A special shout out to the wonderful author of PySimpleGUI. Before this project I'd never done anything graphical. Its all been command line stuff in PERL or PHP and Javascript. The author of PySimpleGUI has built a wonder API around Tkinter to such an awesome extent that Tkinter pretty much disappears. At least from my perspective. Check it out here! https://www.pysimplegui.org/en/latest/


FEATURES
-----------------------------
* Tree Menu: easy access to journal entries on the main screen
* View: single click on entry node from tree menu loads the Journal entry to be read.
* Tags: add tags to each or any entry to be searched on
* Main screen Function buttons: intuitive function buttons to aid journal entries
* Entry Search: Search on Body, Title, Tags or all three.
* Multiple Journal Databases: create and use as many or as few as you wish.
* Local Journal Database: no need for connections to remote database servers. Journal Databases are SQLite database and local to the program. They live in the same directory as the program
* Switching Databases: easily switch from one database to another in mere seconds.
* Journal Entry Security: prevent people who have access to your computer from reading your journal by setting a username and password on a per database basis. Once set and enabled, the program will not open the database without the proper authentication.
*  Enable/Disable Journal Security: The user has the ability to turn on and off password protection for a specific database.
* Changing Password: The program provides the user the ability to not only set a password for a specific database, but then to also change that password.
* Easily Create New Databases: Create new Journaling database without needing to know how. Just give it a name and off you go.
* Insert Time and Date: insert time and date into journal entries. Comes in real handy when making updates to existing entries.
* Database Backups: Easy manual and scheduled backups can be performed without knowing the technical details of how it's done. Both manual and scheduled backups.
* Detach and Reattach Database files: Rather than delete databases, the program has the ability to remove active database files from the program so they don't show up on the available database list. The can later be added back onto the list for access.
* Program Theming: the program has the ability to change its look and feel in regards to color scheme.
* Open Source: as open source software you have the ability to make what ever changes you deem necessary to suite your needs.
* Remove Entries: Rather than actually remove a journal entry you can hide or unhide the entry. There is a field in the entry database called visibible. Its default setting is 1 which means its visisble and will be accessible from the tree menu. When you hide the entry that value is set to 0, which means as long as that value is left at 0 it will not be displayed on the tree menu.
* Key Bindings or Hot Keys: Essentially, I've bound some of the Function keys on the keyboard to specific events in the program. Check in the HOWTO file for more information about the hot-keys. I personally find this extremely useful since the less time I have to spend touch my mouse the better I like it.
* Restore from Backup: it is now possible to restore a database from a backup while inside the program.
* More to come!


GENERAL INFORMATION
----------------------
This program was written to take the place (for me at least) of a Journaling program I used some years back named RoboJournal. It was a database driven program that stored all journal entries in a backend MySQL database. At some point around 2019 the developer of that program stopped active development and support of the program. Subsequently it was no longer available for most Linux distros after 2019. That program was very clean, simple and easy to use. I've made every concious effort to keep this program similar to that one. Basic and easy to use. At the time of this writing the program is at the beta stage at its current version. It is, at this time, stable and usable. Data in and data out with nothing fancy. It's a journaling program after all. Written in Python. While it is possible to use the source code and connect this program to a MySQL database backend, I've designed this program to use SQlite3 and keep the database file local to the program directory. There are plans on my TODO list to give the end user a choice for local (SQLite) database use, or MySQL use on a local or remote server. That is not yet implemented and likely won't be till sometime after version 1.0 release.

The program is primarily designed to be a single user program. That is how I use it, however as this is an open source program if you're confident in your coding skills you can change it to operate however you wish. However, be aware that if you make changes that break things then it is on you to fix said problem. I personally have no desire to make this a multi-user program. It's a journaling program and as such assumes the user wishes to keep their thoughts (entries) private or mostly private.

The compiled elf binary that is included in this repository runs nicely in Linux and should start right up if you download the zip file from Github. I'm working on a self-contained .exe for MS Windows, but it's taking a little longer than expected. The MJournal program was developed using Python 3.9.2. So, the program may work not work with older versions of Python. Python must be installed on your system in order to run the program. When compiling I'm compiling the program into a single file, so the only dependent files are the following:
- cdb
- creds
- dblist (now dblist.json)
- firstrun
- *.json
- *.db

The files mentioned above should be in the root of the program directory along with the MJournal binary file. There is a setup script I'm working on the create a desktop shortcut, but till that's done you may have to make a shortcut the old fashioned way: manually. No portion of the program or setup script (later) will create a menu item in the Launcher menu (in Linux), or the start menu in windows. You just download the package from Github and run the program. Eezy Peezy!


GENERAL OPERATION
-----------------------
**Installaton**

Once you've extracted the files from the archive open a terminal window (you don't need to be root, in fact I recommend against it - the program is designed to run and setup in user space). The program directory can be anywhere in your home directory you want it to be, however the best place for it is in the root of your home folder. Anyway, navigate to the program directory in the terminal window and issue this command: "python3 ./setup.py" witout the quotes of course. That command will get the setup process started and when it is finished the program will open with the default database active and ready to go. Thats It! You don't have to run any of the python code directly. The download comes with a pre-compiled binary file. If you're running Linux the binary is simply named MJournal and is found in the root of the program directory. The same goes for the Windows... You should find both in the program directory.The windows binary, or executable file will be named MJournal.exe. Essentially, the setup file moves all the .py files to the src directory and leaves the setup.py and dbbackup.py files in the root of the program directory along with the program support files named above.

Once the program is completely setup you'll notice in the left pane of the main window a tree menu where entries are displayed. The very first entry is preloaded at setup so that the menu will function. Without that entry the program will not run. By default the tree menu is displayed in expanded mode. You can, of course calapse the nodes, but the menu expanded is set at run time. I have, on my development TODO list, an entry that will track the state of the tree menu, but for now it always loads expanded. Newest entries at the top, oldest at the bottom. To load an entry all you have to do is click on the node for that entry and it loads in the view on the right side of the main screen.

The tree menu displays entries in nodes. Parent node is Year, with children and grand-children nodes month and then day of the month the entry was made. The final node displayed contains the day of the month, title, time of day and the entry id. Those last two items are displayed to give the user a frame of reference. Especially the time of day. Because of the entry ID value you can have multple entries on the same day.

The the right of the tree menu is where entries are made and viewd. (there is also a new entry screen under the file menu just in case. at least for now while the program is still in the beta stage.) This area of the main screen contains elements for Entry Title, Body, a row of Function buttons, an input field for searching entries and a method to choose a different database to use. I've included that mainly because that is something I use a lot. I have a database for personal entries and a database for development. As I'm working on getting this program to version 1 that database is seeing a lot of action so I can track my TODO list and changes that are being made. Since getting the program to a reasonably stable place where its quite usable, I'm constantly adding features to it. Things that need to be there. Creatiing new database and being able to change from one databae to another was the first major addition. The search feature was the second. And so it goes...

There is a HOWTO file that talks about how to operate and get around in the program, however hopefully I've constructed things in a manner that is inutitive and easy to use. Apologies ahead of time because the Hot-keys or _Function keys_ are not intuitve until you start using them. A quick check of the HOWTO reminds me which key I've bound to which program functions. The ones I use the most are these:
* F1: displays the HOWTO window
* F4: inserts date/time into the view element where you would normally make an update to an entry. (it always goes to the bottom of the text in that element.)
* F5: submits an update - THIS IS IMPORTANT - while making an update if you trigger ANY other event in the program your update will be lost. _I'm working on a way to prevent this._
* F7: opens the debug window that allows you to see what's going on under the covers when an event is triggered.
* F8: opens New Entry Submission window and F5 will submit the new entry.
As there are only 12 F-keys available I'm assigning them as judicially as possible. As I've mentioned before, the fewer times I have to touch my mouse the better I like it.

**Backups**
* On the left side Database Maintenance screen it is possible to perform manual backups of your database files. It's pretty simple. You simplly click the browse button, choose the folder you wish to store the backup in, then choose the datbase to backup, then click **Create Backup**. The browse button will open the file dialog window on the backups folder by default, but you can navigate anywhere you'd like to save your backup.
* _any time you're working in the Database Maintenance window and you do or don't perform and operation, when you clock the quit button to close that window the program starts... at this time that is to ensure that **if** you detached any databases the database list on the main screen is properly reloaded. that only happens at program startup._
* _Linux Users_: on the right side of the Database Maintenance window there are options to create a cron job and the accompany startup.sh file. This process is automated so all you have to do is decide the time of day you wish for the automatic backups to happen. At this time you don't have a choice of where these backups get stored. The default is the backups folder inside the program folder.
* _Windows Users_: There are plans to create the functionality to utilize scheduled tasks to handle automated backups of your databases. That likely won't happen until the program reaches version 0.8.0.0.

RUNNING THE PROGRAM IN DEBUG MODE
---------------------------------
Technically speaking there isn't a DEBUG mode... however, if you run the program from the command line you'll see the standard output as well as any error output if/when an error happens. So, if you're experiencing some weirdness or instability in the program this is the best way to capture the information.


QUIRKS AND SHENANIGANS
-------------------------
Any quirks you may experience in the program are likely the result of this being my first Python project. Please open an issue on my Github page to let me know what's going on so I can focus on it and provide a solution. This is my daily driver program and runs on my desktop continuously. That being said its possible I may miss something. So, let me know.
* **non-responsive menu items:** you may find a few of these things in the menu bar. The cause for this abhorrent behavior stems from moving to the structured pattern matching which replaced the if/elif/else statements in the event loop. While making the conversion in the program I concentrated on the actual events in the code and sort of forgot to include the events from the menu bar. I'm fixing this as I find them. 

CHANGE LOG
---------------------------
* **10.21.22** - logging disabled for the near term... everything being sent to standard out while further development moves forward for better debugging.
* **10.24.22** - moved away from using a plain text file for dblist and chose to use a .json file for this using the same file name. this was brought about by a process change involving how the databases are handled by the program. Before, active database were written to the text file dblist in a comma delimited format. this was sloppy at best. using json to write the file is much cleaner and easier to manage. however, now all database files are read from disk using os.listdir and placed into the new dblist.json file. when databases are removed from the active list or _detached_ they're actually moved to a sub-folder of the program root: olddb. Attach Database now looks in that folder for the database file to bring back out, add to active databases (dblist.json). Over all, a much cleaner process and far easier to code for.
* **10.25.22** - accidentally detaching the active database from the program is prevented. I was reminded of the need for checks in that part of the program so I addressed it. It is now impossible to remove (detach) the active database from within the program.
* **10.29.22** - bound Enter key to OK/Submit buttons on sub-screens: program settings, login window, and change password window. Also set auto-close parameter on confirmation popups for these windows.
* **10.30.22** - created two small classes, DBConn and Entry, but the only one in real use right now is DBConn. it's handling the connection to the database, inserts, gets, updates, etc... quite handy and has allowed me to clean up quite a bit of code in the main program. The Entry class was created because I'm looking for a way to prevent entry updates being made from getting lost when the user accidently triggers another event before the update is submitted.
  * Also performed some more code cleanup this evening condensing things a bit by using less code to get a job done. Every little bit helps.
* **10.30.22** - Version: 0.7.7.5 reached.
  * Plans for compiling for windows have been put on hold for now. At least until version 0.8.0.0. More time is required to get the code to a point of being more pythonic in nature to avoid needing to alter a lot of things to make it work as well as avoiding a fork in the project.
  * shrank the main window height to better fit a laptop screen. the main window is find on a desktop monitor, but trying to use the program on a laptop was a real challenge. it fits nicely on the laptop screen now.
* **10.31.22** - DBConn class created. Just a small class with a few methods to create an instance of an object that makes the connection to the active database, handles the gets, inserts, updates and closes the cursor.
* **11.1.22** - first stable version of the program compiled in windows today. There are some bugs to work out but nothing major.
* **11.2.22** - started converting the program over to use the DBConn class. makes things a bit faster but mostly cleans up the code and takes a lot less code to get the job done of data in and data out.
  * current version: 0.7.7.8
  * modified database maintenance screen. because windows has a real problem with the functions for creating crontab entries and the crontab module import, those functions and the import are wrapped in if statements detecting the OS where it's running.
  * increased the height of the new entry window just a smidge so it would appear correctly in windows. the subit and cancel buttons at the bottom of the screen were getting cut off.
* **11.3.22** current version 0.7.8.1 - added error checking for new entry windows in case the title field is left blank. user is warned of the issue and allowed to correct it before submitting the entry.
  * also added a packaging script to handle gathering together all the necessary support files and src files into the dist folder after the program is compile. this script takes one of two arguments: (1) newlist: it will create a new filelist.json file. there is a denylist[] object that can have items added to it so that they're not part of the gathering of file. (2) run: this runs the main part of the script that copies all the support and src files to the distribution folder, then renames the folder and appends the current version to the folder name.
*  **11.3.22** first release posted on GitHub... version: 0.7.8.1. For a Beta release it's quite stable. There's still a lot to do, but the program has a solid foundation. I started this project the last week of Sept. 22 and it's progressed rapidly.
*  **11.4.22** second release posted: version 0.7.8.8..
   * **Change Entry Update** method such that when an entry is selected and update entry is then selected the entry opens in a new window. The primary reason for this was to prevent an entry update from being lost by another event being triggered.
   * **more code cleanup** performed in an ongoing effort to make the program more pythonic in nature and operation. Better for cross-platorm applications.
   * **Still on track** for the version 0.8.8.0 windows release. Should only be a few more days provided I have enough time to get it thoroughly tested.
   * **Added Bread Crumbs** on a few of the function buttons labeled with the corresponding F-key that triggers the event.
* **11.9.22** current version: 0.7.9.5: 
  * **cleaned up the** search results algo that builds the search results tree menu. It now displays correct by Year, Month descending.
  * **Added Restore from Backup** functionality to the program so that a database previously backed up can be easily restored without needing to do it from the command line.
  * **cleanup needed** on the updates sent back to the main screen after an entry is updated. filtering seems to be lacking there. When an update is processed from the update screen it reappears in the VIEW on the main window. As it appears single and double-quotes aren't getting properly converted to human readable. if you click on the entry from the tree menu it displays correctly.
* **11.12.22** current version: 0.7.9.7
  * **Entry Search Function** is finally operating correctly. It was a logic issue and I just had to find the right logic to get things sorted out. Search results are displayed in ascending order.
  * **More Code Clean** performed making the program more pythonic. Approaching the point where I'm more confident about the code compiling on Windows without massaging the code.
  * **Cleanup performed** on updates windows such that all text is displayed human-readable in both the update entry window and the main screen when displaying a journal entry.
* **11.16.22** current version: 0.7.9.9
  * converted program event loop from strung out if/elif/else statements to using structured pattern matching (match/case) statements. required full upgrade of Python from 3.9 to 3.10 and then 3.11. Currently the program is compiled using Python 3.11. Compiled the program is noticeably faster.
  * found and fixed one more bug in the entry search function that involved the program not returning correct results from the search to the screen. Functions responsible for building the record list weren't differentiating between visible and not-visible records. this has been corrected.
* **11.23.22** current version 0.7.9.9
  * found one event that wasn't being handled correctly. this event is triggered from the menu bar and was added in the correct place in the corresponding case statement.
  * program recompiled and posted...
* **11.27.22 cropntab module error** causing program crash. after some research into the error it was discovered that what once worked no longer worked. I suspect this is a result of the change in Python versions. removed generic crontab module usage to python-crontab module which resolved the crash and the error.