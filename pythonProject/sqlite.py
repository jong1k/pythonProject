import sqlite3

conn = sqlite3.connect('database.db')

conn.execute(
    '''
    create table users(email text, name text)
    '''
)

print('create table')

conn.close()