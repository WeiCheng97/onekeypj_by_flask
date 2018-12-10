import os
import sqlite3
import sys

db_path = b'paste.db'


def init():
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS record
           (sno VARCHAR(8) PRIMARY KEY  NOT NULL,
           lastTime  current_date);''')
    conn.commit()
    conn.close()


def put_sno(sno):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    try:
        c.execute('insert into record(sno) values("' + sno + '");')
        if conn.total_changes > 0:
            conn.commit()
            return 0
    except BaseException as e:
        print(e)
        return 1
    finally:
        c.close()


def select_sno(sno):
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    cursor = c.execute('select count(*) from record where sno = "' + sno + '";')
    return cursor.fetchone()[0]
