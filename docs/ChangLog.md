# CHANGE LOG
updated last: Thu 06 Jun 2024 10:44:28 AM EDT

03/17/2024 - (working) when writing to the user's crontab the a new line is created before the entry when writing to the crontab. If this is the first entry in the user's crontab the cron job doesn't happen.

03/17/2024 - (fixed) Database Maintenance: pertains to Linux systems. Setting the crontab entry. Set the default minutes value to 0 and the default hour value to 23. The real issue was there was the default value for minutes was * which if left to it's default value this would cause the scheduled backup job to run many times per hour during the 23rd hour resulting in many, many backups being made. I myself am guilty of overlooking this and have had to later edit my own crontab entry for this scheduled event.  

03/24/2024 - (fixed) searching entries, when they're presented on the screen the dates are from the oldest to newest. This might be a sorting issue, but the bigger issue is that while the entry presented is in the right month some appear in the wrong year. I discovered this while searching for something in the entries and found something I knew was in the wrong year.

4/24/2024 - (fixed - windows versions) program opening an accompaning terminal window when reloading/restarting the program whether due to database change, working in the database maintenance window, or clicking the reload button. The new method of restarting the program is much faster and smoother.

5/8/2024 - (added/fixed - windows version) there is not a button on the Database Maintenance window that starts the Windows Task Scheduler so users can setup MJournal database backups on a schedule.

(bug) 5/17/2024 4:52:35 PM (fixed)
applied to both

* there was a bug in the dbmoves.detach() function... destination path statement was incorrect. Fixed.
* sometimes it would work and sometimes it would fail. took a little while to track down.


(feature) 5/17/2024 4:55:43 PM (complete)
applies to both

* Switching database in program no longer requires a program restart. Switching happens dynamically during runtime.
* big savings in time when compared to changing database and waiting for the program to restart.



06/03/2024 {fixed} - On occassion I've noticed that the install goes smoothly, but the program fails to start after it's complete which it's supposed to do. If you run the main program MJournal in a terminal window, which is where all the debug print statements appear, you may see an error that looks something like this in the terminal window:
====================
Traceback (most recent call last):
  File "main.py", line 882, in <module>
  File "main.py", line 220, in load_tree_data
sqlite3.OperationalError: no such table: entries
[52576] Failed to execute script 'main' due to unhandled exception!

06/03/2024 07:58 (complete) Correcting Launcher Linux **–** At this time rather than having to invoke sudo to create launcher in [/usr/share/applications](file:///usr/share/applications) keeping the launcher local to user home directory.

* changes to the launcher work nicely. Placed the launcher on the desktop. Ubuntu requires the user to set "allow launching" on the launcher.


06/04/2024 Critical Error Checking in TreeMenu function: 

* if a database is damaged or missing then the tree menu can't build and that causes a crash
* added functionality to catch the exception, detach the damaged db and load another one to keep the program running to give the user time to deal with the problem by restoring it from backup. 
* in case there was only the one database then a rescue database is created, loaded into dblist and the program restarted.


06/04/2024 12:18 Configured and began adding logging to the program:

* started adding logging statements where I've been printing information to console and at each place where we're catching exceptions.


06/05/2024 – Program Logging enabled

* enabled logging in the program and removed all the print statements that were spitting out information to STDOUT that were used for debugging.


06/06/2024 – Changed dimensions of main screen - 

* noticed that on smaller displays lower parts of the main screen were inaccessible.
* changed started main screen height and width and made elements grow with the main screen.
* still a limitation to the width of the entry view element on main screen. I'll place that on my todo list.


