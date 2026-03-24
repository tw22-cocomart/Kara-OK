===========================================================
                KARA-OK! SYSTEM - SETUP GUIDE
===========================================================

PROJECT DESCRIPTION:
A Python-based Karaoke application featuring user registration, 
login, songbook management, and a scoring system.

-----------------------------------------------------------
1. PREREQUISITES (SYSTEM REQUIREMENTS)
-----------------------------------------------------------
Before running the application, ensure the following are 
installed on your computer:

* PYTHON (Version 3.x): 
  https://www.python.org/downloads/

* VLC MEDIA PLAYER: 
  https://www.videolan.org/vlc/
  (Required for video/audio playback integration)

* XAMPP: 
  https://www.apachefriends.org/download.html
  (Required for the MySQL Database)

-----------------------------------------------------------
2. INSTALLATION (PYTHON LIBRARIES)
-----------------------------------------------------------
Open your Command Prompt (CMD) or Terminal and run the 
following commands to install the necessary libraries:

    pip install pillow
    pip install python-vlc
    pip install mysql-connector-python

-----------------------------------------------------------
3. DATABASE SETUP (XAMPP)
-----------------------------------------------------------
1. Open the XAMPP Control Panel.
2. Start/Turn on "Apache" and "MySQL".
3. Open your web browser and go to: http://localhost/phpmyadmin/
4. Click on the "SQL" tab at the top.
5. Copy and paste the following script into the text box:

--- START SQL SCRIPT ---

CREATE DATABASE karaoke_system;

USE karaoke_system;

CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100),
    email VARCHAR(150) UNIQUE,
    password VARCHAR(255)
);

--- END SQL SCRIPT ---

6. Click the "Go" button to execute the query and create 
   the database.

-----------------------------------------------------------
4. RUNNING THE APPLICATION
-----------------------------------------------------------
1. Navigate to the folder containing your project files.
2. Open your terminal/CMD in that folder.
3. Run the application using the following command:

    python main.py

-----------------------------------------------------------
NOTES:
- Ensure MySQL remains running in XAMPP while using the app.
- Make sure all image files (like 'songbook.jpg') are in 
  the correct directory path as specified in the code.
===========================================================
