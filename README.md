
REQUIREMENTS
---------------------
You absolutely must have Python 3 installed on your system. This program was written on a system using Python 3.9.2. It may run on 3.8 but I haven't tested it. It's likely that I won't. Most modern operating systems are running at least 3.8 if not higher. If you're running Linux just pop open a terminal and check to see if Python is install: "python --version" or "python3 --version". That will give you a return of the version installed on your system. If you don't get a return telling you the version then it's likely it's not installed. Use your distro's package manager to install the latest version of Python. If you're running Windows, you can get Python from the Microsoft store or you can download it from https://www.python.org/downloads/windows/ You will want Python 3 Release. For Windows users make sure if you install Python from python.org that when you're installing it you click the check boxes to place python in your path. THAT IS IMPORTANT. For Linux users python will already be in your path. (Pyhon being in the users PATH is why its best to store the program directory in your home directory. Windows users in C:\Users\%UserName%). When you download the package from Github you're getting all the souce code, but you're also getting a self-contained compiled binary program that has everything it needs compiled into it except the dependent files mentioned below.


GRAPHICAL USER INTERACE or GUI
------------------------------
A special shout out to the wonderful author of PySimpleGUI. Before this project I'd never done anything graphical. Its all been command line stuff in PERL or PHP and Javascript. The author of PySimpleGUI has built a franework around Tkinter to such an awesome extent that Tkinter pretty much disappears. At least from my perspective. Check it out here! https://www.pysimplegui.org/en/latest/


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
Program Setup

Once you've extracted the files from the archive open a terminal window (you don't need to be root, in fact I recommend against it - the program is designed to run in user space), and go to the program directory. The program directory can be anywhere in your home directory you want it to be, however the best place for it is in the root of your home folder. Anyway, navigate to the program directory in the terminal window and issue this command: "python3 ./setup.py" witout the quotes of course. That command will get the setup process started and then it is finished the program will open with the default database active and ready to go. Thats It!


Once the program is completely setup you'll notice in the left pane of the main window a tree menu where entries are displayed. The very first entry is preloaded at setup so that the menu will function. Without that entry the program will not run. By default the tree menu is displayed in expanded mode. You can, of course calapse the nodes, but the menu expanded is set at run time. I have, on my development TODO list, an entry that will track the state of the tree menu, but for now it always loads expanded. Newest entries at the top, oldest at the bottom. To load an entry all you have to do is click on the node for that entry and it loads in the view on the right side of the main screen.

The tree menu displays entries in nodes. Parent node is Year, with children and grand-children nodes month and then day of the month the entry was made. The final node displayed contains the day of the month, title, time of day and the entry id. Those last two items are displayed to give the user a frame of reference. Especially the time of day. Because of the entry ID value you can have multple entries on the same day.

The the right of the tree menu is where entries are made and viewd. (there is also a new entry screen under the file menu just in case. at least for now while the program is still in the beta stage.) This area of the main screen contains elements for Entry Title, Body, a row of Function buttons, an input field for searching entries and a method to choose a different database to use. I've included that mainly because that is something I use a lot. I have a database for personal entries and a database for development. As I'm working on getting this program to version 1 that database is seeing a lot of action so I can track my TODO list and changes that are being made. Since getting the program to a reasonably stable place where its quite usable, I'm constantly adding features to it. Things that need to be there. Creatiing new database and being able to change from one databae to another was the first major addition. The search feature was the second. And so it goes...

There is a HOWTO file that talks about how to operate and get around in the program, however hopefully I've constructed things in a manner that is inutitive and easy to use.


QUIRKS AND SHANANEGANS
-------------------------
-	UPDATE ENTRY CLOSES PROGRAM: (10.15.22) verion 0.7.5.9: something is causing the program to simply exit with exit(0) after it's been sitting for a while. A while being longer than 30 minutes. The event triggering this program exit is hitting the update entry button to send an entry update back to the database. Added a function button in the button row to allow the program to be reloaded if it's been sitting for a while in an attempt to off-set this condition until I can understand and fix what's causing this.
--	10.17.22: this issue is being addressed. So, with any luck. soon I'll be able to remove this quirk from the list!
-- 	10.18.22: I've narroed down "where" the issue is and now just need to gather a little more information and fix the issue. At least now it doesn't bring down the program, but does prevent the entry update from being carried out. One of those intermittent issues that drive ya nuts.
-	RIGHT CLICK COPY, PASTE, SELECT AND SELECT ALL: There isn't any. Not yet anyway... I've been working hard on getting all the wrinkles smoothed out before tackling that feature, but it's coming. Its one of those things that sounds like it should be easy, but its not. I mean, C'mon... I've only been programming in Python for 3 months and I have a lot more to learn.

