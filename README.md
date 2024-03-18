# MJournal README
#### DOWNLOADING THE PROGRAM PACKAGE
Ah... you've landed on my github page. As such the first thing you're seeing is a listing of all the source files within this project. If you look to the left of the source listing you'll see a section headed with Releases. Click there and you'll be able to download a release package for your platform. I do my best to make sure that the latest versions of the packages are available. Once you've downloaded the package and unzipped it please take a few minutes to read through this document to get a basic understanding of installation and operation. Further detailed information is contained in the HOWTO document also part of the program package. For those that are impatient and want to get started as soon as possible skip down to the Installation section of this document to learn how to install the program.

#### GENERAL INFORMATION
This program was written to take the place (for me at least) of a Journaling program I used some years back named RoboJournal. It was a database driven program that stored all journal entries in a backend MySQL database. At some point around 2019 the developer of that program stopped active development and support of the program. Subsequently it was no longer available for most Linux distros after 2019. That program was very clean, simple and easy to use. I've made every concious effort to keep this program similar to that one. Basic and easy to use. At the time of this writing the program is nearing the end of it's beta stage at its current version of 9.x.x. It is stable and usable. Data in and data out with nothing fancy. It's a journaling program after all. Written in Python. While it is possible to use the source code and connect this program to a MySQL database backend, I've designed this program to use SQlite3 and keep the database file local to the program directory. There are plans on my TODO list to give the end user a choice for local (SQLite) database use, or MySQL use on a local or remote server. That is not yet implemented and likely won't be till sometime after version 1.0 release. *There is no need, on either Linux or Windows, to install supporting SQLite as all that is compiled into the program binaries.*

The program is primarily designed to be a single user program. That is how I use it, however as this is an open source program if you're confident in your coding skills you can change it to operate however you wish. However, be aware that if you make changes that break things then it is on you to fix said problem. I personally have no desire to make this a multi-user program. It's a journaling program and as such assumes the user wishes to keep their thoughts (entries) private or mostly private. Basic security is possible by setting a user password requiring the user to enter a username and password at the start of the program, however this **does not** encrypt, in any way, the database filles or the information inside them.

The compiled binary that is included in this repository runs nicely in Linux or Windows and should start right up if you download the zipped release file from Github. I'm working on polishing a self-contained .exe for MS Windows, but it's taking a little longer than expected. Currently have a test install on a windows system that, for all intents and purposes, appears to be working normally. Albeit, with some limitations in regards to automated backups. The MJournal program was developed using Python 3.10/3.11. When compiling I'm compiling the program into a single file, so the only dependent files are the following:

* cdb
* creds
* dblist (now dblist.json)
* firstrun
* *.json
* *.db

The source files are also included in a separate directory, however if you are planning to or decide you want to work with the source files it is strongly recommended you use a proper development environment such as PyCharm or other IDE because there is a lot going on you'll need that environment for. This also means you'll need to download the complete source package from GitHub.

 The files mentioned above should be in the root of the program directory along with the MJournal binary file. There is a setup script I'm working on the create a desktop shortcut, but till that's done you may have to make a shortcut the old fashioned way: manually. No portion of the program or setup script (later) will create a menu item in the Launcher menu (in Linux), or the start menu in windows. You just download the package from Github and run the program. Eezy Peezy!
##### Cross-Platform Compatabiilty - a gentle warning
I've taken great pains to construct the code base such that I don't have to run two branches of the code. That means that the code itself checks to see if it's running on Windows or Linux. For some processes this happens at the time the binaries are compiled. Other times this occurs at runtime. All that being said, if you alter the source code included with the package and recompile it, it's strongly recommended you DO NOT make changes to the parts that check to see which platform you're running the code on. Working with the code assumes the one doing so really knows what they're doing. I did it this way because I didn't want to have to run and care for two different branches of code. This isn't my day job, but a hobby that brings me happiness. At some point in time I'm just going to stop providing the source code with the installation package and leave it up to the individual to get the code on their own because compiling the binaries requires a certain environment to make it all work properly. So, if you see no folder named src after installation and you want the source code you'll have to downloaded it from my GitHub repository. <https://github.com/mdw1982/MJournal>

