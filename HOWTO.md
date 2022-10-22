MJOURNAL HOWTO

Summary
-------------------------
This will be a brief description that will hopefully make things easier to do just case something isn't clear from the start. The MJournal program is laid out in a manner that makes things quickly and easily accessible. Hopfully intuitive as well. When you first open the program the two most obvious features are the tree menu system and the Entries input and view... left and right respectively. Under the tree menu is Tux, the Mascot. If you're running on Windows, well, you've got a different Mascot image. If you're running this on windows this is what software used to operate like. Fast, clean and unencumbered. There are no fancy hooks to this or that... no APIs or anythting fancy. There's just the program and the data you generate with it. So... on with it. I'm listing the items of common operation in the order in which they're typically used.


HOT KEYS
-------------------------
I wanted to put these near the top of the HOWTO file because they're important and if you like using them then, like me, you're going to want the reference to them quick, fast and in a hurry. It may take a bit of time to remember what they are so I wanted to make sure that the list of them and what the do is easily and quickly accessiuble.
- F1: opens this howto file
- F4: Insert Date/Time value into the New/Update Entry
- F5: Update Entry
- F8: New Entry Window
- F9: Database Maintenance
- F11: Reload Tree Data (tree menu)
- F12: Exit the program.


THE TREE MENU
-------------------
As I mentioned before this is one of two items instantly noticable when you open the screen. When you first start using the program it will have only one entry which is pre-loaded. The tree menu will not operate with out something to display thus the program will not run. As such, the tree menu, at first is a lot of empty space. Clicking in the empty space will cause a popup error to greet you. This is normal and can be safely ignored. It happens because your menu is quite empty. To stop the error fill up the menu with entries. Or, simply don't click the empty space. :)

Description:
The tree menu is comprised of nodes. 
Top Level - year
 |Second Level - month of that year
   |Third Level - entry on the day of the month of the year
	 (you can have as many entries in a day you wish. They all have unique record IDs to keep things sane)

The Year and Month nodes are calapsable. The default setting when the program opens is to expand all. 

Operation:
To view an entry simply click on that entry. They're display as day of the month, title, time and entry record ID. The content of that entry and it's title will be displayed on the right side of the main screen.

CLEAR SCREEN
-----------------------
There is a row of buttons in the Functions section of the main screen labeled "Clear Screen". It does exactly that: What ever is in the title field and the entry view of the main screen (those two elements to the right of the tree menu) is cleared out of those two areas. It's not gone... Those areas have simply been cleared. Remember, what ever you see on the screen that is displayed by clicking an item in the tree menu exists in the database and is being displayed there for reading. If you clear the screen you're not getting rid of anything. You're simply making room for what comes next. 

CREATE AN ENTRY (QUICK ENTRY)
----------------------------
So, you've cleared the screen. Not the title field and View are empty. Start typing! Type in a title then tab down into the view field and type your journal entry to your hearts content. When you're finished click the Save Quick Entry button. 

!!!CAUTION!!! Neither the quick entry screen or the New Entry screen are stateful which means if you're typing in an entry and happen to click on a previous entry to look for something, everything you previously type is gone! I know... I've done this myself a few times while developing this and I'm working on it. In a future version of the program - on my TODO list - I'll make a way to save for a time and unfinished entry so the user can go back and not lose what they've already typed in. It's a process...

New Entry Window
The other, slightly safer method of making a new entry is to use the new entry screen found directly under the File menu. This opens an independent window from the main window. 

TAGS
------------------
Tags are just that... descriptive words related to some content. You can use them or not use them. If you do include tags with your journal entries they should be separated by a comma. It doesn't matter if there's a space in there with the comma, but the comma must be there other wise it just becomes a string of word that lower the efficiency of the search.

