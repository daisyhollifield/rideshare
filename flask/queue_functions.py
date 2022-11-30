import cs304dbi as dbi


# ==========================================================
# The functions that do most of the queue and display of posting work.



dbi.conf('rideshare_db')

def get_posts_with_usernames(conn):
    """ gets info about all posts and corresponding usernames """
    curs = dbi.dict_cursor(conn)
    curs.execute('select * from Post inner join User using (username) where display_now = True order by date;')
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
    curs.execute('select `state` from Post')
    all_states = curs.fetchall()
    states = []
    for s in all_states:
        s_name = s['state']
        if s_name not in states:
            states.append(s_name)
    return sorted(states)

def get_result_posts(conn, destination, street_address, city, state, zipcode, user, date, time, seats, cost):
    curs = dbi.dict_cursor(conn)
    if destination == "":
        destination_string = ''
    else:
        destination_string = 'where destination = "{}"'.format(destination) #is this good enough for injection attacks?
    if street_address == "":
        street_address_string = ''
    else:
        if destination_string == "":
            street_address_string = 'where street_address = "{}"'.format(street_address) #is this good enough for injection attacks?
        else:
            street_address_string = ' and street_address = "{}"'.format(street_address) #is this good enough for injection attacks?
    if city == "":
        city_string = ""
    else:
        if destination_string == "" and street_address_string == "":
            city_string = 'where city = "{}"'.format(city) #is this good enough for injection attacks?
        else:
            city_string = ' and city = "{}"'.format(city) #is this good enough for injection attacks?
    if state == "none":
        state_string = ""
    else:
        if destination_string == "" and street_address_string == "" and city_string == "":
            state_string = 'where state = "{}"'.format(state) #is this good enough for injection attacks?
        else:
            state_string = ' and state = "{}"'.format(state) #is this good enough for injection attacks?
    
    if zipcode == "":
        zipcode_string = ""
    else:
        if destination_string == "" and street_address_string == "" and city_string == "" and state_string == "":
            zipcode_string = 'where zipcode = "{}"'.format(zipcode) #is this good enough for injection attacks?
        else:
            zipcode_string = ' and zipcode = "{}"'.format(zipcode) #is this good enough for injection attacks?
    if user == "none":
        user_string = ''
    else:
        if destination_string == '' and street_address_string == "" and city_string == "" and state_string == "" and zipcode_string == "":
            user_string = 'where username = "{}"'.format(user) #is this good enough for injection attacks?
        else:
            user_string = ' and username = "{}"'.format(user) #is this good enough for injection attacks?

    if date == "":
        date_string = ""
    else:
        if destination_string == '' and street_address_string == "" and city_string == "" and state_string == "" and zipcode_string == "" and user_string == "":
            date_string = 'where date = "{}"'.format(date) #is this good enough for injection attacks?
        else:
            date_string = ' and date = "{}"'.format(date) #is this good enough for injection attacks?

    if time == "":
        time_string = ""
    else:
        if destination_string == '' and street_address_string == "" and city_string == "" and state_string == "" and zipcode_string == "" and user_string == "" and date_string == "":
            time_string = 'where time = "{}"'.format(time) #is this good enough for injection attacks?
        else:
            time_string = ' and time = "{}"'.format(time) #is this good enough for injection attacks?
    if seats == '':
        seats_string = ''
    else:
        if destination_string == '' and street_address_string == "" and city_string == "" and state_string == "" and zipcode_string == "" and user_string == '' and date_string == '' and time_string == '':
            seats_string = 'where seats = {}'.format(seats) #is this good enough for injection attacks?
        else:
            seats_string = ' and seats = {}'.format(seats) #is this good enough for injection attacks?
    
    if cost == '':
        cost_string = ''
    else:
        if destination_string == '' and street_address_string == "" and city_string== "" and state_string == "" and zipcode_string == "" and user_string == '' and date_string == "" and time_string == '' and seats_string == '':
            cost_string = 'where cost = {}'.format(cost) #is this good enough for injection attacks?
        else:
            cost_string = ' and cost = {}'.format(cost) #is this good enough for injection attacks?
    
    curs.execute('select * from Post inner join User using (username) ' + destination_string + street_address_string + city_string + state_string + zipcode_string + user_string + date_string + time_string + seats_string + cost_string + ' order by date;')
    return curs.fetchall()