#### REQUIREMENTS
You absolutely must have Python 3 installed on your system if you intend to work with the source code. This was begun on a system using Python 3.9.2, however as I learned more about Python I eventually moved to an OS that had Python 3.10 and 3.11 as it's primary interpreter. This was done so that I could take advantage of the new match/case functionality introdced in Python 3.10. It's much faster and more efficient that **if** statements in event driven programming. That means that if you intend on working with the code you will need to have at least Python 3.10 installed on your system. That being said I haven't met a Linux system yet that doesn't come with Python as part of the OS. Linux systems released within the last few years are going to have Python 3 installed on them. So, getting the binary version of this program setup should be a breeze since it's not required to run the binaries on either Linux or Windows. The compiled binaries have everything they need to be able to run.

It may run on 3.8 but I haven't tested it. It's likely that I won't. Most modern operating systems are running at least 3.8 if not higher. If you're running Linux just pop open a terminal and check to see if Python is installed: "python3 --version". That will give you a return of the version installed on your system. If you don't get a return telling you the version then it's likely it's not installed. Use your distro's package manager to install the latest version of Python. If you're running Windows, you can get Python from the Microsoft store or you can download it from <https://www.python.org/downloads/windows/> You will want Python 3 Release. For Windows users make sure if you install Python from python.org that when you're installing it you click the check boxes to place python in your path. THAT IS IMPORTANT. For Linux users python will already be in your path. (Pyhon being in the users PATH is why its best to store the program directory in your home directory. Windows users in C:\Users\%UserName%). When you download the package from Github you're getting all the souce code, but you're not getting a self-contained compiled binary program that has everything it needs compiled into. If you download the code then it will need to be compiled. So, it's better to first get the release for your platform and install it. Later, if you wish to get the code and work with it, then by all means download it and have at it.

The compiled version of the program, whether windows or Linux, does not require Python to be installed on the system. When I compile the program it's compiled as a single file and contains everything it needs to run in one file. There are still dependency files that are program specific, but they are files that the program uses for data storage and the like that are specific to the program's operation. If all you're looking for is the compiled version to run it on your system, then check the Releases for your platform. There are two program release package: One for Linux and one for Windows.