SEARCHING ENTRIES
-------------------
In the search field just below the function buttons you can search by title, body, tags or all. Title, Body and Tags is obvious. Those are the database fields that will be the target of the search terms. However if you choose ALL, then the program will apply your search terms to all those fields and return what it finds as nodes in the tree menu. The search terms are not case sensitive therefore tags are not either. For instance... if I have a journal entry about a TODO item in my development journal, which I use while coding programs, I often put TODO in the title with some other information. If I do a search on TODO as it appears in the title the case makes no difference. I capitalize it for me rather than the program. It catches my eye faster. The dropdown to the right of the search terms field is where you'll find the dropdown menu for targeting your search. The search terms field is bound to the ENTER key so you can hit enter or press the GO button to begin your search.


SEARCH RESULTS SCREEN
----------------------
The search results are returned to a secondary window that looks much like the main window. It has the tree menu and the input and view pane with a pair of function buttons: Update Entry and Exit. I placed the Update Entry button on the search results screen because I found most of the time I was searching for something was because I wanted to make an update to the entry. So, viola! there it is.

These next few features started out as an idea that quickly became a must-have. At least for me. As I mentioned in the README the journaling program I used to use that I really liked, RoboJournal, worked great, but there were some glaring shortcomings.
- it would backup the journal entries, but only as HTML or text.
- it would NOT make standard SQL backup files or dumps which is so stinking easy I can't tell ya.
- it was able to make new databases but connecting them to the program or switching between them was a little combersome. 
When it because apparent that I wasn't going to be able to use the program in distros released after 2019 I had to resort to running an older version of Mint in a VM just to keep using the journal program. No longer! I've made that all as simple as possible. One of the biggest reasons the program uses SQLite by default.

CREATE NEW DATABASE
---------------------
Under Settings in the menu bar there is a menu item "Make New Database". It's a simple screen. You just type in the name you want to use and press the button. When accessing this screen I had to choose to reload or not reload the program. If you create a new database then the program needs a restart to load the dropdowns with to include the new database. I know... there are other ways, but it's beta right now. I'm going for light-weight and ease of use here. So, for now it's a program restart just to be on the safe side. Takes all of two seconds.

SWITCH DATABASE
--------------------
I personally use this feature a lot. I keep a personal journal and a development journal for projects. So, while I spend most of my time in the one I use for development I can switch database at the drop of a hat. The control is at the bottom of the main screen. Create a new database and you can switch from one to the other quickly and easily.


DATABASE MAINTENANCE
---------------------
This screen has a lot more going on with it.
Left Column
- manual database backup
- choose the databse to backup
- remove a database
- attach a database
Right Column (Linux Only)
- Schedule backup by creating a crontab entry in the users' crontab. (this makes use of a bash script that is called by the cron job which in turn calls the dbbackup.py script to preform the actual backup of the database(s)). These backups are portable because they're created like normal SQL dumbs.

/Manual Database Backup/
Just as the name suggests this is a manual process in that you choose the folder you wish to save the backup to, then choose the database you want to backup and click the Create Backup button. The database backup files that are created use a date/time stamp in the file name as well as the database name. (when running on a cron job they can and will accumulate over time... more on that later.)

/Remove Database/
This function does not actually delete the database, but rather removes the entry of the database in the dblist file which gets read by the program when it starts. The actual database file remains. The draw back is that unless you're running daily backups of the computer where you're using this program then those detached datbases are not getting backed up either manually or automatically via cronjob.

/Attache Database/
When I added this feature I was thinking about re-attaching previously detached database via Remove Database. Then I realized that this might of use importing data from other sources but only if the data lines up with the format of the databases used by this propgram. As I began to code this program the first thing I had to do was map out and create the databases it was going to use. I modeled them after the ones that were created by the other journaling program that used MySQL, rolled by own script to bring the data from MySQL into SQLite. All that being said the primary function of this feature is to re-attach previously detached databases made by this program.

