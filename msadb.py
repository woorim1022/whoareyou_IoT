import subprocess
import MySQLdb

# DB config
config = {
    'database': 'msa',
    'user': 'msa',
    'password': '1234',
    'host':'ec2-13-208-106-200.ap-northeast-3.compute.amazonaws.com',
    'port': 3306,
    'charset':'utf8',
    'use_unicode':True
}

# get ip adress
def get_ip():
    ip = '192.168.0.54'
    return ip

# connect db
def getConnection():
    conn = MySQLdb.connect(**config)
    return conn

# close db connect
def close(conn, cursor):
    if cursor != None:
        cursor.close()
    if conn != None:
        cursor.close()

# get user information
def get_user_id():
    user_ip = get_ip()
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM user_user WHERE Ip = "%s"' %user_ip)
    user_info = cursor.fetchone()
    close(conn, cursor)
    return user_info[0]



def insert_unknown(data):
    conn = getConnection()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO regi_people(category, danger, pub_date, pic, user_id) VALUES (%s, %s, %s, %s, %s)', data) # category, danger, pub_date, pic, user_id
    conn.commit()
    close(conn, cursor)


user = get_user_id()
print(user)
