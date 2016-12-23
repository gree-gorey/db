# -*- coding: utf-8 -*-

import os
import sqlite3
from datetime import datetime

DBFILE = 'law.db'
DBSCHEMA = 'law_schema.sql'


def create_db(dbfile, schemafile):
    print('create db:', dbfile)
    has_db = os.path.exists(dbfile)
    if has_db: 
        print 'database exists, exit'
        return False

    with sqlite3.connect(dbfile) as conn:
        print 'creating schema'
        schema = None
        with open(schemafile, 'rt') as f:
            schema = f.read()

        if schema is not None:
            conn.executescript(schema)

        print 'schema created successfully'
    
    return True


def fill_db(dbfile):
    with sqlite3.connect(dbfile) as conn:
        print 'filling database...'

        # --- CheckType ---
        check_types = [
            (u'auto',),
            (u'express',),
            (u'professional',)
        ]
        conn.executemany('insert into CheckType(name) values (?)', check_types)

        # --- Lawyer ---
        lawyers = [
            (u'Ivan', u'ivan@ya.ru'),
            (u'Peter', u'peter@gmail.com'),
        ]
        conn.executemany('insert into Lawyer(id, name, email) values (null, ?, ?)', lawyers)

        # --- ContractType ---
        contract_types = [
            (u'аренды',),
            (u'лизинга',),
            (u'трудовой',),
            (u'найма', ),
            (u'рекламы',),
            (u'услуг',)
        ]
        conn.executemany('insert into ContractType(name) values (?)', contract_types)

        # --- Format ---
        formats = [
            (u'txt', 0, 0),
            (u'jpeg', 1, 0),
            (u'pdf', 1, 1),
            (u'docx', 0, 1),
        ]
        conn.executemany('insert into Format(name, needs_recognition, needs_format) values (?, ?, ?)', formats)

        # --- Orders ---
        orders = [
            (datetime(2015, 1, 15, 12, 31), u'text foo', u'/tmp/file1', u'txt', u'аренды', u'арендатор', u'user@ya.ru',
             u'auto', '1', 0, 1530.0, 8.3, datetime(2015, 1, 15, 20, 31)),
            (datetime(2015, 2, 15, 12, 31), u'text egg', u'/tmp/file2', u'txt', u'трудовой', u'рабочий', u'user1@ya.ru',
             u'express', '2', 0, 1303.2, 5.3, datetime(2015, 1, 15, 1, 31)),
            (datetime(2015, 3, 15, 12, 31), u'text goo', u'/tmp/file3', u'txt', u'лизинга', u'лизингодатель', u'user2@ya.ru',
             u'professional', '1', 1, 165.4, 5.7, datetime(2015, 1, 15, 23, 31)),
        ]
        conn.executemany(
            '''insert into Orders(id, datetime, contract_text, file_address, format, contract_type, party, user_email,
               check_type, lawyer_id, done, cost, time_amount, deadline)
               values (null, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', orders)


def query_db(dbfile):
    with sqlite3.connect(dbfile) as conn:
        print 'querying database...'

        print '--- ContractType:'
        cursor = conn.cursor()
        cursor.execute('select * from ContractType;')
        for row in cursor.fetchall():
            print row[0]

        print '--- Lawyer: '
        cursor.execute('SELECT * FROM Lawyer;')
        for row in cursor.fetchall():
            lid, name, email = row
            print lid, name, email

        print '--- Orders: '
        cursor.execute('SELECT * FROM Orders;')
        for row in cursor.fetchall():
            oid = row[0]
            deadline = row[13]
            cost = row[11]
            done = row[10]
            user = row[7]
            print oid, user, cost, deadline, '| done: {}'.format(bool(done))

        cursor.execute('SELECT COUNT(*) FROM Orders;')
        count = cursor.fetchone()
        print 'orders totally:', count[0]

        print 'who is accountable for order:'
        cursor.execute(
            ''' SELECT Orders.user_email, Orders.contract_type, Orders.done, Lawyer.name, Lawyer.email
                FROM Orders
                INNER JOIN Lawyer ON Orders.lawyer_id = Lawyer.id;
            ''')
        for row in cursor.fetchall():
            print ' '.join([unicode(x) for x in row[:3:]]), u'| проверяет: ', ' '.join(row[3::])

        print 'вот что проверяет Peter:'
        cursor.execute(
            ''' SELECT user_email, contract_type FROM Orders
                WHERE lawyer_id IN
                    (SELECT id FROM Lawyer
                     WHERE name LIKE 'Peter');
            '''
            )
        for row in cursor.fetchall():
            print '-', ' '.join(row)


if __name__ == '__main__':
    # --- prepare DB
    create_db(DBFILE, DBSCHEMA)
    fill_db(DBFILE)

    # --- query DB
    query_db(DBFILE)