/Scheduled Backups/
If you're unfamiliar with cronjobs or crontabs or the like I've attempted to make this as easy as possible. There are five distinct values to choose from:
- Minutes 0-59,*
- Hours 0-23,*
- Day/Month 1-31,*
- Month 1-12,*
- Day/Week 1-7,*
First, the asteric is a wild card and stands for "any" or more accurately "every". The very last thing you want to do is leave them with their default settings. You'd be constantly running the cronjob and backing up your database(s).

If you wanted to run a daily cron job to backup your databases at 11:15pm ever evening your choices would like like this
Min 	Hrs		Day/Mon 	Mon 	Day/Week
15		23		  *			 *			*

So, your scheduled backup would start at 11:15 or 23:15 every day of the week, ever day of the month and every month of the year. If you wanted your backups to only run once a week the entry would look like this if we're going to run on Friday at 6pm
Min 	Hrs		Day/Mon 	Mon 	Day/Week
 0       18       *          *         5		week days numbered from 0-6
												sun = 0 -- sat = 6
												

CHANGING THEMES
Due to the extremly flexible nature of the GUI library that I use to create the graphical interface for this program - a HUGE shout out to the creator of PySimpleGUI - part of that library is dedicated to changing the look of the program. Under Settings in the file menu there is a selection labeled Program Settings. Clicking there will open a small screen with two items:
1. Program Theme 
2. Program Security

/Program Theme/
The combo menu here has an entire boat load of different color and font settings to choose from. I have the program setup to use my personal favorite by default but you should feel free to check them out and find the one that fits you best.

/Program Security/ 
IT IS STRONGLY RECOMMENDED THAT YOU NOT TOUCH THIS ONE _UNTIL_ YOU FIRST SET A USERNAME AND PASSWORD FOR THE PROGRAM. Turning on the program security BEFORE setting a username and password will lock you out. So, I'll talk about that now and come back to this.


SET USER PASSWORD
This setting is also found under the menu item Settings. Click Set User Password under Settings and a small screen will appear preloaded with your linux system username. Input a password and click ok. This setting is on a per database basis. Meaning, if you have two database, and databaseA has no username/password set and security turned off then you can switch right into it. Or anyone for that matter that runs the program. If databaseB has a username and password set and user security turned on then a username and password is required to open that datanase. Even after the username and password are set you can turn it on and off under Setting->Program Settings and choosing the value 1 from the second drop down to enable security. The password is hashed when provided the first time and the hashed value is what is stored in the database. When in use the hashes are compared for authentication. The password is never in plain text.


*A WORD OF CAUTION*
In the event that you forget your database password and you don't know how to get connected to the SQLite database you have a few options.
1. there is a file in the src folder that describes how to connect to SQLite from the command line, however you have to have the command line tools package(s) installed on your system. Essentially what you'd have to do is drop the user table from the database and then recreate it. You can't just drop that table and "hope" everything will be ok. The definition for the table is in the source code inside the dbsetup.py file.
2. you can contact me via email, mdw1982@gmail.com and request a script that will do the job for you. Its not a hopeless situation but if you find yourself in that postition all is not lost. Also, it's worth mentioning that this security feature is not to be considered robust. Anyone with the right tools and skillset could defeat this security. It's merely meant to stop the casual snooper from reading through your journal entries uninvited.


And last but not least... 

UPDATE ENTRIES
There are lots of times I simply want to update an existing journal entry rather than creating a new one that is related directly to one that already exists. I do this a lot more in my development journal than my personal one, but then that allows me to track changes on projects more easily. It's really quite simple: select the entry you want to update from the tree menu, click it to load it into the right side of the screen and drop your cursor in where you want to start your update.

Oh wait... wouldn't it be nice if you could "insert" the data and time that you're making this update? Well, under the edit menu there is an item labeled Utilities and under that there is a selection labeled Insert Date/Time. One thing I haven't figured out yet is how to get it to insert where your cursor is, but i'll get there. At the moment it inserts the date/time string at the bottom of the text view. There ya go! Bob's yer Uncle.


Don't forget to have a look at the Quirks and Shananegans section of the README file.
