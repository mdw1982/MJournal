# MJOURNAL HOWTO
Updated: Sun 17 Mar 2024 09:47:16 AM EDT

Table Of Contents
-----------------

* [Summary](#LinuxDocs:Projects:MJournal:HOWTO#summary)
* [Contributions](#LinuxDocs:Projects:MJournal:HOWTO#contributions)
* [Hot Keys](#LinuxDocs:Projects:MJournal:HOWTO#hot-keys)
* [Main Screen](#LinuxDocs:Projects:MJournal:HOWTO#main-screen)
* [Search Results Display Screen](#LinuxDocs:Projects:MJournal:HOWTO#search-results-display-screen)
* [New Entry Window](#LinuxDocs:Projects:MJournal:HOWTO#new-entry-window)
* [The Tree Menu](#LinuxDocs:Projects:MJournal:HOWTO#the-tree-menu)
* [Tags](#LinuxDocs:Projects:MJournal:HOWTO#tags)
* [Searching Entries](#LinuxDocs:Projects:MJournal:HOWTO#searching-entries)
* [Search Results Screen](#LinuxDocs:Projects:MJournal:HOWTO#search-results-screen)
* [Create New Database](#LinuxDocs:Projects:MJournal:HOWTO#create-new-database)
* [Switch Databases](#LinuxDocs:Projects:MJournal:HOWTO#switch-databases)
* [Database Maintenance](#LinuxDocs:Projects:MJournal:HOWTO#database-maintenance)
	* [Left Column](#LinuxDocs:Projects:MJournal:HOWTO#left-column)
	* [Right Column](#LinuxDocs:Projects:MJournal:HOWTO#right-column)
* [Manual Database Backup](#LinuxDocs:Projects:MJournal:HOWTO#manual-database-backup)
* [Remove Database](#LinuxDocs:Projects:MJournal:HOWTO#remove-database)
* [Attach Database](#LinuxDocs:Projects:MJournal:HOWTO#attach-database)


#### Summary
This will be a brief description that will hopefully make things easier to do just in case something isn't clear from the start. The MJournal program is laid out in a manner that makes things quickly and easily accessible. Hopfully intuitive as well. When you first open the program the two most obvious features are the tree menu system and the Entries iview... left and right respectively. Under the tree menu is Tux, the Mascot. If you're running on Windows, well, you've got a different Mascot image. If you're running this on windows this is what software used to operate like. Fast, clean and unencumbered. There are no fancy hooks to this or that... no APIs or anythting fancy. There's just the program and the data you generate with it. So... on with it. I'm listing the items of common operation in the order in which they're typically used. 

As was mentioned in the README when you get this program as a package you're getting the compiled binaries:

* MJournal
* dbbackup
* setup
* Unlock


I was originally including the source files with the program package but stopped since it just added clutter to the program directory file tree. So, if you want the source code its easily available at <https://github.com/mdw1982/MJournal.>
Download the source zip and get to hacking to your hearts content. I would keep it separate from your working program though unless and until you're certain you've got the bugs worked out and you're satisfied with the results. If you want to include your new code into the existing program simply compile the main.py code and replace the original binary in the program directory with the one you've just compiled. It really is that simple. Just know that any changes you make are on you so be careful to retain the previous binary in case something blows up.

#### Contributions
If you wish to contribute to this project I welcome it. Please see the Contribute.md file included with the package. If its not there shoot me an email and request a copy.

#### HOT KEYS
I wanted to put these near the top of the HOWTO file because they're important and if you like using them then, like me, you're going to want the reference to them quick, fast and in a hurry. It may take a bit of time to remember what they are so I wanted to make sure that the list of them and what the do is easily and quickly accessible. 

#### Main Screen
F1: opens this howto file
F4: Insert Date/Time value into the New/Update Entry
F5: Update Entry
F6: Make New Database
F7: opens debug window (downside is that if the program crashes this window will close too)
F8: New Entry Window
F9: Database Maintenance
F11: Reload Tree Data (tree menu)
F12: Exit he program.

#### Search Results Display Screen

F1: opens HOWTO
F4: Insert Date/time
F5: Update Entry - for those occassions when you search for an entry and make an update to it.
F11: Reload Tree Data
F12: close search results window

#### New Entry Window
F5: submit new entry

#### THE TREE MENU
As I mentioned before this is one of two items instantly noticable when you open the screen. When you first start using the program it will have only one entry which is pre-loaded. The tree menu will not operate with out something to display thus the program will not run. As such, the tree menu, at first is a lot of empty space. Clicking in the empty space will cause a popup error to greet you. This is normal and can be safely ignored. It happens because your menu is quite empty. To stop the error fill up the menu with entries. Or, simply don't click the empty space. ☺ It doesn't look like much, but the tree menu was not an easy task. The difficulty building the tree menu and getting it to work correctly is deceptively hidden in it's simple appearance and I'm quite proud of the accomplishment considering this program is my first serious python effort not to mention my first ever GUI/event driven program.

Description: The tree menu is comprised of nodes. Top Level - year |Second Level - month of that year |Third Level - entry on the day of the month of the year (you can have as many entries in a day you wish. They all have unique record IDs to keep things sane)

The Year and Month nodes are calapsable. The default setting when the program opens is to expand all.

Operation: To view an entry simply click on that entry. They're display as day of the month, title, time and entry record ID. The content of that entry and it's title will be displayed on the right side of the main screen.

New Entry Window The new entry screen found directly under the File menu or by using the F8 key opens an independent window from the main window. In this window you can make new Journal entries. When you're finished hit F5 to submit your entry or click the submit button.

#### TAGS
Tags are just that... descriptive words related to some content. You can use them or not use them. If you do include tags with your journal entries they should be separated by a comma. It doesn't matter if there's a space in there with the comma, but the comma must be there other wise it just becomes a string of words that lower the efficiency of the search.

#### SEARCHING ENTRIES
In the search field just below the function buttons you can search by title, body, tags or all. Title, Body and Tags is obvious. Those are the database fields that will be the target of the search terms. However if you choose ALL, then the program will apply your search terms to all those fields and return what it finds as nodes in the tree menu. The search terms are not case sensitive therefore tags are not either. For instance... if I have a journal entry about a TODO item in my development journal, which I use while coding programs, I often put TODO in the title with some other information. If I do a search on TODO as it appears in the title the case makes no difference. I capitalize it for me rather than the program. It catches my eye faster. The dropdown to the right of the search terms field is where you'll find the dropdown menu for targeting your search. The search terms field is bound to the ENTER key so you can hit enter or press the GO button to begin your search.
**Note:** for some reason that I haven't given a lot of priority to the search results are listed from oldest to newest downward. In other words the oldest result is listed first and the newest last. I'm pretty certain it's a sorting issue in the code, however it was a REAL bear just getting the tree to build so, I'll tackle the sort at a later date.

#### SEARCH RESULTS SCREEN
The search results are returned to a secondary window that looks much like the main window. It has the tree menu and the input and view pane with a pair of function buttons: Update Entry and Exit. I placed the Update Entry button on the search results screen because I found most of the time I was searching for something was because I wanted to make an update to the entry. So, viola! there it is.

These next few features started out as an idea that quickly became a must-have. At least for me. As I mentioned in the README the journaling program I used to use that I really liked, RoboJournal, worked great, but there were some glaring shortcomings.


* it would backup the journal entries, but only as HTML or text.
* it would NOT make standard SQL backup files or dumps which is so stinking easy I can't tell ya.
* it was able to make new databases but connecting them to the program or switching between them was a little combersome.


When it became apparent that I wasn't going to be able to use the program in distros released after 2019 I had to resort to running an older version of Mint in a VM just to keep using the journal program. No longer! I've made that all as simple as possible. One of the biggest reasons the program uses SQLite by default.

#### CREATE NEW DATABASE
Under Settings in the menu bar there is a menu item "Make New Database". It's a simple screen. You just type in the name you want to use and press the button. When accessing this screen I had to choose to reload or not reload the program. If you create a new database then the program needs a restart to load the dropdowns with to include the new database. I know... there are other ways, but it's beta right now. I'm going for light-weight and ease of use here. So, for now it's a program restart just to be on the safe side. Takes all of two seconds.

#### SWITCH DATABASE
I personally use this feature a lot. I keep a personal journal and a development journal for projects. So, while I spend most of my time in the one I use for development I can switch database at the drop of a hat. The control is at the bottom of the main screen. Create a new database and you can switch from one to the other quickly and easily.

#### DATABASE MAINTENANCE
This screen has a lot more going on with it. 

##### Left Column

* manual database backup
* choose the databse to backup
* remove a database
* attach a database
* restore database from backup 


##### Right Column
**Windows**
At the moment there is a single button which, when pressed, will open Windows Task Scheduler. After the task scheduler has opened under **Task Scheduler (Local)** you'll see the root folder: **Task Scheduler Library**. It's recommended that you create your task here at the root rather than digging through all the other folders in here. Lets keep things simple. As I develope this program I'll set things up such that all you'll have to do is choose type: daily, weekly, monthly (default: Daily), Time of Day to run backup.

![](./HOWTO_files/pasted_image.png)

1. Open Windows Task Schedule by clicking the button.
2. When Task Scheduler opens click **Create Basic Task** on the right under Actions
3. In the name field type in MJournal Backup... Click Next
4. On the Trigger screen Daily is the default (recommended)... click Next
5. On this page **Start** contains Date and Time. The leave the Date value as is because and change the Time value beside it to the time of day when it's most likely your computer will be running... you don't have to be logged and actively working. Leave the **Recur every** value as 1 if you want it to run everyday. Click Next...
6. Leave the Default value as **Start Program** and click Next
7. On the next page for **Start a Program** click on the Browse button, navigate to the MJournal program folder and seclect dbbackup.exe. Click Next...
8. On the last screen is displayed a summary of your scheduled task.  Near the bottom of the **Finish** screen you'll see a checkbox with the text **Open the Properties dialog for this task when I click Finish**. Please check that box and click Finish.
9. On the next screen select **RUn whether user is logged on or not**. 
10. Click OK... Another dialog box should appear with your Windows Username in the username field. Enter your windows password and click OK. Doing this will give the program permission to run with system (unattended) permissions and requires no further interaction. This is not the MJournal program asking for this information but rather the Windows Task Scheduler and you would see this if you were setting up a completely different task with Task Scheduler. After inputing your password and pressing Enter or clicking OK the setup is done and you're back where you started.

That's it! You've successfully setup a scheduled task to backup your MJournal database(s).

**Linux**
Schedule backup by creating a crontab entry in the users' crontab. (this makes use of a bash script that is called by the cron job which in turn calls the dbbackup program to preform the actual backup of the database(s)). These backups are portable because they're created like normal SQL dumbs.

* **Default values for minutes and hours are set to 0 and 11 respectively**. Early on in development I had these set to * which basically means that if you leave the minutes set to default you'll get a backup made for each database every 60 seconds for the hour you choose for the cron job to run. We don't need that many backups.
* (**Recommended** unless you know what you're doing) leave the minute settings as default and choose the hour value for when you're mostly likely to have your computer running. You won't even notice the backup is/has been run. You can check to verify the backup was run by going to the program directory/backups. Check for an .sql file containing the database name and date in the file name.
* Example: journal.db_2024-05-05_1119.sql


#### Manual Database Backup
Just as the name suggests this is a manual process in that you choose the folder you wish to save the backup to, then choose the database you want to backup and click the Create Backup button. The database backup files that are created use a date/time stamp in the file name as well as the database name. (when running on a cron job they can and will accumulate over time... more on that later.)

#### Remove Database
This function does not actually delete the database, but rather removes the entry of the database in the dblist file which gets read by the program when it starts. The actual database file remains... it is moved to the folder olddb. The draw back is that unless you're running daily backups of the computer where you're using this program then those detached datbases are not getting backed up either manually or automatically via cronjob. Unless, of course, you're doing full system backups. On my linux machine where I'm doing the bulk of development for this program I'm using Timeshift for daily backups which makes a full image of the drive so everything gets backed up. That being said only active databases get exported to an SQL backup file.

#### Attach Database
When I added this feature I was thinking about re-attaching previously detached database via Remove Database. Then I realized that this might be of use importing data from other sources but only if the data lines up with the format of the databases used by this propgram. As I began to code this program the first thing I had to do was map out and create the databases it was going to use. I modeled them after the ones that were created by the other journaling program that used MySQL, rolled by own script to bring the data from MySQL into SQLite. All that being said the primary function of this feature is to re-attach previously detached databases made by this program.

#### Restore Database Backup
If you are storing a copy of your main database it's a good idea to first create a dummy database, switch that database in the program then rename your main database by appending .old to the database you're restoring. Now continue on to restoring your database.

Restoring a database from back choose the database backup using the browse button. The default database name for the restored database will be recover.db. As soon as the database restore has completed you'll be prompted to rename the restored database. Choosing yes will take you to the next screen where you can rename the restored (recover.db) database. it is recommended that you do this immediately after restoring the database. Otherwise you'll have to rename it manually. When renaming the database use a name that hasn't yet been used. In case you do choose a name that already exists you'll be alerted and taken back to the screen to give the recover.db a new name.

Once the restored database has been renamed the program will restart and the recovered database will appear in the database list within the program. If you're satisfied with the datbase restore you may safely move your former database to the olddb folder. Thats pretty much all there is to it. I've attempted to make it as fool proof and easy as possible, however no plan survives first contact. Just go slowly and make sure if you're restoring the current database that you're connecting to that you switch to a dummy.db before renaming the restored database.

#### Scheduled Backups
If you're unfamiliar with cronjobs or crontabs or the like I've attempted to make this as easy as possible. There are five distinct values to choose from:

Minutes 0-59,*
Hours 0-23,*
Day/Month 1-31,*
Month 1-12,*
Day/Week 1-7,*
I attempted to get the formatting correct on how things should look when you're finished editing your crontab, however it doesn't display correctly. So, I'll do the next best thing and provide a link the crontab guru web site Conitor: <https://crontab.guru/> . Here you'll be able to get a pretty fair understanding, if you don't already know, how to choose the correct values for setting your scheduled backups on Linux.
##### Warning
When setting the cron entry you need to be aware to sent a value for minutes which is the left most dropdown item. Failure to do wil result in cron repeating the task many times per hour. I normally set this value to zero. My times settings for the cron entry look something like this:
0   23   *    *   *
So the cron job starts at the top of the 23rd hour and runs once every day, every week and every month of the year. I reckon I should just set the default value for minutes to zero. Hell! I wrote the program and even I overlooked the need to set this value. Also worth mentioning - its a small bug in the code I've yet to identify - after creating the crontab entry, open your crontab with the command **crontab -e** to edit it. For some reason the program enters a blank line above the actual entry. If this is the first item entered into your crontab then the scheduled backup won't run. Remove that blank line and save the crontab. Even if it's not the first entry into your crontab... remove it anyway cause it's messy.

I'm still working on getting a scheduled task for the Windows version included in the program. I'm lazy, I know. You can set one up manually though. Just point the scheduled task at the dbbackup.exe file. The executable will do the rest. No need for command line arguments.

#### CHANGING THEMES
Due to the extremly flexible nature of the GUI library that I use to create the graphical interface for this program - a HUGE shout out to the creator of PySimpleGUI - part of that library is dedicated to changing the look of the program. Under Settings in the file menu there is a selection labeled Program Settings. Clicking there will open a small screen with two items:

Program Theme
Program Security
Program Theme
The combo menu here has an entire boat load of different color combination settings to choose from. I don't yet have the program setup to change to a particular font yet meaning you can't choose a particular system font for the program to use. My priority was to get the program functional and stable before adding bells and whistles.

Program Security
----------------
IT IS STRONGLY RECOMMENDED THAT YOU NOT TOUCH THIS ONE UNTIL YOU FIRST SET A USERNAME AND PASSWORD FOR THE PROGRAM. Turning on the program security BEFORE setting a username and password will lock you out. So, I'll talk about that now and come back to this.

#### SET USER PASSWORD
This setting is also found under the menu item Settings->User Settings. Click Set User Password under Settings->User Settings and a small screen will appear preloaded with your linux system username. (Windows users it will preload with your proper name... you'll want to change that to your prefered user name.) Input a password and click ok. This setting is on a per database basis. Meaning, if you have two database, and databaseA has no username/password set and security turned off then you can switch right into it. Or anyone for that matter that runs the program. If databaseB has a username and password set and user security turned on then a username and password is required to open that datanase. Even after the username and password are set you can turn it on and off under Setting->Program Settings and choosing the value 1 from the second drop down to enable security. The password is hashed when provided the first time and the hashed value is what is stored in the database. When in use the hashes are compared for authentication. The password is never in plain text.

#### LOCKED OUT OF YOUR JOURNAL DATABASE
In the event that you forget your database password or you turned on security before setting a username and password I've included an Unlock tool to help with this. The program Unlock is in the MJournal program directory. For Windows users the file name is Unlock.exe. It's a very simple utility that has one job. To unlock your database... There is a dropdown menu with database names in it. Choose the name of the database you're currently locked out of, the lock the Unlock button. That's it! You'll see a message on screen that the process is complete. What happens when you unlock your Journal database...

1. it turns off security for the database in the settings table.
2. it removes the username and password record in the user table.

To reset a username and password... first set a username and password. Next turn on program security and that's it.

#### UPDATE ENTRIES
There are lots of times I simply want to update an existing journal entry rather than creating a new one that is related directly to one that already exists. I do this a lot more in my development journal than my personal one, but then that allows me to track changes on projects more easily. It's really quite simple: select the entry you want to update from the tree menu, click it to load it into the right side of the screen, then click the button labeled **Update Entry** or press the **F5** key on your keboard. *( if you're using a laptop then it's likely you'll need to also first press the funtion key before pressing the F5 key. Someone at some point in time thought it was a good idea to assign the special functions to have priority on the F keys so they included a special function key to bypass those **special functions**. Horrible idea in my opinion. Indeed, they're so special most people either don't use them or forget they even exist.)* However, on a standard keyboard the F keys still function normally. 

Anyway, when you hit the Update Entry button a second window will appear with the original entry in it. You can...

1. change the title of the entry
2. scroll to the bottom of the entry and begin entering more text..
3. you insert a data/time value which will automagically be inserted below the current information being displayed and from there begin your additions to the entry.
4. then, when you're finished just click **Submit Entry** or hit the **F8** key which will do the same thing.


You can also enter the time/date information by clicking on the **edit** on the menu bar there is an item labeled Utilities and under that there is a selection labeled Insert Date/Time.  You can also insert the date/time by hitting the F4 key. There ya go! Bob's yer Uncle.

