import cs304dbi as dbi

# ==========================================================
# The CRUD functions that do most of the CRUD work.

def insertpost(conn, username, type, date, time, destination, street_address, city, state, 
zipcode, title, seats, special_request, display_now, cost):
    """ Inserts a post into the database based on a given username, type, date, time,
    destination, street address, city, state zipcode, seats, special request, display 
    now attribute and cost. """
    curs = dbi.dict_cursor(conn)
    curs.execute(''' insert into Post(username, type, date, time, destination, street_address,
        city, state, zipcode, title, seats, special_request, display_now, cost) 
        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                      [username, type, date, time, destination, street_address, city, state, 
                      zipcode, title, seats, special_request, display_now, cost])
    conn.commit()


def insertUser(conn, username, name):
    """ inserts a given user into the User table """
    curs = dbi.dict_cursor(conn)
    curs.execute(''' insert into User(username,name)
        values (%s,%s);''',
                      [username, name])
    conn.commit()

def updateUser(conn, username, phone_number, class_year, major, hometown):
    """ updates the User table with give phone number, class year, major and hometown """
    curs = dbi.dict_cursor(conn)
    curs.execute('''update User set phone_number = %s, class_year = %s,  major = %s, 
    hometown = %s where username = %s''',
             [phone_number, class_year, major, hometown, username])
    conn.commit()

def update_post(conn, username, phone_number, class_year, major, hometown):
    """ updates the Post table with given username, type, destination, street address, 
    city, state, zipcode, date, time, title, seats, special_request, display_now, cost"""
    curs = dbi.dict_cursor(conn)
    curs.execute('''update Post set type = %s, destination = %s,  street_address = %s, city = %s, state = %s, 
    zipcode = %s, date = %s, time = %s, title = %s, seats = %s, special_request = %s
    cost = %s where username = %s''',
             [destination, stadd, city, state, zipcode, date, time, title, seats, special_request, cost, username])
    conn.commit()

def updateProfilePic(conn, their_username, filename):
    """ updates the Picfile table given a filename """
    curs = dbi.dict_cursor(conn)
    curs.execute(
                '''insert into Picfile(username,filename) values (%s,%s)
                   on duplicate key update filename = %s''',
                [their_username, filename, filename])
    conn.commit()

def deactivatePost(conn, pid):
    """ sets a given Post's diplay_now attribute to false"""
    curs = dbi.dict_cursor(conn)
    curs.execute('update Post set display_now = False where pid = %s', [pid])
    conn.commit()

def addComment(conn, username, pid, content, time):
    """ adds a comment into the Comment table given its post id, content, and 
    the time of comment """
    curs = dbi.dict_cursor(conn)
    curs.execute(
                'insert into Comment(username,pid, content, time) values (%s,%s,%s,%s)',
                [username, pid, content, time])
    conn.commit()