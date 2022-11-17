import cs304dbi as dbi
dbi.conf('rideshare_db')

def insertpost(conn, pid, username, type, destination, time, title, seats, special_request, display_now, cost):
    """ Inserts a post into the database. """
    curs = dbi.dict_cursor(conn)
    curs.execute('''
        insert into Post(pid, username, type, destination, time, title, seats, special_request, display_now, cost) 
        values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s);''',
                      [pid, username, type, destination, time, title, seats, special_request, display_now, cost])

    conn.commit()


    