#### INSTALLATION
Once you've extracted the files from the archive open a terminal window (YOU DON'T NEED ELEVATED PRIVILEGES TO RUN SETUP, in fact I recommend against it - the program is designed to run and setup in user space). The program directory can be anywhere in your home directory you want it to be, however the best place for it is in the root of your home folder. Anyway, navigate to the program directory in the terminal window and issue this command:  "./setup" without the quotes of course. (If you're running MS Windows then navigate to the Mjournal program directory with Windows Explorer and double-click the setup.exe file.) That command will get the setup process started and when it is finished the program will open with the default database active and ready to go. Thats It! You don't have to run any of the python code directly. The download comes with a pre-compiled binary file. If you're running Linux the binary is simply named MJournal and is found in the root of the program directory. The same goes for the Windows... You should find both in the program directory. The windows binary, or executable file will be named MJournal.exe. Essentially, the setup file moves all the .py files to the src directory and leaves the setup.py and dbbackup.py files in the root of the program directory along with the program support files named above.

##### Important
**related to versions before to 1.0**
During the installation process ***if*** you kick off the installation from Windows Explorer (on the windows platform) it may appear that nothing is happening. That's because all the output from the program during this process is going to STDOUT... i.e. the terminal output. At the very end when everything is finished you'll get a dialog announcing everything is complete. As soon as you click the OK button the program will start. To avoid this confusion open a command prompt - both Linux and Windows - and run the setup from there.

* In Linux - open a termina and CD to the program directory and run the command ./setup
* In Windows - open a command prompt and run the command .\setup.exe

This way you'll see what's going on and there won't be any confusion as to whether the program is installing. The fancy install interface is coming, but has bugs so its not ready yet.

##### Installation Summary
NOTE: these steps can be performed in the described manner on both Linux **AND** windows.

1. download the package and unzip it, then move the program folder to the root of your home directory. In Windows that would be inside your User Profile directory (C:\Users\<yourusername>)
2. Open a terminal window and CD to the program directory. (in Windows open Windows Explorer and navigate to the program directory.)
3. In the terminal window type ./setup... (In windows terminal type .\setup.exe) then hit **ENTER**. The setup program will run and when its finished the MJournal program will start and appear on the screen.

##### Program Shortcut
To be blunt there is none created... I'm working on it, but its low priority at this point because I'm concentrating on the important bits. Like everyone else I have a lot going on so this project is something I do because I like coding and not because I have to, so development takes a bit more time than one might think. That being said you'll have to create the program launcher manually. Icons for the program are located in the *images* folder inside the program directory. MS Windows:  There are two .ico images. One 80x80 for the shortcut and one 36x36 the program uses for the application windows. The same hold true for the linux version, however Linux uses the .png image format for this application.
##### Mascot Image
There is also a Mascot image for each platform version of the program. I'll leave that for you to discover. The program itself doesn't care if it shows up or not which means it will not crash or have problems if the image file is missing. The API used in this program will toss an error to the screen stating that the window (main screen) has an image element with a problem, but if you click the **close** button the program will then run. This can be a problem when accessing other areas of the program such as **Database Maintenance** or any other area of the program which causes the program to restart, such as **changing databases** if you have more than one. If you find that you're missing the mascot images, just head back to the github page for this project, enter the images folder and download the missing mascot image for your platform.

* Linux: image name Penguin.png
* Windows: image name Windows_mascot.png

To date I've not noticed any problems if icon images are missing other than being a general annoyance.

#### PROGRAM UPDATES
In most instances, unless otherwise stated, program updates will apply to the MJournal program binary. All other changes will be included in the latest release of the program.

Upgrading program binaries is as simple as downloading them and placing them in the program directory over-writting the existing program binary. The easiest way, for now, is to just download the latest version of the program. At the current time there is no automated method for updating the program other than doing it manually. That said, there are plans once the program reaches 1.0 to create a method for checking for updates.

#### GRAPHICAL USER INTERFACE or GUI
A special shout out to the wonderful author of PySimpleGUI. Before this project I'd never done anything graphical. Its all been command line stuff in PERL or PHP and Javascript. The author of PySimpleGUI has built a wonder API around Tkinter to such an awesome extent that Tkinter pretty much disappears. At least from my perspective. Check it out here! 
<https://www.pysimplegui.org/en/latest/>

#### FEATURES

* **Tree Menu:** easy access to journal entries on the main screen
* **View**: single click on entry node from tree menu loads the Journal entry to be read.
* **Tags**: add tags to each or any entry to be searched on - tags added for each entry at the time an entry is being made.
* **Main screen Function buttons**: intuitive function buttons to aid journal entries. These are explained in more detail in the HOWTO document.
* **Entry Search**: Search on Body, Title, Tags or all three.
* **Multiple Journal Databases**: create and use as many or as few as you wish.
* **Local Journal Database**: no need for connections to remote database servers. Journal Databases are SQLite database and local to the program. They live in the same directory as the program
* **Switching Databases**: easily switch from one database to another in mere seconds.
* **Journal Entry Security:** prevent people who have access to your computer from reading your journal by setting a username and password on a per database basis. Once set and enabled, the program will not open the database without the proper authentication.
* **Enable/Disable Journal Security:** The user has the ability to turn on and off password protection for a specific database.
* **Changing Password:** The program provides the user the ability to not only set a password for a specific database, but then to also change that password.
* **Easily Create New Databases**: Create new Journaling database without needing to know how. Just give it a name and off you go.
* **Insert Time and Date**: insert time and date into journal entries. Comes in real handy when making updates to existing entries.
* **Database Backups**: Easy manual and scheduled backups can be performed without knowing the technical details of how it's done. Both manual and scheduled backups.
* **Detach and Reattach Database files**: Rather than delete databases, the program has the ability to remove active database files from the program so they don't show up on the available database list. The can later be added back onto the list for access.
* **Program Theming:** the program has the ability to change its look and feel in regards to color scheme.
* **Open Source:** as open source software you have the ability to make what ever changes you deem necessary to suite your needs.
* **Remove Entries**: Rather than actually remove a journal entry you can hide or unhide the entry. There is a field in the entry database called visibible. Its default setting is 1 which means its visisble and will be accessible from the tree menu. When you hide the entry that value is set to 0, which means as long as that value is left at 0 it will not be displayed on the tree menu.
* **Key Bindings or Hot Keys**: Essentially, I've bound some of the Function keys on the keyboard to specific events in the program. Check in the HOWTO file for more information about the hot-keys. I personally find this extremely useful since the less time I have to spend touch my mouse the better I like it.
* **Restore from Backup**: it possible to restore a database from a backup while inside the program.

### More to come!

#### Issues

* 03/17/2024 - when writing to the user's crontab the a new line is created before the entry when writing to the crontab. If this is the first entry in the user's crontab the cron job doesn't happen.


