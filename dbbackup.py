#!/usr/bin/python
###########################################################
#
# This python script is used for mysql database backup
# using mysqldump and tar utility.
#
# Written by :  Gonzalo Cardenas
# Last modified: Apr 22, 2020
# Tested with : Python 2.7.17
# Script Revision: 1.3
#
# Original version: Rahul Kumar
# Website: http://tecadmin.net
# Created date: Dec 03, 2013
#
##########################################################

# Import required python libraries
import os
import time
import pipes
import json
import sys
from subprocess import Popen, PIPE

# MySQL database details to which backup to be done. Make sure below user having enough privileges to take databases backup.
# Pass the path of the file containing the list of DBs in JSON format
# Examples:
# $ python /path/to/dbbackup.py /path/to/databases.json
# $ /path/to/dbbackup.py /path/to/databases.json
db_list = []
try:
    json_file = open(os.path.normpath(sys.argv[1]))
    db_list = json.load(json_file)
except Exception as e:
    sys.stderr.write("Error reading file: " + sys.argv[1] + "\n")
    sys.stderr.write(str(e) + "\n")
    sys.exit(1)

# Getting current datetime to create seprate backup folder like "12012013-071334".
DATETIME = time.strftime('%Y%m%d-%H%M%S')

result_list =[]
for db in db_list:
    today_bkp_path = db["bkpPath"] + DATETIME

    # Checking if backup folder already exists or not. If not exists will create it.
    try:
        os.stat(pipes.quote(today_bkp_path))
    except:
        os.mkdir(pipes.quote(today_bkp_path))

    try:
        print("Backing up DB: " + db["dbName"])

        # Dump database
        p = Popen(["mysqldump", "--login-path=" + db["loginPath"], db["dbName"]], stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        if len(err) > 0:
            raise Exception(err)
        f = open(pipes.quote(today_bkp_path) + "/" + db["dbName"] + ".sql", "w")
        f.write(out)
        f.close()

        # Compress sql file
        compcmd = "tar -zcvf " + pipes.quote(today_bkp_path) + "/" + db["dbName"] + ".tar.gz " +  pipes.quote(today_bkp_path) + "/" + db["dbName"] + ".sql"
        os.system(compcmd)
        delcmd = "rm " + pipes.quote(today_bkp_path) + "/" + db["dbName"] + ".sql"
        os.system(delcmd)

        print "Backup script completed"
        print "Your backups has been created in '" + today_bkp_path + "' directory\n"
        result_list.append({'db': db["dbName"], 'result': 'Succeeded'})
    except Exception as e:
        sys.stderr.write("Error backing up DB: " + db["dbName"] + "\n")
        sys.stderr.write(str(e) + "\n")
        result_list.append({'db': db["dbName"], 'result': 'Failed'})

        # continue backing up next DB
        continue

print("Backup results:")
print("--------------")
for result in result_list:
    print '{0:20} ==> {1:10}'.format(result["db"], result["result"])
