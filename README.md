
GENERAL INFORMATION
----------------------
This program was written to take the place of a Journaling program I used some years back named RoboJournal. It was a database driven program that stored all journal entries in a backend MySQL database. At some point around 2019 the developer of that program stopped active development and support of the program. Subsequently it was no longer available for most Linux distros after 2019. That program was very clean, simple and easy to use. I've made every concious effort to keep this program similar to that one. Basic and easy to use. At the time of this writing the program is at the beta stage at its current version. It is, at this time, stable and usable. Data in and data out with nothing fancy. It's a journaling program after all. Written in Python. While it is possible to use the source code and connect this program to a MySQL database backend, I've designed this program to use SQlite3 and keep the database file local to the program directory. There are plans on my TODO list to give the end user a choice for local (SQLite) database use, or MySQL use on a local or remote server. That is not yet implemented and likely won't be till sometime after version 1.0 release.

The program is primarily designed to be a single user program. That is how I use it, however as this is an open source program if you're confident in your coding skills you can change it to operate however you wish. However, be aware that if you make changes that break things then it is on you to fix said problem. I personally have no desire to make this a multi-user program. It's a journaling program and as such assumes the user wishes to keep their thoughts (entries) private or mostly private.

The compiled elf binary that is included in this repository runs nicely in Linux and should start right up if you download the zip file from Github. I'm working on a self-contained .exe for MS Windows, but it's taking a little longer than expected. The MJournal program was developed using Python 3.9.2. So, the program may work not work with older versions of Python. Python must be installed on your system in order to run the program. When compiling I'm compiling the program into a single file, so the only dependent files are the following:
- cdb
- creds
- dblist
- firstrun
- *.json
- *.db

The files mentioned above should be in the root of the program directory along with the MJournal binary file. There is a setup script I'm working on the create a desktop shortcut, but till that's done you may have to make a shortcut the old fashioned way: manually. No portion of the program or setup script (later) will create a menu item in the Launcher menu (in Linux), or the start menu in windows. You just download the package from Github and run the program. Eezy Peezy!

GENERAL OPERATION
-----------------------
Once the program is completely setup you'll notice in the left pane of the main window a tree menu where entries are displayed. The very first entry is preloaded at setup so that the menu will function. Without that entry the program will not run. By default the tree menu is displayed in expanded mode. You can, of course calapse the nodes, but the menu expanded is set at run time. I have, on my development TODO list, an entry that will track the state of the tree menu, but for now it always loads expanded. Newest entries at the top, oldest at the bottom. To load an entry all you have to do is click on the node for that entry and it loads in the view on the right side of the main screen.

The tree menu displays entries in nodes. Parent node is Year, with children and grand-children nodes month and then day of the month the entry was made. The final node displayed contains the day of the month, title, time of day and the entry id. Those last two items are displayed to give the user a frame of reference. Especially the time of day. Because of the entry ID value you can have multple entries on the same day.

The the right of the tree menu is where entries are made and viewd. (there is also a new entry screen under the file menu just in case. at least for now while the program is still in the beta stage.) This area of the main screen contains elements for Entry Title, Body, a row of Function buttons, an input field for searching entries and a method to choose a different database to use. I've included that mainly because that is something I use a lot. I have a database for personal entries and a database for development. As I'm working on getting this program to version 1 that database is seeing a lot of action so I can track my TODO list and changes that are being made. Since getting the program to a reasonably stable place where its quite usable, I'm constantly adding features to it. Things that need to be there. Creatiing new database and being able to change from one databae to another was the first major addition. The search feature was the second. And so it goes...

There is a HOWTO file that talks about how to operate and get around in the program, however hopefully I've constructed things in a manner that is inutitive and easy to use.


QUIRKS AND ISSUES
-------------------------
-	UPDATE ENTRY CLOSES PROGRAM: (10.15.22) verion 0.7.5.9: something is causing the program to simply exit with exit(0) after it's been sitting for a while. A while being longer than 30 minutes. The event triggering this program exit is hitting the update entry button to send an entry update back to the database. Added a function button in the button row to allow the program to be reloaded if it's been sitting for a while in an attempt to off-set this condition until I can understand and fix what's causing this.
--	10.17.22: this issue is being addressed. So, with any luck. soon I'll be able to remove this quirk from the list!

