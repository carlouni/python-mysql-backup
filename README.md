### Python MySQL Backup
---

A python script to create MySQL backups using <b>mysqldump</b>, <b>mysql_config_editor</b>, and <b>tar</b> utility. The original version was taken from http://tecadmin.net/python-script-for-mysql-database-backup/ by Rahul Kumar but I have added major changes since.

#### Requirements:
1. <b>Python 2.7</b>
2. <b>mysqldump</b>
- <b>Windows:</b> download the "MySQL Product Archives" from https://downloads.mysql.com/archives/community/. After extracting the file, add the <b>"bin"</b> folder (This includes mysqldump.exe) to Windows PATH so as to have it available from command line.
- <b>Linux:</b> Install the MySQL Client.
3. <b>mysql_config_editor</b>
Passing passwords within the command line is a bad practice. <b>mysql_config_editor</b> enables you to store authentication in a .mylogin.cnf file so you don't need to pass it to the command line. For more info, go to https://dev.mysql.com/doc/refman/5.7/en/mysql-config-editor.html
- <b>Windows:</b> It's also included in the "MySQL Product Archives"
- <b>Linux:</b> It's part of the MySQL Client tools
4. <b>tar</b>
The <b>tar</b> utility for Windows can be downloaded from http://gnuwin32.sourceforge.net/packages/gtar.htm

#### Steps:
##### Define login paths with mysql_config_editor
From command line execute the following.
```
shell> mysql_config_editor set --login-path=loginpath1
         --host=yourdbhost1 --user=dbuser1 --password
Enter password: enter password "dbpass1" here
```
This will store your authentication in .mylogin.cnf for future use. Repete previous steps for every DB you want to include in your back up.

To check your login paths execute the following. These login paths will be used in your JSON file.
```
shell> mysql_config_editor print --all
[loginpath1]
user = dbuser1
password = *****
host = yourdbhost1
[loginpath2]
user = dbuser2
password = *****
host = yourdbhost2
```

##### JSON File
Create a file containing a list of DBs to be backed up. The DB list must be in JSON format. See example below.
```javascript
[
    {
        "loginPath": "loginpath1",
        "dbName": "dbname1",
        "bkpPath": "/path/to/backup/folder1/"
    },
    {
        "loginPath": "loginpath2",
        "dbName": "dbname2",
        "bkpPath": "/path/to/backup/folder2/"
    }
]
```
##### Running the script (dbbackup.py)
Execute the following:
```
shell> /path/to/dbbackup.py /path/to/your_database_list.json
```
Or
```
shell> python /path/to/dbbackup.py /path/to/your_database_list.json
```

The script will output something like.
```
Backing up DB: dbname1
/path/to/backup/folder1/20200422-152835/dbname1.sql
Backup script completed
Your backups has been created in '/path/to/backup/folder1/20200422-152835' directory

Backing up DB: dbname2
/path/to/backup/folder1/20200422-152835/dbname2.sql
Backup script completed
Your backups has been created in '/path/to/backup/folder2/20200422-152835' directory

Backup results:
--------------
dbname1          ==> Succeeded 
dbname2          ==> Succeeded
```