# MJournal README
#### DOWNLOADING THE PROGRAM PACKAGE
Ah... you've landed on my github page. As such the first thing you're seeing is a listing of all the source files within this project. If you look to the right of the source listing you'll see a section headed with Releases. Click there and you'll be able to download a release package for your platform. I do my best to make sure that the latest versions of the packages are available. Once you've downloaded the package and unzipped it please take a few minutes to read through this document to get a basic understanding of installation and operation. Further detailed information is contained in the HOWTO document also part of the program package. For those that are impatient and want to get started as soon as possible skip down to the Installation section of this document to learn how to install the program.

#### GENERAL INFORMATION
**This program is open source and shall remain so hereafter forever. It is presented 'as is'.**
This program was written to take the place (for me at least) of a Journaling program I used some years back named RoboJournal. It was a database driven program that stored all journal entries in a backend MySQL database. At some point around 2019 the developer of that program stopped active development and support of the program. Subsequently it was no longer available for most Linux distros after 2019. That program was very clean, simple and easy to use. I've made every concious effort to keep this program similar to that one. Basic and easy to use. At the time of this writing the program is nearing the end of it's beta stage at its current version of 0.9.8.x. It is stable and very usable. Data in and data out with nothing fancy. It's a journaling program after all. Written in Python. While it is possible to use the source code and connect this program to a MySQL database backend. I've designed this program to use SQlite3 and keep the database file local to the program. After much thought about this I don't really see the need to build that functionality into this program. *There is no need, on either Linux or Windows, to install supporting SQLite as all that is compiled into the program binaries. **IT IS CRITICALLY IMPORTANT THAT YOU SETUP AUTOMATIC BACKUPS AS SOON AS POSSIBLE*** if you intend to use this program long term. You can't restore what you don't have in case something happens and your daily driver journal database gets damaged. Losing a database is rare and since I started delelopment of this program it's happened only once. Its better to plan for the worse and hope for the best. **see the howto file for setting up automatic backups. The Linux version of the program the backup is rock-solid using a crontab entry for scheduling.

The program is primarily designed to be a single user program. That is how I use it, however as this is an open source program if you're confident in your coding skills you can change it to operate however you wish. However, be aware that if you make changes that break things then it is on you to fix said problem. I personally have no desire to make this a multi-user program. It's a journaling program and as such assumes the user wishes to keep their thoughts (entries) private or mostly private. Basic security is possible by setting a user password requiring the user to enter a username and password at the start of the program, however this **does not** encrypt, in any way, the database filles or the information inside them.

The compiled binary that is included in this repository runs nicely in Linux or Windows and should start right up if you download the zipped release file from Github. I'm working on polishing a self-contained .exe for MS Windows, but it's taking a little longer than expected. Currently have a test install on a windows system that, for all intents and purposes, appears to be working normally. Albeit, with some limitations in regards to automated backups. The MJournal program was developed using Python 3.10/3.11 and now 3.12. When compiling I'm compiling the program into a single file, so the only dependent files are the following:

* cdb
* creds
* dblist.json
* defaults.json
* firstrun
* *.json
* *.db

The source files are also included in a separate directory, however if you are planning to or decide you want to work with the source files it is strongly recommended you use a proper development environment such as PyCharm or other IDE because there is a lot going on you'll need that environment for. This also means you'll need to download the complete source package from GitHub. At this time I'm not taking on Contributors until at least the program version reaches 1.0.

The files mentioned above should be in the root of the program directory along with the MJournal binary file. There is a setup script I'm working on the create a desktop shortcut, but till that's done you may have to make a shortcut the old fashioned way: manually. No portion of the program or setup script (later) will create a menu item in the Launcher menu (in Linux), or the start menu in windows. You just download the package from Github and run the program. Eezy Peezy!
##### Cross-Platform Compatabiilty - a gentle warning
I've taken great pains to construct the code base such that I don't have to run two branches of the code. That means that the code itself checks to see if it's running on Windows or Linux. For some processes this happens at the time the binaries are compiled. Other times this occurs at runtime. All that being said, if you alter the source code included with the package and recompile it, it's strongly recommended you DO NOT make changes to the parts that check to see which platform you're running the code on. Working with the code assumes the one doing so really knows what they're doing. I did it this way because I didn't want to have to run and care for two different branches of code. This isn't my day job, but a hobby that brings me happiness. At some point in time I'm just going to stop providing the source code with the installation package and leave it up to the individual to get the code on their own because compiling the binaries requires a certain environment to make it all work properly. So, if you see no folder named src after installation and you want the source code you'll have to downloaded it from my GitHub repository. <https://github.com/mdw1982/MJournal>

#### DOCUMENTATION
I do my best to keep this as up to date as possible. When you download a release the documentation is pretty much up to date, but you can always get **the** most up-to-date HOWTO file from the github repository.

#### REQUIREMENTS
You absolutely must have Python 3.11 or above installed on your system if you intend to work with the source code.  Getting the binary version of this program setup should be a breeze since it's not required to run the binaries on either Linux or Windows. The compiled binaries have everything they need to be able to run. Essentially, the setup program checks to make sure all the dependency files are present and have their default values in them. Then, it creates the default database. Check the import statements for the modules used so you can install any missing modules.

