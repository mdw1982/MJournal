			
GENERAL INFORMATION
----------------------
This program was written to take the place of a Journaling program I used some years back named RoboJournal. It was a database driven program that stored all journal entries in a backend MySQL database. At some point around 2019 the developer of that program stopped active development and support of the program. Subsequently it was no longer available for most Linux distros after 2019. That program was very clean and simple and easy to use. I've made every concious effort to keep this program like that one. Basic and easy to use. At the time of this writing the program is at the beta stage at version 0.3.5. It is mostly stable and usable. Data in and data out with nothing fancy. It's a journaling program after all. Written in Python. While it is possible to use the source code and connect this program to a MySQL database backend, I've designed this program to use SQlite3 and keep the database file local to the program directory. 

The program is primarily designed to be a single user program, but if nececssary it could be adjusted to allow for multiple users. Then again as previously stated it is a jouraling program, which I myself use, and I don't see much need for more than single user access.

GERNAL OPERATION
-----------------------
Once the program is completely setup you'll notice in the left pane of the main window a tree menu where entries are displayed. The very first entry is preloaded at setup so that the menu will function. Without that entry the program will not run. By default the tree menu is displayed in expanded mode. You can, of course calapse the nodes, but the menu expanded is set at run time. I have, on my development TODO list, an entry that will track the state of the tree menu, but for now it always loads expanded. Newest entries at the top, oldest at the bottom. To load an entry all you have to do is click on the node for that entry and it loads in the view on the right side of the main screen.

The tree menu displays entries in nodes. Parent node is Year, with children and grand-children nodes month and then day of the month the entry was made. The final node displayed contains the day of the month, title, time of day and the entry id. Those last two items are displayed to give the user a frame of reference. Especially the time of day. Because of the entry ID value you can have multple entries on the same day.

If you want to add additional information to an existing entry, simply select the entry, and enter any additional information, then click "Update Entry" to send your original and added content back to the database for storage. This over-writes what was previously in that database field so be aware when updating an entry. Be sure to append any new information to the entry starting after the original entry for continuity sake. If you remove anything from the entry during the update process it will be gone and cannot be recovered.

The refresh button refreshes the tree menu in the left pane. This button will likely be removed in later versions of the program since when a new entry is made the tree menu updates automatically. 

The "Remove Entry", located under File in the menu bar, does _not_ actually delete a journal entry but rather sets it to invisible. What I mean by that is this: each time a journal entry is made there is a database field named visiable that has a default value of 1. When the program loads the tree menu it pulls all record information where the field visisble == 1. When you _remove_ an entry what you're actually doing is setting that field value to 0 so that those entries are not selected to be displayed in the tree menu. Select and load the entry, then click the Remove Entry button and that entry will be hidden. Years ago while in college my professor teaching the database class emphatically instructed us that you NEVER delete a record because you might find one day that you need it. So, you just hide it by adding a field to the table that we can set to 1 (visible) or 0 (hidden). In that manner you preserve data for later in case you need it. At some point in a later versiion of the program I plan to include a screen that will display hidden entries and allow for them to be made visible again. At this point, however, the only method available is to do so manually by interfacing with the SQLite database on the command line and changing the value of visisble from 0 to 1. Not recommended.

If you actually want to remove an entry then it will take some work. As this program uses SQLite you'll need the command line tools to be able to connect to the database and then actually issue the SQL commands to remove records from your journal database. Unless you really know what you're doing I wouldn't recomment messing around with that.

ADDING NEW ENTRIES
-------------------------
Adding new entries to the MJournal program is very straight-forward. Click the "New Entry" button. That will open a second window over top of the main window. There you'll see you have three fields: Title, entry content and a text field for tags. Tags should be words seperated by a comma. You don't have to use tags, but the search feature is fully functional those tags will come in handy. The search function won't be visible to the user until it's completed.

# Mjournal
# Mjournal
