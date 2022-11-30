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
    