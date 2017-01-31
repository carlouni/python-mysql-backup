#!/usr/bin/python
###########################################################
#
# This python script is used for mysql database backup
# using mysqldump and tar utility.
#
# Written by : Rahul Kumar
# Website: http://tecadmin.net
# Created date: Dec 03, 2013
# Last modified: jan 31, 2017 by Gonzalo Cardenas
# Tested with : Python 2.7.12
# Script Revision: 1.2
#
##########################################################

# Import required python libraries
import os
import time
import datetime
import pipes

# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# To take multiple databases backup, create any file like /backup/dbnames.txt and put databses names one on each line and assignd to DB_NAME variable.

DB_HOST = 'your_mysql_host' #ie. localhost
DB_USER = 'your_user_name'
DB_USER_PASSWORD = 'your_password'
#DB_NAME = '/backup/dbnames.txt'
DB_NAME = 'your_db_name'
BACKUP_PATH = '/your/backup/folder/path/'

# Getting current datetime to create seprate backup folder like "12012013-071334".
DATETIME = time.strftime('%Y%m%d-%H%M%S')

TODAYBACKUPPATH = BACKUP_PATH + DATETIME

# Checking if backup folder already exists or not. If not exists will create it.
try:
    os.stat(TODAYBACKUPPATH)
except:
    os.mkdir(TODAYBACKUPPATH)

# Code for checking if you want to take single database backup or assinged multiple backups in DB_NAME.
print "checking for databases names file."
if os.path.exists(DB_NAME):
    file1 = open(DB_NAME)
    multi = 1
    print "Databases file found..."
    print "Starting backup of all dbs listed in file " + DB_NAME
else:
    print "Databases file not found..."
    print "Starting backup of database " + DB_NAME
    multi = 0

# Starting actual database backup process.
if multi:
   in_file = open(DB_NAME,"r")
   flength = len(in_file.readlines())
   in_file.close()
   p = 1
   dbfile = open(DB_NAME,"r")

   while p <= flength:
       db = dbfile.readline()   # reading database name from file
       db = db[:-1]         # deletes extra line
       dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(dumpcmd)
       compcmd = "tar -zcvf " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".tar.gz " +  pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(compcmd)
       delcmd = "rm " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
       os.system(delcmd)
       p = p + 1
   dbfile.close()
else:
   db = DB_NAME
   dumpcmd = "mysqldump -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + db + " > " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
   os.system(dumpcmd)
   compcmd = "tar -zcvf " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".tar.gz " +  pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
   os.system(compcmd)
   delcmd = "rm " + pipes.quote(TODAYBACKUPPATH) + "/" + db + ".sql"
   os.system(delcmd)

print "Backup script completed"
print "Your backups has been created in '" + TODAYBACKUPPATH + "' directory"