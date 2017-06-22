#!/usr/bin/python
import MySQLdb
import time
import logging
from datetime import datetime
from secret import *
import argparse

def _update():
    """
    The function will search through the database for all apps that need to update.
    It will output the results in the output.txt with a package name per line.
    """

    current_utc = datetime.utcnow()
    current_time = int(time.mktime(current_utc.timetuple()))

    database = MySQLdb.connect(host, user, passwd, db)
    logging.warning('db connection success')

    cur = database.cursor()

    cur.execute("""
                SELECT packageName FROM apps 
                WHERE UNIX_TIMESTAMP(UTC_TIMESTAMP()) - timestampLastChecked > checkInterval 
                ORDER BY installCount DESC
                LIMIT 100 """)
    app_lst = [row[0] for row in cur]
    logging.warning('result apps count: %d' % len(app_lst))
    
    with open('output.txt', 'w') as f:
        for app in app_lst:
            f.write(app + '\n')
    logging.warning('writing done')
    cur.close()
    database.close()
    

if __name__ == '__main__':
    _update()