If you're running Windows, you can get Python from <https://www.python.org/downloads/windows/> You will want Python 3 Release. For Windows users make sure if you install Python from python.org that when you're installing it you click the check boxes to place python in your path. THAT IS IMPORTANT. For Linux users python will already be in your path. (Pyhon being in the users PATH is why its best to store the program directory in your home directory. Windows users in C:\Users\%UserName%). When you download the package from Github you're getting all the souce code, but you're not getting a self-contained compiled binary program that has everything it needs compiled into. If you download the code then it will need to be compiled. So, it's better to first get the release for your platform and install it. Later, if you wish to get the code and work with it, then by all means download it and have at it. Make certain to pay attention to the import statements at the beginning of these files if you intend to work with the source code so you can be sure you have the requisite modules installed.

**The compiled version of the program, whether windows or Linux, does not require Python to be installed on the system**. When I compile the program it's compiled as a single file and contains everything it needs to run in one file. There are still dependency files that are program specific, but they are files that the program uses for data storage and the like that are specific to the program's operation. If all you're looking for is the compiled version to run it on your system, then check the Releases for your platform. There are two program release package: One for Linux and one for Windows.

#### INSTALLATION
YOU DON'T NEED ELEVATED PRIVILEGES TO RUN SETUP (YET), in fact I recommend against it - the program is designed to run and setup in user space. I'm still thinking about creating a main menu item for the program on both platforms. I rather like the freedom that's offered so far by not going that route. A desktop shortcut appears to be working just fine for now.

The program directory, is set to the root of the user's home directory.

