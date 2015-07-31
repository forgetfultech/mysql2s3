#!/usr/bin/env python

import os
import MySQLdb as mdb
import boto

from datetime import datetime

serverName = '' #Server name
dbUser = '' #DB User eg. root
dbPass = '' #DB User Pass
skipdb=['information_schema',"mysql","performance_schema"]
folderName = '' + datetime.now().strftime('%Y.%m.%d.%H.%M') #Folder Name for backup <servername>_date
backupFolder = '/usr/local/bin/db_backup/' + folderName
currentMonth = datetime.now().strftime("%B")
access_key = '' # Amazon S3 Access Key
secret_key = '' # Amazon S3 Secret Key
bucket = '' # Amazon S3 Bucket Name

con = mdb.connect('localhost', dbUser, dbPass)

os.system("mkdir -p %s" % (backupFolder))

print 'CONNECTING TO MYSQL SERVER'

cur = con.cursor()
cur.execute("SHOW DATABASES")

print 'BUILDING A LIST OF DATABASES'

dbList = []

for i in cur:
    if i[0] in skipdb: continue
    dbList.append(i[0])
    cmd='mysqldump -h localhost -u %s -p%s %s >%s/%s.sql' % (dbUser,dbPass, i[0],backupFolder,i[0])
    print 'BACKING UP - ' + i[0]
    os.system(cmd)

print 'COMPRESSING BACKUP FOLDER'

cmd = 'tar -cvzf ' + backupFolder + '.tar.gz ' + backupFolder
os.system(cmd)

print 'TRANSFEREING BACKUP TO AMAZON S3'

s3 = boto.connect_s3(access_key, secret_key)
bucket = s3.get_bucket(bucket)
key = bucket.new_key("%s/%s/%s.tar.gz" % (serverName,currentMonth,folderName))
key.set_contents_from_filename(os.path.join(os.curdir, "%s.tar.gz" % (backupFolder)))
key.set_acl('private')

print 'CLEANUP PROCESS'

cmd = 'rm -rf ' + backupFolder + '.tar.gz '
os.system(cmd)

print 'REMOVED' + backupFolder + '.tar.gz'

cmd = 'rm -rf ' + backupFolder
os.system(cmd)

print 'REMOVED' + backupFolder + '/'
