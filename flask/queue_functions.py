import cs304dbi as dbi


# ==========================================================
# The functions that do most of the queue and display of posting work.



dbi.conf('rideshare_db')

def get_posts_with_user_names(conn):
    """ gets info about all posts and corresponding usernames """
    curs = dbi.dict_cursor(conn)
    curs.execute('select * from Post inner join User using (username) order by time;')
    return curs.fetchall()

def get_profile_info(conn, username):
    """ gets profile info about a given username"""
    curs = dbi.dict_cursor(conn)
    curs.execute('select * from User where username = %s;', [username])
    return curs.fetchone()
    
def get_all_users(conn):
    curs = dbi.dict_cursor(conn)
    curs.execute('select * from User order by username')
    return curs.fetchall()

def get_all_states(conn):
    curs = dbi.dict_cursor(conn)
    curs.execute('select destination from Post')
    destinations = curs.fetchall()
    states = []
    for d in destinations:
        print(d)
        dlst = d['destination'].split(", ")
        state = dlst[3][0:2]
        if state not in states:
            states.append(state)
    return sorted(states)
