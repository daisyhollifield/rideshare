import cs304dbi as dbi

# ==========================================================
# The CRUD functions that do most of the CRUD work.


dbi.conf('rideshare_db')

def insertpost(conn, username, type, date, time, destination, street_address, city, state, zipcode, title, seats, special_request, display_now, cost):
    """ Inserts a post into the database. """
    curs = dbi.dict_cursor(conn)
    curs.execute(''' insert into Post(username, type, date, time, destination, street_address, city, state, zipcode, title, seats, special_request, display_now, cost) 
        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                      [username, type, date, time, destination, street_address, city, state, zipcode, title, seats, special_request, display_now, cost])
    conn.commit()


def insertUser(conn, username, name):
    curs = dbi.dict_cursor(conn)
    curs.execute(''' insert into User(username,name)
        values (%s,%s);''',
                      [username, name])
    conn.commit()

def updateUser(conn, username, phone_number, class_year, major, hometown):
    curs = dbi.dict_cursor(conn)
    curs.execute('update User set phone_number = %s, class_year = %s,  major = %s, hometown = %s where username = %s',
             [phone_number, class_year, major, hometown, username])
    conn.commit()

def updateProfilePic(conn, their_username, filename):
    curs = dbi.dict_cursor(conn)
    curs.execute(
                '''insert into Picfile(username,filename) values (%s,%s)
                   on duplicate key update filename = %s''',
                [their_username, filename, filename])
    conn.commit()

def deactivatePost(conn, pid):
    curs = dbi.dict_cursor(conn)
    curs.execute('update Post set display_now = False where pid = %s', [pid])
    conn.commit()