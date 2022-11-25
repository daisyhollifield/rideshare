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
        dlst = d['destination'].split(", ")
        state = dlst[3][0:2]
        if state not in states:
            states.append(state)
    return sorted(states)

def get_posts_by_user_and_seats_and_cost(conn, user, seats, cost):
    curs = dbi.dict_cursor(conn)
    if user == "none":
        user_string = ''
    else:
        user_string = 'where username = "{}"'.format(user) #is this good enough for injection attacks?

    if seats == '':
        seats_string = ''
    else:
        if user_string == '':
            seats_string = 'where seats = {}'.format(seats) #is this good enough for injection attacks?
        else:
            seats_string = ' and seats = {}'.format(seats) #is this good enough for injection attacks?
    
    if cost == '':
        cost_string = ''
    else:
        if user_string == '' and seats_string == '':
            cost_string = 'where cost = {}'.format(cost) #is this good enough for injection attacks?
        else:
            cost_string = ' and cost = {}'.format(cost) #is this good enough for injection attacks?
    
    curs.execute('select * from Post inner join User using (username) ' + user_string + seats_string + cost_string + ' order by time;')
    return curs.fetchall()