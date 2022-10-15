BEGIN TRANSACTION;
CREATE TABLE entries (
                id integer PRIMARY KEY,
                title varchar(500),
                month integer,
                day integer,
                year integer,
                tags varchar(300),
                body blob,
                time varchar(5),
                visible int DEFAULT 1           
                );
INSERT INTO "entries" VALUES(1,'WELCOME',10,7,2022,'','Welcome to Mjournal. I hope you find it useful','09:56',1);
INSERT INTO "entries" VALUES(2,'Mjournal program',10,7,2022,'','Boy oh Boy! does this critter have a long way to go. But then I''ve only been coding in Python for about 2 months, so not too shabby. As I progress through the program I''m of course finding things that need fixed or changed. At the very least I''ve got data going in and being able to be displayed. The hardest part so far has been the tree menu that shows entries that exist in the database. Since RoboJournal is no longer being developed - since 2019 - I decided I''d write something that looked and behaved similarly. I''ve looked far and wide and haven''t been able to find anything even remotely like it. The journal or diary programs I''ve looked at for Linux are real stinkers. Meaning they actually stink and are either a pain the ass to use or just plain terrible.

I got spoiled with the way RoboJournal operated since it used a backend datanase to store all Journal entries. However, rather than use a MySQL database I''m using an SQLite database for this. Its mostly self contained within the program and is quite well supported by Python. I could use MySQL and sometimes while developing this program I do think about it. But would naturally require securing the db username and password information. Not diffucult but can be a pain in the ass. I''m mostly undecided right now because having the database for the entries self-contained in the program''s data directory is very convenient. For my use that''s fine... I do daily backups. Then again... using MySQL on the localhost or another host opens up a lot of other issues. I''m not going to bother thinking about that for now because there a tons more things to get sorted before I really consider that.

Hell! I''ve only got very basic functionality right now. Data in and data out. That''s about it for now. I''m a long way off from all that other stuff. I''m using the PySimpleGUI module for all the GUI stuff as well as using a tree menu system to display entries in a similar fasion to the way RoboJournal did. It''s definitely not designed for that, but I was able to get it working. It''s going to take time to flesh things out. 

Spent hours today just getting the damned thing to settle down and stop crashing when submitting entries. I''ll consider myself lucky if I''m able to get this entry submitted without a crash and loss of the entry. I''m pretty certain I''ve got that sorted out. Apparently there was an issue in the manner I was trying to send the data to the database. There are some quirks with SQLite that don''t exist with MySQL. I''m so used to that backend that it makes it weird.

I can only read previously posted entries and make new ones. I can''t yet edit current entries or remove them. Though I''m not sure how important it is to be able to easily remove them from within the program. I can of course connect directly to the database and remove entries. That too is a pain in the ass. 

I almost gave up on the tree menu earlier today. I was having a horrible time getting it go do what I needed. Eventually, things started falling into place. now as long as I can submit this entry without it crashing on me that would be awesome!','13:04',1);
INSERT INTO "entries" VALUES(3,'Trying the compiled version',10,7,2022,'','there is a bug somewhere in the update sequence of the program. In both the compiled version and source version of the program. are you going to cooperate?

Lets see if we can get this updated now. 

It would appear that we have got things sorted out... still cannot copy and paste into the multiline window element. in fact that process is a whole other set of hoops to jump through. Unable to use contractions as well in the entry update. this is not making a lot of sense at the moment. I am pretty sure it is a limitation of sqlite and not an actual issue in the manner in which I am coding the record update. 

I''ve enclosed the body varliable in the update statement in double-quotes to see if I''m able to use single quote characters in the text I''m sending back in the update.

And apparently that was that was needed. For pete''s sake. I''m not going to back and undo all the previous changes at this point. I''m just goiung to leave things as they are for as long as its working.','13:05',1);
INSERT INTO "entries" VALUES(4,'Running the Compiled version',10,7,2022,'','Essentially a snapshot of the code compiled as an elf binary. Frozen at the time it was compiled, so I can use it while I&sngquom still working on the source code. Its been sitting her running on the desktop for about an hour and so far no major issues with freezing, becoming unresponsive or any detectable memory leakage. I&sngquove got Ksysguard running at the same time and I&sngquom tracking the mem usage once an hour. mem usage has ticked up ever so slight since opening the entry window. It&sngquoll be interesting to see if it goes back down when this entry is processed and the window closes.

1154
still no detectable leaks in memory and usage appears to be so far quite stable. at least as far as running on Linux goes. its been steady and stable the last two hours.

1409
good and stable so far today. I just made a change and recompiled main. added a field to the database. it took a while to find a tool to use to edit the database, but I found one that light and efficient. anyway, I added a field called visible and set the default value to 1. that way when the user deletes a record its actually hidden rather than being deleted.

1650
Added the necessary code to create users for the program with hashed password and connected to the menu bar under Settings->Set User Password. Guess the next thing to do is get things setup so that when the program starts it asks for credentials.

2039
coded the necessary pieces that are required to prompt the user to authenticate to open the program. Now I&sngquove got to code a solution to be able to turn it on and off.

10.10.22  -0709-
I&sngquove made a copy of the Mjournal folder under my python folder where I keep non-project python file and programs. I&sngquom using that one as the production version of the program. If any changes are made to the code base that are stable I have to sync those file up. So far I&sngquove not done so. Yesterday was quite the day. Ran down a few actual bugs in the program and got stuck on an issue for an hour or so till I figured it out. I also tried placing the source in a subdirectory of the Mjournal folder but it didn&sngquot like it very much. Most likely because of the way I was doing it. It complained loud and long about not being able to see other file. So, I put everything back in the root folder. Once compiled into a single binary it doesn&sngquot care. Only that the files cdb and dblist and database files are in the same directory as the binary. It&sngquos happy then.

10.13.22  -1601-
testing the update to entries displayed in search results...','13:05',1);
INSERT INTO "entries" VALUES(5,'compiling for Windows',10,7,2022,'','I made an attempt at getting things setup to compile the program on the windows platform, but I wasn''t able to get it done. this machine just doesn''t have the necessary power to run windows well enough to make it happen. Once I got Pycham install and running on the windows VM it was just unusable. So, I have no idea yet what will happen or even if I''ll be able to get that to happen.

At the very least now I have to code a solution to be able to turn off the user authentication to open the program. that''s working nicely, but for me at least I really don''t need it.

I''m also considering creating a third db table for program settings. one of those settings would be whether or not we''re running with user authentication. I thought about writing to and reading a file that would send back a true or false conditon, but it makes more sense to use a database for that. I''ve got just about everything I need personally for the program to be useful to me, but there are more things that should be done in case anyone else would like to use it. I really need to see if can get it to compile and run on Windows. It doesn''t like windows 11 at all. It ran briefly but the shut down. seems there''s a lot of problems getting the needed libraries installed that the program needs.

10/4/22 1447
I never did get to try and compile it on windows last night. Just don''t have the horse power on this old machine to get it done on the windows VM I have.

10/6/22  0759
I tried this again yesterday afternoon. Windows doesn''t make it easy. Python doesn''t get installed in the normal place, but rather gets placed inside the users'' home folder down inside appdata. this makes getting the right folders in the users'' path a real pain in the ass. When I finally got the PATH setting correct then it would get amost to the end of the compile and fail. Not sure why it''s failing yet because I don''t understand information in the traceback.','13:06',1);
INSERT INTO "entries" VALUES(6,'possible bug',10,7,2022,'','tree menu isn''t updating after a new entry is made. - fixed

10/6/22  0740
I found out why the tree isn''t being updated when a new entry is made. the tree update wasn''t being called when sending the new entry for processing. that''s fixed now.','13:06',1);
INSERT INTO "entries" VALUES(7,'reloading tree new entry',10,7,2022,'','this is something that I want to happen automatically. When a new entry is made I want the tree menu to reload rather than having to use the refresh button. That button should be able to be removed...DONE','13:07',1);
INSERT INTO "entries" VALUES(8,'MJournal TODO list',10,7,2022,'','PROGRAM FIRST RUN - Moved out to it''s own entry...DONE


SEARCH FUNCTION - the items for this are already on the main screen. I''ll need to create the screen that returns the results from the search. the biggest problem at the moment is how to load a Tree menu with the results. I don''t know if I can reuse the TreeData object already established or not.


PROGRAM LOGGING	- at present there is no logging for the program going on. That will need to be setup and implmented. There are a lot of places where try/except should go, but those only exist presently in places where I''m catching an exception to keep the program from crashing. (another column in the settings table - log_level)
- 1549 -
I''ve started setting up the program logging. It''s going to be a long boring process getting this all in place. At this point I don''t think I''m going to bother setting up for a log level.
- 1613 -
Logging has been setup and has begun.
10.10.22  -0708- 
There is still a lot of the program and it''s functions that need to have logging setup in. Doing that as I go through the program tracking down problems.


ADDITIONAL DATABASES - broken out into it''s own entry...DONE


TAGS - I''m thinking that the TAGS field on the entry screen should be blank such that there is no default value being tossed into the database if you don''t remember what''s in there. Instead, increase the screen size a bit and put a text field in there or use a frame around the field with some text with a small explanation...DONE','13:08',1);
INSERT INTO "entries" VALUES(9,'Additional Database',10,8,2022,'','I just had a thought that if a person wanted to keep certain kinds of information separate like a developer who wanted project information separate from personal information entries it would be handy to be able to create new databases and then switch between them. (another column in the settings table - current_db)
- 2316 -
I''ve got the first part of this completed. I''ve created the window necessary to allow for input and the functions to create the database and preload the tables. I''m thinking though that it would be better to store the current database in use in a file that is read at the beginning of the progam. that would also mean I''d have to keep another file that would store the database names.
10.7.22 -1107-
code is in place to create more databases and even switch to a different database, but I can''t yet do it on the fly. so far for the program to use the newly chosen database the user must exist the program and restart it. The screen does reload as expected but not with the chosen database.
- 1410 -
This is going to have to wait for a while. I''m just chasing my tail droping bits and peices here and there trying to get the db change to show up without a restart. There''s something playing at the back of my brain about it.
10.8.22  -1024-
I just had a though as I thinking about presenting search results. Essentially, if and when I connect the search function and present records that were searched for I''ll need a way to get back to the main window. I''ve got a function called make_window() that is used when the theme is changed. I''m wondering if I can use that to close and recall the main window.
-1045-
Didn''t work... created a second window and did change the database but the way I implemented it the tree menu didn''t work correctly meaning clicking on the entry didn''t cause it to load in the reading pane. But, do I have the binding in the make_window() function? The binding is there. I just have to work at this some more. I''ll get it figured out eventually.
-1302- 
this is turning out to be quite a challenge. I can change the db name easy enough, but closing and respawning the window to use that database is harder than I thought and I''m pretty sure its due to the way I coded the program as it is right now. At the moment I''m not sure where and what to change.
-1310-
I am so close I can taste iit. I really don''t want to go to a program database for settings. But because of the way I''ve designed this program I don''t know that I have a choice. If I was better at using json files that might be the way to go.
-1317-
placed the global ver database at the top of the main.py file and set it = to get_database(). there''s a print statement right after it so I can see that the database change is happening and python is reading from the top down each time but when the new window appears its not displaying the treemenu for that database.

10.9.22  -0834-
with this information in my while loop:
        if event == ''DBCHANGE'' or event == ''Change Database'':
            #print(values[''DBNAME''])
            change_database(values[''DBNAME''])
            window.close()
            main()
I''m seeing the gvar database value being changed and then calling main() after closing the window, but the global var change doesn''t have any affect in the program even though main.py is the only place it''s defined. Any time the database value is changed the file holding the value for the current database is read in from that file by get_database(). At that point the current value of database is set. Since get_database is called at the very top of the main program file I don''t need to call it anywhere else in the program. For the purposes of changing the database for the program I need to call change_database() and send the new db name along. That is then opening cdb and writing the value of the db to be changed to in there. Which is then read again at the top of the program as main() is called.

I can call main() or make_window() which is the same window layout as the one in main(), however for some as yet unknown reason the change to the gvar database isn''t being applied. The respawned window is using the old value of database with which it loads the tree menu. The current database value is also in the title bar and that doesn''t change either. It still requires a complete close and reopen of the program. If I use the exit command then the program stops completely and will not reopen.

-0857-
I finally found the answer...  replacing the lines window.close() and the call to main() with this line:
os.execl(sys.executable, sys.executable, *sys.argv)
completely close the current application and reopens it fresh AND using the chosen database.','10:52',1);
INSERT INTO "entries" VALUES(10,'Found a bug',10,8,2022,'','Updating an entry AFTER changing the theme and causing the window to reload will result in a crash because there is no way to handle the update from that window. But that doesn&sngquot quite make sense because make_window returns the window object and events from that returned window still go to the original window while loop. Well?

ADDRESSED
Not a bug... not sure what happened. It must have been something else I was doing at the time.','10:58',1);
INSERT INTO "entries" VALUES(11,'Program First Run',10,9,2022,'firstrun, intial, setup, program setup','PROGRAM FIRST RUN - Set up a check for incoming arguments such that if the argument is init_setup the program will create the journal.db file and write said file to the file dlist and cdb then start the program with that database just created. Or, we could check a file for a specific value. file (firstrun) has a 0 in it. If firstrun contains 0 run dbsetup.init_setup.

First Run Cleanup of dlist file - when init_setup runs it is placing extra line breaks (\n) in the dlist file. thankfully if there''s already something in there it doesn''t over right the file because it IS reading the file first, but still those extra line breaks are sloppy and appear in the database list when subsequently read.

-1113-
- setup file named firstrun and inside that file is the string True. in the if statement at the bottom of main.py just after launching the splashscreen there''s a check to see if this file has either True or False contained in it.
def is_first_run():
    with open(''firstrun'', ''r'') as f:
        val = f.read()
    print(val)
    if val == ''True'':
        with open(''firstrun'', ''w'') as f:
            f.writelines(''False'')
        return True
    else:
        return False

If True then the init_setup runs and creates the default journal.db database, closed the program and reopens with new database. If false then the program reads the cdb file to know which database is active.

In order for this setup to work I had to create a dummy database and place that db''s name in the cdb file. The program will not run if there is nothing in there and it has to be the name of an existing database. I believe the program needs the settings in that dummy database to be able to function... again, a design flaw if you wish to call it that. At the moment I''m not exactly sure where that is located within the program. I reckon I could setup some initial settings because the program was looking for the theme setting. with no database to pull that setting from it would crash when get_theme() is called at the top of the main program.

To Setup the propgram for first run:
- dlist is empty
- cdb has the name of the dummy database
- firstrun file contains True in it.

When these conditions exist then the program will initialize the default setup as outline in the init_setup() function. At this point I''m going to move my live verison of the program out of the project directory so that I can continue to use it and concentrate on further development of the project without disturbing the production version.','11:10',1);
INSERT INTO "entries" VALUES(12,'bug - touching nodes other than record',10,9,2022,'','ADDRESSED and FIXED
I accidently found that if you touch any node other than the actual record node in the tree menu.. such as month or year then the program crashes. the use should be able to collapse or expand the nodes on the tree without the program crashing. I''m going to have to dig at this a bit.

found the problem... it was stemming from the window.bind statemnt. When touching the parent nodes of the entry record it was sending a value to the while loop for the event '' SelectTreeItem'' that the program couldn''t deal with. Dealt with this by testing for those parent node values _A_ and _A1_ like this:
 if '' SelectTreeItem'' in event:
            if values[''_TREE_''][0] == ''_A1_'' or values[''_TREE_''][0] == ''_A_'':
                continue

Now the nodes, which appear on the screen can be collapsed and/or expanded without crashing the program. That was a happy accident.','12:43',1);
INSERT INTO "entries" VALUES(13,'bug - creating new database',10,9,2022,'','ADDRESSED
yet another bug... at least in the compiled version of the program. If I attempt to create a new database the program crashes as soon as I click the button the create the database. In the non-compiled program the database gets created but the dblist file looks like shit with a boat load of line breaks. thus the database list in the main program window looks like shit.

-1424- 
it was crashing in the non-compiled as well, but no matter how hard I looked I couldn''t find what was causing it. So, after it finishes in create_new_db() it comes back to:
        if event == ''Make New Database'':
            dbsetup.new_db_window()
            os.execl(sys.executable, sys.executable, *sys.argv)

I placed the command to execute a full stop and restart. Damned program was closing with an exit(0) and I couldn''t find any reason for it IF in that check I placed: 

if event == ''Make New Database'':
            dbsetup.new_db_window()
            window.close()
            make_window()

At that point when it came back from creating the new database the program would close. So, unless and until it shows up again I''ll leave it at that and considered it fixed.

-1434-
I think I figured out why it was exiting... instead of having this:
        if event == ''Make New Database'':
            dbsetup.new_db_window()
            window.close()
            window = make_window()
I had this:
        if event == ''Make New Database'':
            dbsetup.new_db_window()
            window.close()
            make_window()

YUP! that fixed the problem AND reloaded the database list as its supposed to. I been at this for a wee bit too long today perhaps. All better now. Correctly.','13:41',1);
INSERT INTO "entries" VALUES(14,'Trying to Compile on Windows',10,9,2022,'windiows, windows 10, beta','I''ve got, what I believe is a pretty fair beta version of the program. I''m loading it onto my Windows 10 VM and I''m going to see if I can get it to compile and run.

10.10..22  -0653-
That attempt at compiling in Windows, even though the path was in good shape, went just as badly as the other attempt. I guess more research into compiling for windows is needed. I spites me now that I didn''t even try to run the program. I was just so burnt from coding all day, hunting down bugs and windows taking so damn long to setup and load that I''d had enough and shut everything down.','16:48',1);
INSERT INTO "entries" VALUES(15,'bare word error back',10,10,2022,'','update_entryyou didn&sngquot tell me much that I could use. Why I&sngquoll never know.yyou didn&sngquot tell me much that I could use. 

what happens when I &dbqupput things in double&dbqup quotes

and now how &sngquoabout&sngquo single quotes?

Still getting the occassional crash when submitting an update. It&sngquos still not clear since there&sngquos nothing in the logs or from a popup.','10:40',1);
INSERT INTO "entries" VALUES(16,'dffasdf',10,10,2022,'','sdfasasd','20:40',0);
INSERT INTO "entries" VALUES(17,'is you is',10,11,2022,'','you&sngquore being a pain in the ass!','08:18',0);
INSERT INTO "entries" VALUES(18,'is you is',10,11,2022,'','Quick Entry Body','08:36',0);
INSERT INTO "entries" VALUES(19,'is you is',10,11,2022,'','Quick Entry Body','08:46',0);
INSERT INTO "entries" VALUES(20,'testing quick entry bug',10,11,2022,'','Quick Entry Body','13:06',0);
INSERT INTO "entries" VALUES(21,'testing quick entry bug -2',10,11,2022,'','Quick Entry Body','13:07',0);
CREATE TABLE settings(
    	                sid	INTEGER NOT NULL,
    	                theme	TEXT DEFAULT 'none',
    	                pwsec	INTEGER DEFAULT 0,
    	                PRIMARY KEY("sid" AUTOINCREMENT)
                    );
INSERT INTO "settings" VALUES(1,'DarkBlue1',0);
DELETE FROM "sqlite_sequence";
INSERT INTO "sqlite_sequence" VALUES('settings',1);
CREATE TABLE users (
                    uid INTEGER NOT NULL,
                    user text,
                    password text,
                    PRIMARY KEY("uid" AUTOINCREMENT));
COMMIT;
