import cs304dbi as dbi
dbi.conf('rideshare_db')

def insertpost(conn, username, type, destination, time, title, seats, special_request, display_now, cost):
    """ Inserts a post into the database. """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        insert into Post(username, type, destination, time, title, seats, special_request, display_now, cost) 
        values (%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                      [username, type, destination, time, title, seats, special_request, display_now, cost])

    conn.commit()
    