* Linux: [/home/<username>/MJournal_Linux](file:///home/%3Cusername%3E/MJournal_Linux)
* Windows: C:\Users\<username>\MJournal_Win64

Once the setup is complete, if you really wanted to, you could move the program directory anywhere you wished to as long as you have the necessary system permissions to do so. Just don't forget to update the program's shortcut for launching the program. Thats on the user.

##### Important
**related to versions before to v1.0**
Versions prior to 0.9.7.6 the installation was a little confusing with little output to the screen as to what was going on. Until, at the very end you'd see a quick popup announcing the installation finished. If something failed there wasn't anyway to know. Versions after 0.9.7.6 come with a compiled setup executable which gives the user feedback on what's going on with the install. If there are any errors they'll be shown on the screen. The setup UI isn't fancy, but it is functional. At the time of this writing I'm still working some bugs out of the windows version. (*Something I've found in testing this program which started in 2022 is on the Windows platform things run a bit slower than they do on the Linux platform. That is because Windows defender is slowing things down. It's doing its job as it were. You __may__ have to add a folder exclusion in Windows Defender to run this program because I have not yet started digitally signing the program. So, Windows defender will identify the program as a virus or trojan. Its a false positive and primarily because the binaries are unsigned and Publisher Unknown. I assure you they are safe. Windows Defender in Windows 11 is even more aggressive about it all.*) I haven't yet decided if I'm going to go the route of getting signing certificates and begin jumping through the MS driven Software Delopment hoops. I am aware, the deeper I go with development of this project that signing your work is necessary on both Windows and Linux, but that's going to wait till the first release candidate or RC1 or just version 1.0 of the program.
#### =
#### Current Versions
You can start the setup on either platform - Windows or Linux - by double-clicking the setup file. In this version a basic GUI now runs that provides for user interaction and gives visual feedback during the process.

* Linux - setup
* Windows - setup.exe

As before, once setup is complete the setup process ends and the MJournal program starts automatically ready to go.

##### Installation Summary
NOTE: these steps can be performed in the described manner on both Linux **AND** windows.

1. download the package and unzip it, then move the program folder to the root of your home directory. In Windows that would be inside your User Profile directory (C:\Users\<yourusername>)
2. open your file manager... On Windows that would Windows Explorer... On Linux, well that depends on the DM you're using. At this point the extracted folder will bear a name MJournal_<platform>_vx.x.x.x (where is the 'x' appears is the current version number. You should rename the folder to just 'MJournal', but that's really up to you. I recommend it.
3. locate and double click the setup or setup.exe file you find there. That will get thiings started. At the end the setup program will complete and the MJournal program will start.

##### Program Shortcut
To be blunt there is none created... I'm working on it, but its low priority at this point because I'm concentrating on the important bits. Like everyone else I have a lot going on so this project is something I do because I like coding and not because I have to, so development takes a bit more time than one might think. That being said you'll have to create the program launcher manually. Icons for the program are located in the *images* folder inside the program directory. MS Windows:  There are two .ico images. One 80x80 for the shortcut and one 36x36 the program uses for the application windows. The same holds true for the linux version, however Linux uses the .png image format for this application.
##### Mascot Image
...*has been removed. It was just a place-holder anyway. Now, the tree menu extends to the bottom of the main window.*

#### PROGRAM UPDATES
In most instances, unless otherwise stated, program updates will apply to the MJournal program binary. All other changes will be included in the latest release of the program. If you decide to download the program for your platform then follow the repo and you'll get notified when new packages are released. On my todo list would be program patches where just the compiled binaries are uploaded to the repository that would include just the binaries. Those would just need to be copied to the MJournal program directory. For now at least. Maybe at some point I'll get fancy and include an installer for patch releases.

Upgrading program binaries is as simple as downloading them and placing them in the program directory over-writting the existing program binary. The easiest way, for now, is to just download the latest version of the program. At the current time there is no automated method for updating the program other than doing it manually. That said, there are plans once the program reaches 1.0 to create a method for checking for updates.

### GRAPHICAL USER INTERFACE or GUI

#### FEATURES

* **Tree Menu:** easy access to journal entries on the main screen
* **View**: single click on entry node from tree menu loads the Journal entry to be read.
* **Tags**: add tags to each or any entry to be searched on - tags added for each entry at the time an entry is being made.
* **Main screen Function buttons**: intuitive function buttons to aid journal entries. These are explained in more detail in the HOWTO document.
* **Entry Search**: Search on Body, Title, Tags or all three.
* **Multiple Journal Databases**: create and use as many or as few as you wish.
* **Local Journal Database**: no need for connections to remote database servers. Journal Databases are SQLite database and local to the program. They live in the same directory as the program
* **Switching Databases**: easily switch from one database to another in mere seconds.
* **Journal Entry Security:** prevent people who have access to your computer from reading your journal by setting a username and password on a per database basis. Once set and enabled, the program will not open the database without the proper authentication. **Please see the HOWTO file to understand exactly how to use the database security. If done in the wrong order you'll find yourself locked out of your journal database.** There is an unlock tool included in just in case name Unlock (linux) or Unlock.exe (windows).
* **Enable/Disable Journal Security:** The user has the ability to turn on and off password protection for a specific database.
* **Changing Password:** The program provides the user the ability to not only set a password for a specific database, but then to also change that password.
* **Easily Create New Databases**: Create new Journaling database without needing to know how. Just give it a name and off you go.
* **Insert Time and Date**: insert time and date into journal entries. Comes in real handy when making updates to existing entries.
* **Database Backups**: Easy manual and scheduled backups can be performed without knowing the technical details of how it's done. Both manual and scheduled backups. Windows version has a button to open Windows Task Scheduler where you can define a scheduled backup.
* **Detach and Reattach Database files**: Rather than delete databases, the program has the ability to remove active database files from the program so they don't show up on the available database list. The can later be added back onto the list for access.
* **Program Theming:** the program has the ability to change its look and feel in regards to color scheme.
* **Open Source:** as open source software you have the ability to make what ever changes you deem necessary to suite your needs.
* **Remove Entries**: Rather than actually remove a journal entry you can hide or unhide the entry. There is a field in the entry database called visibible. Its default setting is 1 which means its visisble and will be accessible from the tree menu. When you hide the entry that value is set to 0, which means as long as that value is left at 0 it will not be displayed on the tree menu.
* **Key Bindings or Hot Keys**: Essentially, I've bound some of the Function keys on the keyboard to specific events in the program. Check in the HOWTO file for more information about the hot-keys. I personally find this extremely useful since the less time I have to spend touch my mouse the better I like it. You can open the HOWTO page from the menu bar on the main screen under Help.
* **Restore from Backup**: it possible to restore a database from a backup while inside the program, and its a relatively painless process. What is required is a backup file to restore from. ***Make certain to setup the backups when you install the program***. At this time, on the windows platform this has to be done directly using Task Manager. All you have to do is call the binary dbbackup.exe, set the time of day and days for the backup to happen. Make sure you set the backup ***time*** for when the computer will be on.
* **Unlock Tool** - for use in case you set a user password for a database then forget the password, or you set user security **before** setting up a password.


#### Issues -  Changelog

* 03/17/2024 - (working) when writing to the user's crontab the a new line is created before the entry when writing to the crontab. If this is the first entry in the user's crontab the cron job doesn't happen.
* 03/17/2024 - (fixed) Database Maintenance: pertains to Linux systems. Setting the crontab entry. Set the default minutes value to 0 and the default hour value to 23. The real issue was there was the default value for minutes was * which if left to it's default value this would cause the scheduled backup job to run many times per hour during the 23rd hour resulting in many, many backups being made. I myself am guilty of overlooking this and have had to later edit my own crontab entry for this scheduled event.  
* 03/24/2024 - (fixed) searching entries, when they're presented on the screen the dates are from the oldest to newest. This might be a sorting issue, but the bigger issue is that while the entry presented is in the right month some appear in the wrong year. I discovered this while searching for something in the entries and found something I knew was in the wrong year.
* 4/24/2024 - (fixed - windows versions) program opening an accompaning terminal window when reloading/restarting the program whether due to database change, working in the database maintenance window, or clicking the reload button. The new method of restarting the program is much faster and smoother.
* 5/8/2024 - (added/fixed - windows version) there is not a button on the Database Maintenance window that starts the Windows Task Scheduler so users can setup MJournal database backups on a schedule.


