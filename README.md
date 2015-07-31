MySQL to S3
===========================================

Simple utility that dumps mysql databases and archives them to send to Amazon S3

Define Servname and DB credentials
serverName = ''
dbUser = ''
dbPass = ''

Define prefix for archive name (usually servername_ note: date gets added automatically)
folderName = '' 

Define Amazon S3 credentials
access_key = ''
secret_key = ''
bucket = ''