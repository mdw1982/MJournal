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
INSERT INTO "entries" VALUES(1,'WELCOME',10,9,2022,'','=====================================
README	MJOURNAL PROGRAM - 10/2/2022
=====================================
AUTHOR: 
Mark Weaver
mdw1982@gmail.com

LICENSE:
GnuPL - for more information about copyright
please view the licens file in the program
directory or view it from the main program
help menu.

VERSION:	0.4.7
			
GENERAL INFORMATION
----------------------
This program was written to take the place of a Journaling program I used some years back named RoboJournal. It was a database driven program that stored all journal entries in a backend MySQL database. At some point around 2019 the developer of that program stopped active development and support of the program. Subsequently it was no longer available for most Linux distros after 2019. That program was very clean and simple and easy to use. I''ve made every concious effort to keep this program like that one. Basic and easy to use. At the time of this writing the program is at the beta stage at version 0.3.5. It is mostly stable and usable. Data in and data out with nothing fancy. It''s a journaling program after all. Written in Python. While it is possible to use the source code and connect this program to a MySQL database backend, I''ve designed this program to use SQlite3 and keep the database file local to the program directory. 

The program is primarily designed to be a single user program, but if nececssary it could be adjusted to allow for multiple users. Then again as previously stated it is a jouraling program, which I myself use, and I don''t see much need for more than single user access.

GERNAL OPERATION
-----------------------
Once the program is completely setup you''ll noticed in the left pane of the main window a tree menu where entries are displayed. The tree system is primarily designed for folder listing and as such click events on elements in the tree data is no easy task. Thus, you will see a button in the function buttons labeled "Load". Much effort went into trying to get events sent back to display the record content when it is selected from the tree menu, but ultimately I found it was far easier and efficient to use a button to send the chose entry information back to the main program. Select the entry to be viewed and click the Load button. That entry is then displayed in the right pain of the main window.

The tree menu displays entries in nodes. Parent node is Year, with children and grand-children nodes month and then day of the month the entry was made. The final node displayed contains the day of the month, title, time of day and the entry id. Those last two items are displayed to give the user a frame of reference. Especially the time of day. Because of the entry ID value you can have multple entries on the same day.

If you want to add additional information to an existing entry, simply select the entry, click "Load" and enter any additional information, then click "Update Entry" to send your original and added content back to the database for storage. This over-writes what was previously in that db field so be aware when updating an entry. Be sure to append any new information to the entry starting after the original entry for continuity sake. If you remove anything from the entry during the update process it will be gone and cannot be recovered.

The refresh button refreshes the tree menu in the left pane. This comes in handy when you make a new entry. At this time I haven''t found a way to send a command back to the main part of the program to reload the tree menu, so the refresh button is filling that roll. I''ve using it during developmnt to make sure new entries are getting placed into the database.

The "Remove Entry" does _not_ actually delete a journal entry but rather sets it to invisible. What I mean by that is this: each time a journal entry is made there is a database field named visiable that has a default value of 1. When the program loads the tree menu it pulls all record information where the field visisble == 1. When you _remove_ an entry what you''re actually doing is setting that field value to 0 so that those entries are not selected to be displayed in the tree menu. Select and load the entry, then click the Remove Entry button and that entry will be hidden. Years ago while in college my professor teaching the database class emphatically instructed us that you NEVER delete a record because you might find one day that you need it. So, you just hide it by adding a field to the table that we can set to 1 (visible) or 0 (hidden). In that manner you preserve data for later in case you need it.

If you actually want to remove an entry then it will take some work. As this program uses SQLite you''ll need the command line tools to be able to connect to the database and then actually issue the SQL commands to remove records from your journal database. Unless you really know what you''re doing I wouldn''t recomment messing around with that.

ADDING NEW ENTRIES
-------------------------
Adding new entries to the MJournal program is very straight-forward. Click the "New Entry" button. That will open a second window over top of the main window. There you''ll see you have three fields: Title, entry content and a text field for tags. Tags should be words seperated by a comma. You don''t have to use tags, but the search feature is fully functional those tags will come in handy. The search function won''t be visible to the user until it''s completed.

','11:08',1);
INSERT INTO "entries" VALUES(2,'test entry',10,10,2022,'','&dbqupsome things should just be easy&dbqup','10:34',1);
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
